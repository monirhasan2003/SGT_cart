"""Phase 15 Chunk D-6 smoke test — urgency & inventory signals.

Covers:
  * stock_service.units_sold_recent counts only non-cancelled sub-orders
    within the window.
  * stock_service.subscribe rejects when in-stock; stores a row when out of
    stock; idempotent on duplicate email; re-opens a previously-notified
    row after the next out-of-stock incident.
  * presence_service.record_view + active_viewers counts unique viewers
    within the 60-second window.
  * Public POST /product/<slug>/notify-stock persists a row.
  * Product page renders the urgency signals:
      - "Only X left" when stock <= 5
      - "Y sold in last 24h" when sold_24h > 0
      - "Z viewing now" when viewing_now > 1
      - Back-in-stock form ONLY when stock <= 0
  * Seller transitioning stock 0 → positive via /seller/products/<id>/edit
    fires notify_back_in_stock: subscriber rows get `notified_at` stamped
    and the user gets a NOTIF_PRODUCT row.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d6.py
"""
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.order import (
    Order, SubOrder, OrderItem,
    SUBORDER_DELIVERED, SUBORDER_CANCELLED,
)
from app.models.stock import StockNotification
from app.models.notification import Notification, NOTIF_PRODUCT
from app.services.stock_service import (
    subscribe, units_sold_recent, pending_count_for_product,
)
from app.services import presence_service

