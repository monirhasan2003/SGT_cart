"""Phase 3 smoke test — seller order fulfilment + admin order oversight.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase3_orders.py <admin_password>
"""
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.cart import CartItem
from app.models.order import Order, SubOrder
from app.models.marketing import RewardLedger
from app.services.order_service import place_order

ADMIN_EMAIL = "monirhasan2003@gmail.com"
CUSTOMER = "smoke_ord_customer@example.com"
SELLER_B = "smoke_ord_sellerb@example.com"
SELLER_C = "smoke_ord_sellerc@example.com"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        cust = User.query.filter_by(email=CUSTOMER).first()
        if cust:
            RewardLedger.query.filter_by(user_id=cust.id).delete()
            for o in Order.query.filter_by(customer_id=cust.id).all():
                db.session.delete(o)
            CartItem.query.filter_by(user_id=cust.id).delete()
            Address.query.filter_by(user_id=cust.id).delete()
            OtpCode.query.filter_by(user_id=cust.id).delete()
            db.session.delete(cust)
            db.session.commit()
        for email in (SELLER_B, SELLER_C):
            u = User.query.filter_by(email=email).first()
            if u:
                OtpCode.query.filter_by(user_id=u.id).delete()
                db.session.delete(u)
                db.session.commit()


def seller_login(app, c, email):
    c.post("/login/", data={"email": email, "password": "test1234", "account_type": "seller"})
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query.filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
    c.post("/verify-otp/", data={"code": otp.code})


def main():
    admin_password = sys.argv[1] if len(sys.argv) > 1 else ""
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)

    # --- setup: customer + order, seller B (has the order), seller C (unrelated) ---
    with app.app_context():
        cust = User(name="Order Buyer", email=CUSTOMER, role="customer",
                    is_active=True, is_email_verified=True)
        cust.set_password("test1234")
        db.session.add(cust)
        db.session.flush()
        addr = Address(user_id=cust.id, full_name="Order Buyer", phone="01700000000",
                       address_line="1 Test Road", city="Dhaka", is_default=True)
        db.session.add(addr)

        sbu = User(name="Order Seller B", email=SELLER_B, role="seller",
                   is_active=True, is_email_verified=True)
        sbu.set_password("test1234")
        db.session.add(sbu)
        db.session.flush()
        vb = VendorProfile(user_id=sbu.id, shop_name_en="Order Shop B", slug="order-shop-b",
                           status=VENDOR_APPROVED, commission_rate=Decimal("10.00"))
        db.session.add(vb)
        db.session.flush()
        cat_id = Category.query.first().id
        pb = Product(vendor_id=vb.id, category_id=cat_id, title_en="Order Product B",
                     slug="order-product-b", base_price=Decimal("300.00"),
                     stock=50, status=PRODUCT_PUBLISHED)
        db.session.add(pb)
        db.session.flush()
        db.session.add(CartItem(user_id=cust.id, product_id=pb.id, quantity=2))
        db.session.commit()

        order = place_order(cust, addr, "cod")
        suborder_id = order.suborders[0].id
        order_number = order.order_number

        scu = User(name="Order Seller C", email=SELLER_C, role="seller",
                   is_active=True, is_email_verified=True)
        scu.set_password("test1234")
        db.session.add(scu)
        db.session.flush()
        db.session.add(VendorProfile(user_id=scu.id, shop_name_en="Order Shop C",
                                     slug="order-shop-c", status=VENDOR_APPROVED))
        db.session.commit()

    # --- seller B fulfils the order ---
    with app.test_client() as c:
        seller_login(app, c, SELLER_B)

        r = c.get("/seller/orders/")
        check("Seller sees their orders",
              r.status_code == 200 and order_number.encode() in r.data)

        r = c.get(f"/seller/orders/{suborder_id}/")
        check("Seller order detail", r.status_code == 200
              and b"Your earning" in r.data)

        r = c.post(f"/seller/orders/{suborder_id}/status", data={"status": "shipped"})
        with app.app_context():
            check("Seller updates status -> shipped",
                  db.session.get(SubOrder, suborder_id).status == "shipped")

    # --- seller C must NOT access seller B's sub-order ---
    with app.test_client() as c:
        seller_login(app, c, SELLER_C)
        r = c.get(f"/seller/orders/{suborder_id}/")
        check("Other seller blocked from this order", r.status_code == 403)
        r = c.get("/seller/orders/")
        check("Other seller has no orders",
              r.status_code == 200 and order_number.encode() not in r.data)

    # --- admin oversight ---
    with app.test_client() as c:
        c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})
        r = c.get("/admin/orders/")
        check("Admin orders list", r.status_code == 200 and order_number.encode() in r.data)
        r = c.get(f"/admin/orders/{order_number}/")
        check("Admin order detail (commission visible)",
              r.status_code == 200 and b"Commission" in r.data
              and b"Vendor earning" in r.data)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 3 orders smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
