"""Phase 15 Chunk D-0 smoke test — anti-disintermediation enforcement.

Covers:
  * Seller chat phone-share logs a PolicyViolation.
  * Customer chat phone-share is redacted but NOT logged (no auto-block).
  * Customer review phone-share is redacted in title + comment, no log.
  * Two seller violations auto-suspend the vendor (status -> suspended) and
    fire admin + seller `NOTIF_SYSTEM` notifications.
  * Admin policy-violations list page renders with the rows.
  * Admin /admin/vendors/<id>/unsuspend reinstates a suspended vendor.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d0.py <admin_password>
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, ROLE_ADMIN
from app.models.vendor import (
    VendorProfile, VENDOR_APPROVED, VENDOR_SUSPENDED,
)
from app.models.otp import OtpCode
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.order import Order, SubOrder, OrderItem, SUBORDER_DELIVERED
from app.models.review import Review
from app.models.chat import ChatThread
from app.models.notification import Notification, NOTIF_SYSTEM
from app.models.policy import (
    PolicyViolation, SURFACE_CHAT, SURFACE_REVIEW, SELLER_VIOLATION_THRESHOLD,
)
from app.services.chat_service import (
    get_or_create_vendor_thread, post_message,
)
from app.services.review_service import submit_review, delete_review

ADMIN_EMAIL = "monirhasan2003@gmail.com"
CUSTOMER = "smoke_p15d0_customer@example.com"
SELLER = "smoke_p15d0_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d0-cat"
ORDER_NO = "SGTP15D0-TEST01"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        users = [u for u in
                 (User.query.filter_by(email=e).first() for e in (CUSTOMER, SELLER))
                 if u is not None]
        for u in users:
            PolicyViolation.query.filter_by(user_id=u.id).delete()
            Notification.query.filter_by(user_id=u.id).delete()
            for rv in Review.query.filter_by(user_id=u.id).all():
                db.session.delete(rv)
            for t in ChatThread.query.filter(
                db.or_(ChatThread.customer_id == u.id,
                       ChatThread.vendor_id.in_(
                           db.session.query(VendorProfile.id).filter_by(user_id=u.id)))
            ).all():
                db.session.delete(t)
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
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


def seed(app):
    """Seller + customer + a published product + a delivered order."""
    with app.app_context():
        cat = Category(name_en="Smoke P15D0", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P15D0 Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P15D0 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15D0 Store",
                           slug="p15d0-store", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(vendor_id=vp.id, category_id=cat.id,
                          title_en="P15D0 Product", slug="p15d0-product",
                          base_price=300, stock=10, status=PRODUCT_PUBLISHED)
        db.session.add(product)
        db.session.flush()
        order = Order(customer_id=customer.id, order_number=ORDER_NO,
                      payment_method="cod", payment_status="pending",
                      ship_name="P15D0 Customer", ship_phone="01700000099",
                      ship_address_line="1 Test St", ship_city="Dhaka",
                      subtotal=300, shipping_fee=0, total_amount=300)
        db.session.add(order)
        db.session.flush()
        sub = SubOrder(order_id=order.id, vendor_id=vp.id, subtotal=300,
                       status=SUBORDER_DELIVERED)
        db.session.add(sub)
        db.session.flush()
        db.session.add(OrderItem(sub_order_id=sub.id, product_id=product.id,
                                 title="P15D0 Product", unit_price=300,
                                 quantity=1, line_total=300))
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id, "product_id": product.id}


def main():
    admin_password = sys.argv[1] if len(sys.argv) > 1 else ""
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # customer in chat — redact but no log, no block
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        seller = db.session.get(User, ids["seller_id"])
        vendor = db.session.get(VendorProfile, ids["vendor_id"])
        product = db.session.get(Product, ids["product_id"])

        thread = get_or_create_vendor_thread(customer, vendor, product)
        msg, error = post_message(
            thread, customer, "hi, can you call me at 01712345678 please?"
        )
        check("customer chat message stored", error is None and msg is not None)
        check("customer phone redacted in body",
              "01712345678" not in msg.body and "[number removed]" in msg.body)
        check("customer phone-share NOT logged as a violation",
              PolicyViolation.query.filter_by(user_id=customer.id).count() == 0)

    # ====================================================================
    # seller in chat — strike 1 (no suspend yet)
    # ====================================================================
    with app.app_context():
        seller = db.session.get(User, ids["seller_id"])
        vendor = db.session.get(VendorProfile, ids["vendor_id"])
        thread = ChatThread.query.filter_by(
            customer_id=ids["customer_id"], vendor_id=vendor.id
        ).first()

        msg, error = post_message(
            thread, seller, "sure, my whatsapp is +8801812345678"
        )
        check("seller strike-1 message stored", error is None and msg is not None)
        check("seller strike-1 phone redacted",
              "01812345678" not in msg.body and "[number removed]" in msg.body)
        check("seller strike-1 logged as PolicyViolation",
              PolicyViolation.query.filter_by(user_id=seller.id).count() == 1)
        vendor = db.session.get(VendorProfile, ids["vendor_id"])
        check("vendor still approved after 1 violation",
              vendor.status == VENDOR_APPROVED)

    # ====================================================================
    # seller in chat — strike 2 (auto-suspend)
    # ====================================================================
    with app.app_context():
        seller = db.session.get(User, ids["seller_id"])
        vendor = db.session.get(VendorProfile, ids["vendor_id"])
        thread = ChatThread.query.filter_by(
            customer_id=ids["customer_id"], vendor_id=vendor.id
        ).first()

        before_admin_notifs = Notification.query.filter(
            Notification.kind == NOTIF_SYSTEM,
            Notification.user_id.in_(db.session.query(User.id).filter_by(role=ROLE_ADMIN)),
        ).count()
        before_seller_notifs = Notification.query.filter_by(
            user_id=seller.id, kind=NOTIF_SYSTEM
        ).count()

        msg, error = post_message(
            thread, seller, "also reach me on 0191-234-5678 thanks"
        )
        check("seller strike-2 message stored", error is None and msg is not None)
        check("seller strike-2 phone redacted",
              "01912345678" not in (msg.body or "").replace("-", "")
              and "[number removed]" in msg.body)
        check(
            "seller violations now at threshold",
            PolicyViolation.query.filter_by(user_id=seller.id).count() >= SELLER_VIOLATION_THRESHOLD,
        )

        vendor = db.session.get(VendorProfile, ids["vendor_id"])
        check("vendor auto-suspended after 2 violations",
              vendor.status == VENDOR_SUSPENDED)

        after_seller_notifs = Notification.query.filter_by(
            user_id=seller.id, kind=NOTIF_SYSTEM
        ).count()
        check("seller received suspension notification",
              after_seller_notifs > before_seller_notifs)

        after_admin_notifs = Notification.query.filter(
            Notification.kind == NOTIF_SYSTEM,
            Notification.user_id.in_(db.session.query(User.id).filter_by(role=ROLE_ADMIN)),
        ).count()
        check("admins notified of auto-suspension",
              after_admin_notifs > before_admin_notifs)

    # ====================================================================
    # customer review — phone redacted in title + comment, no log
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        product = db.session.get(Product, ids["product_id"])
        before_violations = PolicyViolation.query.filter_by(
            user_id=customer.id).count()

        rev, error = submit_review(
            customer, product, 5,
            "Call me 01711111111",
            "Comment with 01722222222 inside.",
        )
        check("customer review submitted", error is None and rev is not None)
        check("review title redacted",
              "01711111111" not in (rev.title or "")
              and "[number removed]" in (rev.title or ""))
        check("review comment redacted",
              "01722222222" not in (rev.comment or "")
              and "[number removed]" in (rev.comment or ""))
        after_violations = PolicyViolation.query.filter_by(
            user_id=customer.id).count()
        check("customer review redaction NOT logged",
              after_violations == before_violations)
        delete_review(rev)

    # ====================================================================
    # admin web flow — policy violations page + unsuspend
    # ====================================================================
    if admin_password:
        with app.test_client() as c:
            c.post("/admin/login",
                   data={"email": ADMIN_EMAIL, "password": admin_password})

            r = c.get("/admin/policy-violations/")
            check("admin policy-violations page renders",
                  r.status_code == 200 and b"Policy Violations" in r.data)
            check("policy-violations page shows the seller's email",
                  SELLER.encode() in r.data)

            r = c.get(f"/admin/vendors/{ids['vendor_id']}/")
            check("vendor_detail surfaces violation count",
                  r.status_code == 200 and b"Policy Violations" in r.data)

            r = c.post(f"/admin/vendors/{ids['vendor_id']}/unsuspend",
                       follow_redirects=False)
            check("unsuspend POST redirects", r.status_code in (302, 303))
            with app.app_context():
                vendor = db.session.get(VendorProfile, ids["vendor_id"])
                check("vendor reinstated by admin unsuspend",
                      vendor.status == VENDOR_APPROVED)
                # Seller receives a reinstatement notice
                check("seller notified of reinstatement",
                      Notification.query.filter(
                          Notification.user_id == ids["seller_id"],
                          Notification.kind == NOTIF_SYSTEM,
                          Notification.title.like("%reinstated%"),
                      ).count() >= 1)
    else:
        print("(admin password not supplied — admin web flow checks skipped)")

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-0 anti-disintermediation smoke test: "
          f"{passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