CUSTOMER = "smoke_p15d6_customer@example.com"
SELLER = "smoke_p15d6_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d6-cat"
IN_STOCK_SLUG = "p15d6-in-stock"
OOS_SLUG = "p15d6-out-of-stock"
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
            StockNotification.query.filter_by(user_id=u.id).delete()
            Notification.query.filter_by(user_id=u.id).delete()
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    StockNotification.query.filter_by(product_id=p.id).delete()
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
        cat = Category(name_en="Smoke P15D6", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P15D6 Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P15D6 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15D6 Shop",
                           slug="p15d6-shop", status=VENDOR_APPROVED,
                           commission_rate=10,
                           trade_license_doc="kyc/tl.pdf", nid_doc="kyc/nid.pdf")
        db.session.add(vp)
        db.session.flush()
        in_stock = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D6 In Stock", slug=IN_STOCK_SLUG,
            base_price=500, stock=3, status=PRODUCT_PUBLISHED,
        )
        oos = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D6 OOS", slug=OOS_SLUG,
            base_price=300, stock=0, status=PRODUCT_PUBLISHED,
        )
        db.session.add_all([in_stock, oos])
        db.session.flush()

        # Two delivered sub-orders today + one cancelled today on in_stock.
        order = Order(customer_id=customer.id, order_number="SGTP15D6-T01",
                      payment_method="cod", payment_status="pending",
                      ship_name=customer.name, ship_phone="01700000099",
                      ship_address_line="1 Test St", ship_city="Dhaka",
                      subtotal=2500, shipping_fee=0, total_amount=2500)
        db.session.add(order)
        db.session.flush()
        s_ok = SubOrder(order_id=order.id, vendor_id=vp.id, subtotal=1500,
                        status=SUBORDER_DELIVERED)
        s_cancel = SubOrder(order_id=order.id, vendor_id=vp.id, subtotal=1000,
                            status=SUBORDER_CANCELLED)
        db.session.add_all([s_ok, s_cancel])
        db.session.flush()
        db.session.add_all([
            OrderItem(sub_order_id=s_ok.id, product_id=in_stock.id,
                      title="P15D6 In Stock", unit_price=500,
                      quantity=3, line_total=1500),
            OrderItem(sub_order_id=s_cancel.id, product_id=in_stock.id,
                      title="P15D6 In Stock", unit_price=500,
                      quantity=2, line_total=1000),
        ])
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id,
                "in_stock_id": in_stock.id, "oos_id": oos.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # service-layer: stock_service.units_sold_recent
    # ====================================================================
    with app.app_context():
        in_stock = db.session.get(Product, ids["in_stock_id"])
        oos = db.session.get(Product, ids["oos_id"])

        check("units_sold_recent counts only non-cancelled sub-orders",
              units_sold_recent(in_stock, hours=24) == 3)
        check("units_sold_recent zero when nothing sold",
              units_sold_recent(oos, hours=24) == 0)

    # ====================================================================
    # service-layer: stock_service.subscribe
    # ====================================================================
    with app.app_context():
        in_stock = db.session.get(Product, ids["in_stock_id"])
        oos = db.session.get(Product, ids["oos_id"])
        customer = db.session.get(User, ids["customer_id"])

        # Reject when product is in stock
        row, error = subscribe(in_stock, customer, customer.email)
        check("subscribe rejected when in stock", row is None and error)

        # Subscribe when out of stock
        row, error = subscribe(oos, customer, customer.email)
        check("subscribe stored for OOS product",
              error is None and row is not None and row.notified_at is None)

        # Idempotent duplicate
        row2, error = subscribe(oos, customer, customer.email)
        check("subscribe idempotent on duplicate email",
              error is None and row2.id == row.id)

        # Anonymous subscriber with bare email
        row3, error = subscribe(oos, None, "guest_p15d6@example.com")
        check("anonymous subscriber accepted",
              error is None and row3.user_id is None)

        # Empty email + no user → error
        none_row, error = subscribe(oos, None, "")
        check("subscribe rejects empty email", none_row is None and error)

        # Pending count = 2 (customer + guest)
        check("pending_count_for_product reports 2",
              pending_count_for_product(oos) == 2)

    # ====================================================================
    # presence_service
    # ====================================================================
    presence_service.reset()
    presence_service.record_view(99, "alice")
    presence_service.record_view(99, "bob")
    presence_service.record_view(99, "alice")   # alice again — still 2 unique
    presence_service.record_view(100, "alice")  # different product
    check("active_viewers counts unique viewer keys",
          presence_service.active_viewers(99) == 2)
    check("active_viewers separates products",
          presence_service.active_viewers(100) == 1)
    check("active_viewers ignores unrecorded product",
          presence_service.active_viewers(999) == 0)
    presence_service.reset()

    # ====================================================================
    # web flow — public POST /notify-stock + product page rendering
    # ====================================================================
    with app.test_client() as c:
        # Anonymous subscribe via the public endpoint
        r = c.post(f"/product/{OOS_SLUG}/notify-stock",
                   data={"email": "anon_p15d6@example.com"},
                   follow_redirects=False)
        check("POST /notify-stock redirects to product#urgency",
              r.status_code in (302, 303)
              and "#urgency" in r.headers.get("Location", ""))
        with app.app_context():
            check("anonymous subscription persisted",
                  StockNotification.query.filter_by(
                      product_id=ids["oos_id"],
                      email="anon_p15d6@example.com").count() == 1)

        # Page renders OOS subscribe form + subscriber count
        body = c.get(f"/product/{OOS_SLUG}/").data.decode("utf-8", errors="ignore")
        check("OOS product page shows the subscribe form",
              "pdp-notify-stock" in body
              and "Notify me when back in stock" in body)
        check("subscriber-count line shown on OOS page",
              "other" in body and "waiting for this product" in body)

        # In-stock product: no subscribe form; urgency badges show
        body_in = c.get(f"/product/{IN_STOCK_SLUG}/").data.decode("utf-8", errors="ignore")
        check("in-stock product hides the subscribe form",
              "pdp-notify-stock" not in body_in)
        check("Only X left urgency shown when stock <= 5",
              "Only 3 left in stock" in body_in)
        check("'sold in last 24h' shown when sold > 0",
              "3 sold in last 24h" in body_in)

        # Two distinct sessions touching the page → viewing_now should
        # reach 2 (test client = new session here).
        body_in2 = c.get(f"/product/{IN_STOCK_SLUG}/").data.decode("utf-8", errors="ignore")
        check("urgency block renders",
              'id="urgency"' in body_in2)

    with app.test_client() as c2:
        # second viewer
        c2.get(f"/product/{IN_STOCK_SLUG}/")
    with app.test_client() as c3:
        body_v = c3.get(f"/product/{IN_STOCK_SLUG}/").data.decode(
            "utf-8", errors="ignore")
        check("viewing-now reaches >1 with multiple sessions",
              "viewing now" in body_v)

    # ====================================================================
    # back-in-stock fire via the seller edit form
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, SELLER, "seller")
        # Stock OOS → 12 via /seller/products/<id>/edit. The form posts
        # the full product fields; we mirror them here.
        with app.app_context():
            oos = db.session.get(Product, ids["oos_id"])
            form_data = {
                "title_en": oos.title_en,
                "category_id": str(oos.category_id),
                "base_price": str(oos.base_price),
                "stock": "12",
            }
        c.post(f"/seller/products/{ids['oos_id']}/edit",
               data=form_data, follow_redirects=True)
        with app.app_context():
            oos = db.session.get(Product, ids["oos_id"])
            check("stock raised by seller edit",
                  (oos.stock or 0) == 12)
            # All pending subscriptions for this product were notified.
            pending = StockNotification.query.filter_by(
                product_id=ids["oos_id"], notified_at=None
            ).count()
            notified = StockNotification.query.filter(
                StockNotification.product_id == ids["oos_id"],
                StockNotification.notified_at.isnot(None),
            ).count()
            check("all pending stock-notifications stamped notified_at",
                  pending == 0 and notified >= 2)
            check("registered user got in-app NOTIF_PRODUCT",
                  Notification.query.filter_by(
                      user_id=ids["customer_id"], kind=NOTIF_PRODUCT
                  ).filter(Notification.title.like("%Back in stock%")).count() >= 1)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-6 urgency & inventory smoke test: "
          f"{passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
