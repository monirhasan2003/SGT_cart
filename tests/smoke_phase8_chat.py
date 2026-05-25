"""Phase 8 (Chunk B) smoke test — the two chat systems.

Covers the chat service, the REST API, the web triage flow and the admin
support desk, plus the phone-number guard and the SocketIO connection.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase8_chat.py <admin_password>
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db, socketio
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.chat import ChatThread, CHAT_SUPPORT, CHAT_VENDOR, SUPPORT_REFUND, SUPPORT_DELIVERY
from app.models.notification import Notification, NOTIF_CHAT
from app.services.chat_service import (
    get_or_create_vendor_thread, get_or_create_support_thread,
    post_message, can_access, mark_thread_read, threads_for,
)

ADMIN_EMAIL = "monirhasan2003@gmail.com"
CUSTOMER = "smoke_p8b_customer@example.com"
SELLER = "smoke_p8b_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p8b-cat"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for email in (CUSTOMER, SELLER):
            u = User.query.filter_by(email=email).first()
            if not u:
                continue
            for t in ChatThread.query.filter(
                db.or_(ChatThread.customer_id == u.id,
                       ChatThread.vendor_id.in_(
                           db.session.query(VendorProfile.id).filter_by(user_id=u.id)))
            ).all():
                db.session.delete(t)
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)
            OtpCode.query.filter_by(user_id=u.id).delete()
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


def api_token(app, c, email):
    c.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
    r = c.post("/api/v1/auth/verify-otp",
               json={"email": email, "code": latest_otp(app, email)})
    return (r.get_json() or {}).get("access_token")


def web_login(app, c, email, account_type):
    c.post("/login/", data={"email": email, "password": PASSWORD,
                            "account_type": account_type})
    c.post("/verify-otp/", data={"code": latest_otp(app, email)})


def seed(app):
    with app.app_context():
        cat = Category(name_en="Smoke P8B Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P8B Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P8B Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P8B Smoke Store",
                           slug="p8b-smoke-store", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(vendor_id=vp.id, category_id=cat.id,
                          title_en="P8B Smoke Product", slug="p8b-smoke-product",
                          base_price=300, stock=10, status=PRODUCT_PUBLISHED)
        db.session.add(product)
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id, "product_id": product.id,
                "product_slug": product.slug, "vendor_slug": vp.slug}


def main():
    admin_password = sys.argv[1] if len(sys.argv) > 1 else ""
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # service layer
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        seller = db.session.get(User, ids["seller_id"])
        vendor = db.session.get(VendorProfile, ids["vendor_id"])
        product = db.session.get(Product, ids["product_id"])

        vt1 = get_or_create_vendor_thread(customer, vendor, product)
        vt2 = get_or_create_vendor_thread(customer, vendor)
        check("vendor thread is one-per-pair (idempotent)", vt1.id == vt2.id)
        check("vendor thread kind", vt1.kind == CHAT_VENDOR)

        st_refund = get_or_create_support_thread(customer, SUPPORT_REFUND)
        st_refund2 = get_or_create_support_thread(customer, SUPPORT_REFUND)
        st_delivery = get_or_create_support_thread(customer, SUPPORT_DELIVERY)
        check("support thread reused per topic", st_refund.id == st_refund2.id)
        check("different topic -> different thread", st_refund.id != st_delivery.id)
        check("support thread kind + topic",
              st_refund.kind == CHAT_SUPPORT and st_refund.topic == SUPPORT_REFUND)

        # phone guard inside post_message
        msg, error = post_message(vt1, customer,
                                  "Hi, is this available? call me 01712345678")
        check("post_message succeeds", error is None and msg is not None)
        check("phone number redacted from message",
              msg.is_flagged and "01712345678" not in msg.body
              and "[number removed]" in msg.body)

        # recipient (the seller) got a chat notification
        check("seller notified of new message",
              Notification.query.filter_by(user_id=seller.id, kind=NOTIF_CHAT).count() >= 1)

        # access control
        other = User(name="Outsider", email="smoke_p8b_x@example.com",
                     role="customer", is_active=True)
        other.set_password(PASSWORD)
        db.session.add(other)
        db.session.flush()
        check("participant can access thread", can_access(customer, vt1))
        check("seller can access their vendor thread", can_access(seller, vt1))
        check("outsider cannot access thread", not can_access(other, vt1))
        check("seller cannot access support thread", not can_access(seller, st_refund))
        db.session.delete(other)

        # seller replies, customer reads
        post_message(vt1, seller, "Yes, it is in stock!")
        before = vt1.unread_count(customer.id)
        mark_thread_read(vt1, customer)
        check("mark_thread_read clears unread for the reader",
              before >= 1 and vt1.unread_count(customer.id) == 0)
        check("threads_for customer lists their threads",
              len(threads_for(customer)) >= 3)
        db.session.commit()

    # ====================================================================
    # REST API
    # ====================================================================
    with app.test_client() as c:
        token = api_token(app, c, CUSTOMER)
        auth = {"Authorization": f"Bearer {token}"}
        check("customer API token obtained", bool(token))

        r = c.get("/api/v1/chat/support/topics", headers=auth)
        check("GET /chat/support/topics",
              r.status_code == 200 and len((r.get_json() or {}).get("topics", [])) == 4)

        r = c.post("/api/v1/chat/threads/support", headers=auth,
                   json={"topic": "delivery"})
        api_thread = (r.get_json() or {}).get("thread", {})
        check("POST /chat/threads/support (triaged)",
              r.status_code == 201 and api_thread.get("topic") == "delivery")

        r = c.post("/api/v1/chat/threads/support", headers=auth, json={"topic": "bogus"})
        check("support thread rejects an unknown topic", r.status_code == 400)

        r = c.post("/api/v1/chat/threads/vendor", headers=auth,
                   json={"vendor_slug": ids["vendor_slug"],
                         "product_slug": ids["product_slug"]})
        vthread = (r.get_json() or {}).get("thread", {})
        check("POST /chat/threads/vendor", r.status_code == 201
              and vthread.get("kind") == "vendor")

        r = c.post(f"/api/v1/chat/threads/{vthread['id']}/messages", headers=auth,
                   json={"body": "Please reply at 01898765432 thanks"})
        sent = (r.get_json() or {}).get("message", {})
        check("API message posts with phone redaction",
              r.status_code == 201 and sent.get("is_flagged")
              and "01898765432" not in sent.get("body", ""))

        r = c.get("/api/v1/chat/threads", headers=auth)
        check("GET /chat/threads", r.status_code == 200
              and len((r.get_json() or {}).get("threads", [])) >= 2)

        r = c.get(f"/api/v1/chat/threads/{vthread['id']}", headers=auth)
        check("GET /chat/threads/<id> with messages",
              r.status_code == 200
              and "messages" in (r.get_json() or {}).get("thread", {}))

        # access control — a thread the customer is not part of
        with app.app_context():
            foreign = get_or_create_support_thread(
                db.session.get(User, ids["seller_id"]), SUPPORT_REFUND)
            foreign_id = foreign.id
        r = c.get(f"/api/v1/chat/threads/{foreign_id}", headers=auth)
        check("API blocks access to a foreign thread (404)", r.status_code == 404)

    # ====================================================================
    # web triage flow
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")

        r = c.get("/messages/")
        check("web GET /messages/ inbox", r.status_code == 200)

        r = c.get("/messages/new")
        check("web GET /messages/new triage screen",
              r.status_code == 200 and b"SGT Support" in r.data
              and b"Ask a Seller" in r.data)

        r = c.post("/messages/start/support", data={"topic": "purchase"})
        check("web start support chat -> redirect to thread",
              r.status_code == 302 and "/messages/" in r.headers.get("Location", ""))

        r = c.post("/messages/start/vendor",
                   data={"vendor_id": ids["vendor_id"], "product_id": ids["product_id"]},
                   follow_redirects=True)
        check("web start seller chat", r.status_code == 200 and b"Seller chat" in r.data)

        # send a message through the web form
        with app.app_context():
            vt = ChatThread.query.filter_by(
                kind=CHAT_VENDOR, customer_id=ids["customer_id"]).first()
            vt_id = vt.id
        r = c.post(f"/messages/{vt_id}/send", data={"body": "Thanks for the help"},
                   follow_redirects=True)
        check("web send message", r.status_code == 200 and b"Thanks for the help" in r.data)

    # ====================================================================
    # admin support desk
    # ====================================================================
    if admin_password:
        with app.test_client() as c:
            c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})
            r = c.get("/admin/messages/")
            check("admin support inbox lists threads",
                  r.status_code == 200 and b"Support Messages" in r.data)

            with app.app_context():
                st = ChatThread.query.filter_by(
                    kind=CHAT_SUPPORT, customer_id=ids["customer_id"]).first()
                st_id = st.id
            r = c.get(f"/admin/messages/{st_id}/")
            check("admin opens a support thread", r.status_code == 200)

            r = c.post(f"/admin/messages/{st_id}/send",
                       data={"body": "Hello, this is SGT Support. How can we help?"},
                       follow_redirects=True)
            check("admin replies to support thread",
                  r.status_code == 200 and b"SGT Support. How can we help" in r.data)

            with app.app_context():
                st = db.session.get(ChatThread, st_id)
                check("admin reply stored with admin role",
                      any(m.sender_role == "admin" for m in st.messages))
    else:
        print("(admin password not supplied — admin desk checks skipped)")

    # ====================================================================
    # SocketIO wiring
    # ====================================================================
    sclient = socketio.test_client(app)
    check("SocketIO client connects", sclient.is_connected())
    sclient.disconnect()

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 8 chat smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
