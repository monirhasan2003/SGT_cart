"""Phase 15 Chunk D-4 smoke test — trust & seller credibility.

Covers:
  * `VendorProfile.is_verified_seller` — True only when status=approved AND
    both trade_license_doc and nid_doc are set.
  * `has_trade_license_verified` / `has_nid_verified` independent flags.
  * `vendor_stats_service.trust_stats(vendor)` returns:
      - positive_rate, review_count from delivered + reviewed orders,
      - avg_delivery_days, cancel_rate_pct from existing aggregates,
      - avg_reply_minutes from chat history,
      - three verification booleans.
  * Product page renders:
      - "Verified by SGT" badge when is_verified_seller is True,
      - bilingual KYC badges (Trade License + NID, with Bengali label),
      - "Why buy from this seller?" card with at least one signal,
      - none of the above for an un-verified low-stat seller.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d4.py
"""
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.order import Order, SubOrder, OrderItem, SUBORDER_DELIVERED
from app.models.review import Review
from app.models.chat import ChatThread, ChatMessage, CHAT_VENDOR
from app.services.vendor_stats_service import trust_stats
from app.services.review_service import recompute_product_rating, recompute_vendor_rating

CUSTOMERS = [f"smoke_p15d4_c{i}@example.com" for i in range(1, 6)]
SELLER_VERIFIED = "smoke_p15d4_verified@example.com"
SELLER_PLAIN = "smoke_p15d4_plain@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d4-cat"
PROD_VERIFIED_SLUG = "p15d4-verified-product"
PROD_PLAIN_SLUG = "p15d4-plain-product"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        emails = CUSTOMERS + [SELLER_VERIFIED, SELLER_PLAIN]
        users = [u for u in
                 (User.query.filter_by(email=e).first() for e in emails)
                 if u is not None]
        uids = [u.id for u in users]
        if uids:
            # Chat messages -> threads
            ChatMessage.query.filter(ChatMessage.sender_id.in_(uids)).delete(
                synchronize_session=False)
            ChatThread.query.filter(
                db.or_(ChatThread.customer_id.in_(uids),
                       ChatThread.vendor_id.in_(
                           db.session.query(VendorProfile.id).filter(
                               VendorProfile.user_id.in_(uids))))
            ).delete(synchronize_session=False)
        for u in users:
            for r in Review.query.filter_by(user_id=u.id).all():
                db.session.delete(r)
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)
        db.session.flush()
        for u in users:
            db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()


