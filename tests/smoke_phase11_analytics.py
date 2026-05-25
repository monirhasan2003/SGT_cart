"""Phase 11 smoke test — analytics, low-stock alerts, scheduled payouts.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase11_analytics.py
"""
import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.cart import CartItem
from app.models.order import Order, SubOrder, SUBORDER_DELIVERED
from app.models.wallet import PayoutRequest, PAYOUT_REQUESTED, PAYOUT_APPROVED
from app.models.notification import Notification, NOTIF_PRODUCT
from app.models.marketing import RewardLedger
from app.models.analytics import ProductView
from app.services.order_service import place_order, update_suborder_status
from app.services.analytics_service import (
    seller_metrics, platform_metrics, LOW_STOCK_THRESHOLD,
)
from app.services.payout_service import process_due_payouts

ADMIN_EMAIL = "monirhasan2003@gmail.com"
CUSTOMER = "smoke_p11_customer@example.com"
SELLER = "smoke_p11_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p11-cat"
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
            RewardLedger.query.filter_by(user_id=u.id).delete()
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                PayoutRequest.query.filter_by(vendor_id=vp.id).delete()
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    ProductView.query.filter_by(product_id=p.id).delete()
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
    """Customer + delivered order so analytics have something to report."""
    with app.app_context():
        cat = Category(name_en="Smoke P11 Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P11 Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P11 Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        db.session.add(Address(user_id=customer.id, full_name="P11 Customer",
                               phone="01700000009", address_line="6 Test St",
                               city="Dhaka", is_default=True))
        vp = VendorProfile(user_id=seller.id, shop_name_en="P11 Store",
                           slug="p11-store", status=VENDOR_APPROVED, commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        # Stock = LOW_STOCK_THRESHOLD + 2 so the first order crosses the threshold.
        product = Product(vendor_id=vp.id, category_id=cat.id, title_en="P11 Product",
                          slug="p11-product", base_price=500,
                          stock=LOW_STOCK_THRESHOLD + 2, status=PRODUCT_PUBLISHED)
        db.session.add(product)
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id, "product_id": product.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)
    with app.app_context():
        admin_id = User.query.filter_by(email=ADMIN_EMAIL).first().id

    # ====================================================================
    # low-stock alert on order placement
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        product = db.session.get(Product, ids["product_id"])
        address = Address.query.filter_by(user_id=customer.id).first()
        before_stock = product.stock
        db.session.add(CartItem(user_id=customer.id, product_id=product.id, quantity=3))
        db.session.commit()
        place_order(customer, address, "cod")
        product = db.session.get(Product, ids["product_id"])
        check("order placement decrements product stock",
              product.stock == before_stock - 3)
        check("low-stock alert raised for the seller when crossing the threshold",
              Notification.query.filter_by(user_id=ids["seller_id"],
                                           kind=NOTIF_PRODUCT)
              .filter(Notification.title.like("Low stock%")).count() == 1)

        # Deliver so revenue / commission count in analytics.
        sub = SubOrder.query.filter(
            SubOrder.vendor_id == ids["vendor_id"]
        ).order_by(SubOrder.id.desc()).first()
        update_suborder_status(sub, SUBORDER_DELIVERED)
        db.session.commit()

    # ====================================================================
    # seller_metrics
    # ====================================================================
    with app.app_context():
        vp = db.session.get(VendorProfile, ids["vendor_id"])
        m = seller_metrics(vp, days=30)
        check("seller revenue includes the new delivered order",
              m["total_revenue"] >= 1500)              # 3 × 500
        check("seller orders count is 1", m["total_orders"] == 1)
        check("daily_series has 30 entries", len(m["daily_series"]) == 30)
        check("top_products lists the test product",
              m["top_products"] and m["top_products"][0]["qty"] == 3)
        check("top_categories lists the test category",
              m["top_categories"] and m["top_categories"][0]["category"] == "Smoke P11 Cat")
        check("revenue forecast is positive", m["forecast_7d_revenue"] > 0)

    # ====================================================================
    # platform_metrics
    # ====================================================================
    with app.app_context():
        m = platform_metrics(days=30)
        check("platform metrics includes GMV", m["gmv"] >= 1500)
        check("platform metrics tracks commission earned",
              m["commission_earned"] > 0)
        check("platform top_sellers lists this shop",
              any(s["shop"] == "P11 Store" for s in m["top_sellers"]))

    # ====================================================================
    # scheduled payouts
    # ====================================================================
    with app.app_context():
        # One old (auto-approvable), one fresh (must stay pending).
        old = PayoutRequest(vendor_id=ids["vendor_id"], amount=Decimal("100"),
                            method="bkash", account_detail="01700000009",
                            status=PAYOUT_REQUESTED)
        old.requested_at = datetime.utcnow() - timedelta(hours=48)
        recent = PayoutRequest(vendor_id=ids["vendor_id"], amount=Decimal("50"),
                               method="bkash", account_detail="01700000009",
                               status=PAYOUT_REQUESTED)
        db.session.add_all([old, recent])
        db.session.commit()
        old_id, recent_id = old.id, recent.id

    with app.app_context():
        approved = process_due_payouts()
        check("scheduled payouts approve old requests",
              approved >= 1
              and db.session.get(PayoutRequest, old_id).status == PAYOUT_APPROVED)
        check("scheduled payouts skip recent requests",
              db.session.get(PayoutRequest, recent_id).status == PAYOUT_REQUESTED)

    # ====================================================================
    # admin web — reports page + run-scheduled-payouts button
    # ====================================================================
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["_user_id"] = str(admin_id)

        r = c.get("/admin/reports/")
        check("admin reports page renders",
              r.status_code == 200 and b"GMV" in r.data
              and b"Top sellers" in r.data)

        r = c.post("/admin/payouts/run-scheduled", follow_redirects=True)
        check("admin can run scheduled payouts from the UI",
              r.status_code == 200 and b"Scheduled payouts run" in r.data)

    # ====================================================================
    # seller web + API
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, SELLER, "seller")
        r = c.get("/seller/analytics/")
        check("seller analytics page renders",
              r.status_code == 200 and b"Sales Analytics" in r.data
              and b"P11 Product" in r.data)

    with app.test_client() as c:
        token = api_token(app, c, SELLER)
        r = c.get("/api/v1/seller/analytics?days=30",
                  headers={"Authorization": f"Bearer {token}"})
        body = r.get_json() or {}
        check("API seller analytics returns metrics",
              r.status_code == 200
              and body.get("total_revenue", 0) >= 1500
              and "daily_series" in body
              and "forecast_7d_revenue" in body)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 11 analytics smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
