"""Phase 9 (Chunk B) smoke test — coupons.

Covers the coupon service (validation, limits, scoping), coupon discount at
order placement, admin & seller coupon management, the web checkout flow and
the REST API.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase9_coupons.py
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
from app.models.order import Order
from app.models.marketing import (
    Coupon, CouponRedemption, COUPON_PLATFORM, COUPON_VENDOR,
    DISCOUNT_PERCENT, DISCOUNT_FIXED,
)
from app.services.coupon_service import validate_coupon
from app.services.order_service import place_order

ADMIN_EMAIL = "monirhasan2003@gmail.com"
CUSTOMER = "smoke_p9b_customer@example.com"
SELLER = "smoke_p9b_seller@example.com"
SELLER2 = "smoke_p9b_seller2@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p9b-cat"
COUPONS = ["SAVE20", "FLAT50", "BIGMIN", "EXPIRED", "ONCE", "STOREOK",
           "STOREX", "ADMINTEST", "SELLERTEST"]
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for code in COUPONS:
            c = Coupon.query.filter_by(code=code).first()
            if c:
                db.session.delete(c)        # cascades redemptions
        db.session.flush()
        for email in (CUSTOMER, SELLER, SELLER2):
            u = User.query.filter_by(email=email).first()
            if not u:
                continue
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
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


def add_cart_item(app, customer_id, product_id, qty=2):
    with app.app_context():
        db.session.add(CartItem(user_id=customer_id, product_id=product_id,
                                quantity=qty))
        db.session.commit()


def seed(app):
    with app.app_context():
        cat = Category(name_en="Smoke P9B Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P9B Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P9B Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        seller2 = User(name="P9B Seller2", email=SELLER2, role="seller", is_active=True)
        seller2.set_password(PASSWORD)
        db.session.add_all([customer, seller, seller2])
        db.session.flush()
        db.session.add(Address(user_id=customer.id, full_name="P9B Customer",
                               phone="01700000005", address_line="2 Test Rd",
                               city="Dhaka", is_default=True))
        vp = VendorProfile(user_id=seller.id, shop_name_en="P9B Store",
                           slug="p9b-store", status=VENDOR_APPROVED, commission_rate=10)
        vp2 = VendorProfile(user_id=seller2.id, shop_name_en="P9B Store 2",
                            slug="p9b-store-2", status=VENDOR_APPROVED,
                            commission_rate=10)
        db.session.add_all([vp, vp2])
        db.session.flush()
        product = Product(vendor_id=vp.id, category_id=cat.id, title_en="P9B Product",
                          slug="p9b-product", base_price=400, stock=50,
                          status=PRODUCT_PUBLISHED)
        db.session.add(product)
        db.session.flush()

        past = datetime.utcnow() - timedelta(days=2)
        db.session.add_all([
            Coupon(code="SAVE20", scope=COUPON_PLATFORM, discount_type=DISCOUNT_PERCENT,
                   discount_value=20, max_discount=100, per_user_limit=10),
            Coupon(code="FLAT50", scope=COUPON_PLATFORM, discount_type=DISCOUNT_FIXED,
                   discount_value=50, per_user_limit=10),
            Coupon(code="BIGMIN", scope=COUPON_PLATFORM, discount_type=DISCOUNT_FIXED,
                   discount_value=50, min_order_amount=99999),
            Coupon(code="EXPIRED", scope=COUPON_PLATFORM, discount_type=DISCOUNT_FIXED,
                   discount_value=50, ends_at=past),
            Coupon(code="ONCE", scope=COUPON_PLATFORM, discount_type=DISCOUNT_FIXED,
                   discount_value=30, per_user_limit=1),
            Coupon(code="STOREOK", scope=COUPON_VENDOR, vendor_id=vp.id,
                   discount_type=DISCOUNT_FIXED, discount_value=40, per_user_limit=10),
            Coupon(code="STOREX", scope=COUPON_VENDOR, vendor_id=vp2.id,
                   discount_type=DISCOUNT_FIXED, discount_value=40),
        ])
        db.session.commit()
        return {"customer_id": customer.id, "product_id": product.id,
                "vendor_id": vp.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)
    with app.app_context():
        admin_id = User.query.filter_by(email=ADMIN_EMAIL).first().id

    # ====================================================================
    # coupon service — validation rules
    # ====================================================================
    add_cart_item(app, ids["customer_id"], ids["product_id"], qty=2)  # 2 × 400 = 800
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        items = CartItem.query.filter_by(user_id=customer.id).all()

        _, disc, err = validate_coupon("SAVE20", customer, items)
        check("percent coupon respects the max-discount cap",
              err is None and disc == Decimal("100.00"))         # 20% of 800 = 160 -> 100

        _, disc, err = validate_coupon("FLAT50", customer, items)
        check("fixed coupon discounts the flat amount",
              err is None and disc == Decimal("50.00"))

        _, _, err = validate_coupon("BIGMIN", customer, items)
        check("min-order requirement enforced", err is not None)

        _, _, err = validate_coupon("EXPIRED", customer, items)
        check("expired coupon rejected", err is not None and "expired" in err)

        _, _, err = validate_coupon("BOGUSCODE", customer, items)
        check("unknown coupon rejected", err is not None)

        _, disc, err = validate_coupon("STOREOK", customer, items)
        check("vendor coupon valid for that store's items", err is None and disc > 0)

        _, _, err = validate_coupon("STOREX", customer, items)
        check("vendor coupon rejected when no matching store items",
              err is not None)

        # per-user limit — simulate a prior redemption of ONCE
        once = Coupon.query.filter_by(code="ONCE").first()
        db.session.add(CouponRedemption(coupon_id=once.id, user_id=customer.id,
                                        amount=30))
        db.session.commit()
        _, _, err = validate_coupon("ONCE", customer, items)
        check("per-user usage limit enforced", err is not None)

    # ====================================================================
    # order placement applies the coupon
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        address = Address.query.filter_by(user_id=customer.id).first()
        order = place_order(customer, address, "cod", coupon_code="SAVE20")
        check("order placed with coupon",
              order is not None and order.coupon_code == "SAVE20")
        check("order discount applied (capped at 100)",
              order.discount_amount == Decimal("100.00"))
        check("order total = subtotal + shipping - discount",
              order.total_amount == order.subtotal + order.shipping_fee
              - order.discount_amount)
        save20 = Coupon.query.filter_by(code="SAVE20").first()
        check("coupon used_count incremented", save20.used_count == 1)
        check("redemption recorded",
              CouponRedemption.query.filter_by(coupon_id=save20.id,
                                               user_id=customer.id).count() == 1)

    # ====================================================================
    # admin coupon management
    # ====================================================================
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["_user_id"] = str(admin_id)

        r = c.get("/admin/coupons/")
        check("admin coupons page lists platform coupons",
              r.status_code == 200 and b"SAVE20" in r.data)

        r = c.post("/admin/coupons/new", data={
            "code": "admintest", "discount_type": "percent", "discount_value": "15",
            "min_order_amount": "0", "per_user_limit": "1", "is_active": "on",
        }, follow_redirects=True)
        check("admin creates a coupon (code upper-cased)", b"ADMINTEST" in r.data)
        with app.app_context():
            ac = Coupon.query.filter_by(code="ADMINTEST").first()
            check("admin coupon stored as platform scope",
                  ac is not None and ac.scope == COUPON_PLATFORM)
            ac_id = ac.id

        r = c.post(f"/admin/coupons/{ac_id}/delete", follow_redirects=True)
        with app.app_context():
            check("admin deletes a coupon",
                  Coupon.query.filter_by(code="ADMINTEST").first() is None)

    # ====================================================================
    # seller coupon management
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, SELLER, "seller")
        r = c.get("/seller/coupons/")
        check("seller coupons page renders",
              r.status_code == 200 and b"Store Coupons" in r.data)

        r = c.post("/seller/coupons/new", data={
            "code": "sellertest", "discount_type": "fixed", "discount_value": "25",
            "min_order_amount": "0", "per_user_limit": "1", "is_active": "on",
        }, follow_redirects=True)
        check("seller creates a coupon", b"SELLERTEST" in r.data)
        with app.app_context():
            sc = Coupon.query.filter_by(code="SELLERTEST").first()
            check("seller coupon scoped to the vendor",
                  sc is not None and sc.scope == COUPON_VENDOR
                  and sc.vendor_id == ids["vendor_id"])

    # ====================================================================
    # web checkout flow
    # ====================================================================
    add_cart_item(app, ids["customer_id"], ids["product_id"], qty=1)  # 1 × 400
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")

        r = c.post("/cart/checkout/apply-coupon", data={"coupon_code": "FLAT50"},
                   follow_redirects=True)
        check("web apply-coupon shows the discount",
              r.status_code == 200 and b"FLAT50" in r.data)

        r = c.post("/cart/checkout/apply-coupon", data={"coupon_code": "NOPE"},
                   follow_redirects=True)
        check("web apply-coupon rejects a bad code",
              b"Invalid coupon code" in r.data)

        # re-apply a good one, then place the order
        c.post("/cart/checkout/apply-coupon", data={"coupon_code": "FLAT50"})
        with app.app_context():
            addr_id = Address.query.filter_by(user_id=ids["customer_id"]).first().id
        r = c.post("/cart/checkout/", data={"address_id": addr_id,
                                            "payment_method": "cod"},
                   follow_redirects=True)
        check("web checkout places the order", r.status_code == 200)
        with app.app_context():
            o = (Order.query.filter_by(customer_id=ids["customer_id"],
                                       coupon_code="FLAT50")
                 .order_by(Order.id.desc()).first())
            check("web order carries the coupon discount",
                  o is not None and o.discount_amount == Decimal("50.00"))

    # ====================================================================
    # REST API
    # ====================================================================
    add_cart_item(app, ids["customer_id"], ids["product_id"], qty=2)
    with app.test_client() as c:
        token = api_token(app, c, CUSTOMER)
        auth = {"Authorization": f"Bearer {token}"}

        r = c.post("/api/v1/coupons/validate", headers=auth, json={"code": "SAVE20"})
        body = r.get_json() or {}
        check("API validates a coupon",
              r.status_code == 200 and body.get("valid") is True
              and body.get("discount") == 100.0)

        r = c.post("/api/v1/coupons/validate", headers=auth, json={"code": "EXPIRED"})
        check("API reports an invalid coupon",
              (r.get_json() or {}).get("valid") is False)

        r = c.get("/api/v1/coupons", headers=auth)
        codes = {x["code"] for x in (r.get_json() or {}).get("coupons", [])}
        check("API lists active platform coupons", "SAVE20" in codes)

        with app.app_context():
            addr_id = Address.query.filter_by(user_id=ids["customer_id"]).first().id
        r = c.post("/api/v1/checkout", headers=auth,
                   json={"address_id": addr_id, "payment_method": "cod",
                         "coupon_code": "FLAT50"})
        order = (r.get_json() or {}).get("order", {})
        check("API checkout applies the coupon",
              r.status_code == 201 and order.get("coupon_code") == "FLAT50"
              and order.get("discount_amount") == 50.0)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 9 coupons smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