def seed(app):
    """Two sellers: verified (full KYC + 5 reviews + chat history) vs plain."""
    with app.app_context():
        cat = Category(name_en="Smoke P15D4", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)

        # ------ Verified seller ------
        s1 = User(name="Verified Seller", email=SELLER_VERIFIED,
                  role="seller", is_active=True)
        s1.set_password(PASSWORD)
        # Plain seller (no KYC docs at all)
        s2 = User(name="Plain Seller", email=SELLER_PLAIN,
                  role="seller", is_active=True)
        s2.set_password(PASSWORD)
        db.session.add_all([s1, s2])
        db.session.flush()

        v1 = VendorProfile(
            user_id=s1.id, shop_name_en="Verified Shop", slug="p15d4-verified-shop",
            status=VENDOR_APPROVED, commission_rate=10,
            trade_license_no="TL-VER", trade_license_doc="kyc/tl.pdf",
            nid_number="NID-VER", nid_doc="kyc/nid.pdf",
            verification_submitted_at=datetime.utcnow(),
            avg_delivery_days=1.5, cancel_rate=0.02,
        )
        v2 = VendorProfile(
            user_id=s2.id, shop_name_en="Plain Shop", slug="p15d4-plain-shop",
            status=VENDOR_APPROVED, commission_rate=10,
        )
        db.session.add_all([v1, v2])
        db.session.flush()

        p1 = Product(vendor_id=v1.id, category_id=cat.id,
                     title_en="Verified Seller Product", slug=PROD_VERIFIED_SLUG,
                     base_price=600, stock=20, status=PRODUCT_PUBLISHED)
        p2 = Product(vendor_id=v2.id, category_id=cat.id,
                     title_en="Plain Seller Product", slug=PROD_PLAIN_SLUG,
                     base_price=500, stock=10, status=PRODUCT_PUBLISHED)
        db.session.add_all([p1, p2])
        db.session.flush()

        # 5 customers with delivered orders + reviews on p1: four 5★, one 3★
        # → 80% positive rate.
        ratings = [5, 5, 5, 5, 3]
        cust_ids = []
        for i, rating in enumerate(ratings):
            cust = User(name=f"P15D4 C{i}", email=CUSTOMERS[i],
                        role="customer", is_active=True)
            cust.set_password(PASSWORD)
            db.session.add(cust)
            db.session.flush()
            cust_ids.append(cust.id)
            order = Order(customer_id=cust.id,
                          order_number=f"SGTP15D4-T{i:02d}",
                          payment_method="cod", payment_status="pending",
                          ship_name=cust.name, ship_phone="01700000099",
                          ship_address_line="1 Test St", ship_city="Dhaka",
                          subtotal=600, shipping_fee=0, total_amount=600)
            db.session.add(order)
            db.session.flush()
            sub = SubOrder(order_id=order.id, vendor_id=v1.id, subtotal=600,
                           status=SUBORDER_DELIVERED)
            db.session.add(sub)
            db.session.flush()
            db.session.add(OrderItem(sub_order_id=sub.id, product_id=p1.id,
                                     title="Verified Product", unit_price=600,
                                     quantity=1, line_total=600))
            db.session.add(Review(product_id=p1.id, user_id=cust.id,
                                  rating=rating, comment=f"review{i}",
                                  is_verified=True))
        recompute_product_rating(p1)
        recompute_vendor_rating(v1)

        # Chat history — 1 thread, customer asks then seller replies 30 min later.
        thread = ChatThread(kind=CHAT_VENDOR, customer_id=cust_ids[0],
                            vendor_id=v1.id, subject="P15D4")
        db.session.add(thread)
        db.session.flush()
        t0 = datetime.utcnow() - timedelta(days=1)
        db.session.add_all([
            ChatMessage(thread_id=thread.id, sender_id=cust_ids[0],
                        sender_role="customer", body="Original original?",
                        created_at=t0),
            ChatMessage(thread_id=thread.id, sender_id=s1.id,
                        sender_role="seller", body="Yes, original.",
                        created_at=t0 + timedelta(minutes=30)),
            ChatMessage(thread_id=thread.id, sender_id=cust_ids[0],
                        sender_role="customer", body="Warranty?",
                        created_at=t0 + timedelta(hours=2)),
            ChatMessage(thread_id=thread.id, sender_id=s1.id,
                        sender_role="seller", body="6 months.",
                        created_at=t0 + timedelta(hours=2, minutes=20)),
        ])
        thread.last_message_at = t0 + timedelta(hours=2, minutes=20)
        db.session.commit()
        return {"v1": v1.id, "v2": v2.id, "p1": p1.id, "p2": p2.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # model properties
    # ====================================================================
    with app.app_context():
        v1 = db.session.get(VendorProfile, ids["v1"])
        v2 = db.session.get(VendorProfile, ids["v2"])

        check("is_verified_seller True for full-KYC + approved",
              v1.is_verified_seller is True)
        check("is_verified_seller False for plain seller",
              v2.is_verified_seller is False)
        check("has_trade_license_verified True for verified",
              v1.has_trade_license_verified is True)
        check("has_nid_verified True for verified",
              v1.has_nid_verified is True)
        check("plain seller has no KYC flags",
              v2.has_trade_license_verified is False
              and v2.has_nid_verified is False)

    # ====================================================================
    # trust_stats helper
    # ====================================================================
    with app.app_context():
        v1 = db.session.get(VendorProfile, ids["v1"])
        v2 = db.session.get(VendorProfile, ids["v2"])

        t1 = trust_stats(v1)
        check("trust_stats positive_rate computed",
              t1["positive_rate"] == 80.0 and t1["review_count"] == 5)
        check("trust_stats avg_delivery_days surfaced",
              t1["avg_delivery_days"] == 1.5)
        check("trust_stats cancel_rate_pct from existing aggregate",
              t1["cancel_rate_pct"] == 2.0)
        check("trust_stats avg_reply_minutes computed from chat",
              t1["avg_reply_minutes"] is not None
              and 20 <= t1["avg_reply_minutes"] <= 40)
        check("trust_stats verification booleans True for verified",
              t1["is_verified_seller"] is True
              and t1["has_trade_license_verified"] is True
              and t1["has_nid_verified"] is True)

        # Plain seller — sparse signal
        t2 = trust_stats(v2)
        check("trust_stats handles no-data seller gracefully",
              t2["positive_rate"] is None and t2["review_count"] == 0
              and t2["avg_delivery_days"] is None
              and t2["avg_reply_minutes"] is None
              and t2["is_verified_seller"] is False)

    # ====================================================================
    # product page rendering
    # ====================================================================
    with app.test_client() as c:
        body = c.get(f"/product/{PROD_VERIFIED_SLUG}/").data.decode("utf-8", errors="ignore")
        check("verified product page renders", "Sold By" in body)
        check("Verified by SGT badge present",
              "Verified by SGT" in body)
        check("bilingual KYC badge: trade license",
              "Trade License Verified" in body
              and "ব্যবসায়িক লাইসেন্স যাচাইকৃত" in body)
        check("bilingual KYC badge: NID",
              "NID Verified" in body
              and "জাতীয় পরিচয়পত্র যাচাইকৃত" in body)
        check("Why buy card present",
              "Why buy from this seller" in body)
        check("Why buy card surfaces positive_rate",
              "80.0% positive" in body)
        check("Why buy card surfaces avg delivery",
              "1.5-day delivery" in body)
        check("Why buy card surfaces reply latency",
              "Replies in ~" in body)
        check("Why buy card surfaces order success",
              "98.0% order success" in body)

        # Plain seller product — no verified / KYC / Why-buy card
        body_p = c.get(f"/product/{PROD_PLAIN_SLUG}/").data.decode("utf-8", errors="ignore")
        check("plain product page renders", "Sold By" in body_p)
        check("plain seller has no Verified-by-SGT badge",
              "Verified by SGT" not in body_p)
        check("plain seller has no bilingual KYC panel",
              "ব্যবসায়িক লাইসেন্স যাচাইকৃত" not in body_p
              and "জাতীয় পরিচয়পত্র যাচাইকৃত" not in body_p)
        check("plain seller has no Why-buy card (no signal yet)",
              "Why buy from this seller" not in body_p)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-4 trust & seller credibility smoke test: "
          f"{passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
