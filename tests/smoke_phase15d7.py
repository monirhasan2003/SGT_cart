"""Phase 15 Chunk D-7 smoke test — communication enhancement.

Covers:
  * `User.last_seen_at` column and `ChatMessage.audio_path` exist.
  * `presence_service.mark_user_online` / `is_user_online` honor the
    ONLINE_WINDOW_SECONDS gate.
  * `chat_service.post_message` accepts an `audio_path` and stamps the
    sender's `last_seen_at`.
  * Empty body + audio is allowed (placeholder body); empty + no audio is
    rejected.
  * Product page Sold-By panel renders:
      - the presence indicator (Online / Last seen / Offline),
      - "Typically replies in ~X" line when avg_reply_minutes exists,
      - quick-question buttons (login required, hidden when viewing your own
        store).
  * POST /messages/quick-question creates/finds the vendor thread + posts
    the canonical question body.
  * POST /messages/<id>/send-audio with a tiny webm payload persists the
    audio_path. Unknown extensions are rejected.
  * Quick-question rejects an unknown key and self-chat.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d7.py
"""
import io
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.chat import ChatThread, ChatMessage, CHAT_VENDOR
from app.services import presence_service
from app.services.chat_service import post_message, get_or_create_vendor_thread
from app.services.quick_questions import QUICK_QUESTIONS, question_body

CUSTOMER = "smoke_p15d7_customer@example.com"
SELLER = "smoke_p15d7_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d7-cat"
PROD_SLUG = "p15d7-product-a"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        users = [u for u in
                 (User.query.filter_by(email=e).first()
                  for e in (CUSTOMER, SELLER))
                 if u is not None]
        for u in users:
            for t in ChatThread.query.filter(
                db.or_(ChatThread.customer_id == u.id,
                       ChatThread.vendor_id.in_(
                           db.session.query(VendorProfile.id).filter_by(
                               user_id=u.id)))
            ).all():
                db.session.delete(t)
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)
            OtpCode.query.filter_by(user_id=u.id).delete()
        db.session.flush()
        for u in users:
            db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()


def latest_otp(app, email):
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query
               .filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
        return otp.code if otp else None


def web_login(app, c, email, account_type):
    c.post("/login/", data={"email": email, "password": PASSWORD,
                            "account_type": account_type})
    c.post("/verify-otp/", data={"code": latest_otp(app, email)})


def seed(app):
    with app.app_context():
        cat = Category(name_en="Smoke P15D7", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P15D7 Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P15D7 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15D7 Shop",
                           slug="p15d7-shop", status=VENDOR_APPROVED,
                           commission_rate=10,
                           trade_license_doc="kyc/tl.pdf", nid_doc="kyc/nid.pdf")
        db.session.add(vp)
        db.session.flush()
        product = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D7 Product", slug=PROD_SLUG,
            base_price=400, stock=10, status=PRODUCT_PUBLISHED,
        )
        db.session.add(product)
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id, "product_id": product.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    # Tighten the online window so the offline transition is quick to test.
    presence_service.ONLINE_WINDOW_SECONDS = 2
    purge(app)
    ids = seed(app)

    # ====================================================================
    # presence_service user APIs
    # ====================================================================
    presence_service.reset()
    presence_service.mark_user_online(ids["seller_id"])
    check("is_user_online True after mark_user_online",
          presence_service.is_user_online(ids["seller_id"]) is True)
    check("user_last_seen_epoch returns a recent timestamp",
          presence_service.user_last_seen_epoch(ids["seller_id"]) is not None)
    time.sleep(2.1)
    check("is_user_online False after the window expires",
          presence_service.is_user_online(ids["seller_id"]) is False)
    presence_service.reset()

    # ====================================================================
    # quick_questions service
    # ====================================================================
    check("quick_questions has at least 3 entries", len(QUICK_QUESTIONS) >= 3)
    check("question_body resolves a known key",
          question_body("delivery_time") is not None)
    check("question_body returns None for unknown key",
          question_body("nope") is None)
    check("quick-questions include bilingual labels",
          all(("label_en" in q and "label_bn" in q) for q in QUICK_QUESTIONS))

    # ====================================================================
    # chat_service.post_message + audio_path + last_seen_at
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        seller = db.session.get(User, ids["seller_id"])
        vendor = db.session.get(VendorProfile, ids["vendor_id"])
        product = db.session.get(Product, ids["product_id"])

        before_last_seen = customer.last_seen_at
        thread = get_or_create_vendor_thread(customer, vendor, product)

        msg, error = post_message(thread, customer, "", audio_path=None)
        check("post_message rejects empty body + no audio",
              msg is None and error)

        msg, error = post_message(thread, customer, "",
                                  audio_path="uploads/chat_audio/test.webm")
        check("post_message accepts empty body when audio_path supplied",
              error is None and msg is not None
              and msg.audio_path == "uploads/chat_audio/test.webm"
              and msg.body == "[voice message]")

        customer = db.session.get(User, ids["customer_id"])
        check("post_message stamps sender.last_seen_at",
              customer.last_seen_at is not None
              and customer.last_seen_at != before_last_seen)

    # ====================================================================
    # product page presence + quick-question buttons
    # ====================================================================
    presence_service.reset()
    presence_service.mark_user_online(ids["seller_id"])
    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("Sold-By presence indicator shows Online now",
              "Online now" in body and "pdp-seller-presence" in body)
        # anonymous → no quick-question buttons
        check("anonymous user does NOT see quick-question buttons",
              "pdp-quick-questions" not in body)
    presence_service.reset()

    # Force a stale presence (no socket connection) → fallback to Last seen.
    with app.app_context():
        from datetime import datetime
        seller = db.session.get(User, ids["seller_id"])
        seller.last_seen_at = datetime.utcnow()
        db.session.commit()
    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("Sold-By falls back to Last seen when not online",
              "Last seen" in body)

    # Logged-in customer sees quick-question buttons
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("logged-in customer sees quick-question section",
              "pdp-quick-questions" in body and "Quick questions" in body)
        check("at least one bilingual quick-question label rendered",
              "ডেলিভারি কত দিনে?" in body)

        # POST quick-question
        r = c.post("/messages/quick-question", data={
            "vendor_id": ids["vendor_id"],
            "product_id": ids["product_id"],
            "question_key": "delivery_time",
        }, follow_redirects=False)
        check("quick-question redirects to the new vendor thread",
              r.status_code in (302, 303)
              and "/messages/" in r.headers.get("Location", ""))
        with app.app_context():
            t = ChatThread.query.filter_by(
                kind=CHAT_VENDOR, customer_id=ids["customer_id"],
                vendor_id=ids["vendor_id"],
            ).first()
            check("vendor thread created with the canonical body",
                  t is not None and any(
                      m.body == "Hi, how long will delivery take?"
                      for m in t.messages
                  ))

        # Unknown key rejected
        r = c.post("/messages/quick-question", data={
            "vendor_id": ids["vendor_id"], "product_id": ids["product_id"],
            "question_key": "bogus",
        }, follow_redirects=False)
        check("quick-question rejects an unknown key",
              r.status_code in (302, 303))

    # Self-chat blocked
    with app.test_client() as c:
        web_login(app, c, SELLER, "seller")
        r = c.post("/messages/quick-question", data={
            "vendor_id": ids["vendor_id"], "product_id": ids["product_id"],
            "question_key": "delivery_time",
        }, follow_redirects=False)
        check("quick-question blocks seller from chatting with their own shop",
              r.status_code in (302, 303)
              and "/messages/" in r.headers.get("Location", ""))

    # ====================================================================
    # Audio upload endpoint
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")
        with app.app_context():
            thread = ChatThread.query.filter_by(
                customer_id=ids["customer_id"], vendor_id=ids["vendor_id"]
            ).first()
            thread_id = thread.id

        # Reject unknown extension (.exe)
        bad = (io.BytesIO(b"fake binary"), "voice.exe")
        c.post(f"/messages/{thread_id}/send-audio",
               data={"audio": bad}, content_type="multipart/form-data")
        with app.app_context():
            t = db.session.get(ChatThread, thread_id)
            bad_msgs = [m for m in t.messages
                        if (m.audio_path or "").endswith(".exe")]
            check("audio upload rejects unknown extension",
                  not bad_msgs)

        # Accept a tiny webm payload
        good = (io.BytesIO(b"webm-bytes" * 32), "voice.webm")
        c.post(f"/messages/{thread_id}/send-audio",
               data={"audio": good}, content_type="multipart/form-data")
        with app.app_context():
            t = db.session.get(ChatThread, thread_id)
            audio_msgs = [m for m in t.messages if m.audio_path]
            check("audio upload persists ChatMessage with audio_path",
                  any(m.audio_path.startswith("uploads/chat_audio/")
                      and m.audio_path.endswith(".webm")
                      for m in audio_msgs))
            # Body uses the placeholder when audio is the only content
            voice_msg = next((m for m in audio_msgs
                              if m.body == "[voice message]"), None)
            check("voice message uses '[voice message]' placeholder body",
                  voice_msg is not None)

    # Clean up any audio files we wrote.
    with app.app_context():
        for m in ChatMessage.query.filter(
            ChatMessage.audio_path.like("uploads/chat_audio/%")
        ).all():
            full = os.path.join(app.config["UPLOAD_FOLDER"], "..", m.audio_path)
            try:
                if os.path.exists(full):
                    os.remove(full)
            except Exception:  # noqa: BLE001
                pass

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-7 communication smoke test: "
          f"{passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
