"""Phase 3 smoke test — checkout, multi-vendor order split, commission, COD.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase3_checkout.py
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
from app.models.order import Order, SubOrder, OrderItem

CUSTOMER = "smoke_checkout_customer@example.com"
SELLER_B = "smoke_checkout_sellerb@example.com"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        cust = User.query.filter_by(email=CUSTOMER).first()
        if cust:
            for o in Order.query.filter_by(customer_id=cust.id).all():
                db.session.delete(o)
            CartItem.query.filter_by(user_id=cust.id).delete()
            Address.query.filter_by(user_id=cust.id).delete()
            OtpCode.query.filter_by(user_id=cust.id).delete()
            db.session.delete(cust)
            db.session.commit()
        sb = User.query.filter_by(email=SELLER_B).first()
        if sb:
            OtpCode.query.filter_by(user_id=sb.id).delete()
            db.session.delete(sb)  # cascades vendor -> products
            db.session.commit()


def otp_login(app, c, email):
    c.post("/login/", data={"email": email, "password": "test1234", "account_type": "customer"})
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query.filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
    c.post("/verify-otp/", data={"code": otp.code})


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)

    # --- setup: vendor A (demo store product) + vendor B (created here) ---
    with app.app_context():
        product_a = Product.query.filter_by(status=PRODUCT_PUBLISHED).first()
        product_a_id = product_a.id
        price_a = Decimal(product_a.current_price)

        sb = User(name="Checkout Seller B", email=SELLER_B, role="seller",
                  is_active=True, is_email_verified=True)
        sb.set_password("test1234")
        db.session.add(sb)
        db.session.flush()
        vb = VendorProfile(user_id=sb.id, shop_name_en="Checkout Shop B",
                           slug="checkout-shop-b", status=VENDOR_APPROVED,
                           commission_rate=Decimal("15.00"))
        db.session.add(vb)
        db.session.flush()
        category_id = Category.query.first().id
        pb = Product(vendor_id=vb.id, category_id=category_id, title_en="Checkout Product B",
                     slug="checkout-product-b", base_price=Decimal("500.00"),
                     stock=100, status=PRODUCT_PUBLISHED)
        db.session.add(pb)
        db.session.commit()
        product_b_id = pb.id

    with app.test_client() as c:
        c.post("/signup/", data={
            "first_name": "Checkout", "last_name": "Buyer", "email": CUSTOMER,
            "role": "customer", "password": "test1234", "confirm_password": "test1234",
        })
        otp_login(app, c, CUSTOMER)

        # add one product from each vendor
        c.post("/cart/add", data={"product_id": str(product_a_id), "quantity": "1"})
        c.post("/cart/add", data={"product_id": str(product_b_id), "quantity": "2"})

        # add a delivery address
        c.post("/addresses/new", data={
            "full_name": "Checkout Buyer", "phone": "01700000000",
            "address_line": "10 Test Road", "city": "Dhaka",
        })
        with app.app_context():
            cust = User.query.filter_by(email=CUSTOMER).first()
            address_id = Address.query.filter_by(user_id=cust.id).first().id
            cust_id = cust.id

        # checkout page shows both shops
        r = c.get("/cart/checkout/")
        check("Checkout page (2 vendors)",
              r.status_code == 200 and b"Checkout Shop B" in r.data
              and b"Sold by" in r.data)

        # place the order
        r = c.post("/cart/checkout/", data={"address_id": str(address_id),
                                            "payment_method": "cod"})
        check("Order placed -> redirect to detail",
              r.status_code == 302 and "/my-orders/" in r.headers.get("Location", ""))

        with app.app_context():
            order = Order.query.filter_by(customer_id=cust_id).first()
            check("One Order created", order is not None)
            subs = SubOrder.query.filter_by(order_id=order.id).all() if order else []
            check("Order split into 2 sub-orders (per vendor)", len(subs) == 2)

            items = []
            for s in subs:
                items += OrderItem.query.filter_by(sub_order_id=s.id).all()
            check("Order has 2 line items", len(items) == 2)

            # vendor B sub-order: subtotal 1000, commission 15% = 150, earning 850
            sub_b = next((s for s in subs if s.commission_rate == Decimal("15.00")), None)
            check("Vendor B sub-order present", sub_b is not None)
            if sub_b:
                check("Vendor B subtotal = 1000",
                      sub_b.subtotal == Decimal("1000.00"), str(sub_b.subtotal))
                check("Vendor B commission = 150 (15%)",
                      sub_b.commission_amount == Decimal("150.00"), str(sub_b.commission_amount))
                check("Vendor B earning = 850",
                      sub_b.vendor_earning == Decimal("850.00"), str(sub_b.vendor_earning))

            # order totals: subtotal = price_a + 1000, shipping = 60 * 2
            expected_subtotal = price_a + Decimal("1000.00")
            check("Order subtotal correct",
                  order.subtotal == expected_subtotal, str(order.subtotal))
            check("Shipping = 60 x 2 vendors",
                  order.shipping_fee == Decimal("120.00"), str(order.shipping_fee))
            check("Order total = subtotal + shipping",
                  order.total_amount == expected_subtotal + Decimal("120.00"))
            check("Payment is COD / pending",
                  order.payment_method == "cod" and order.payment_status == "pending")
            order_number = order.order_number

            check("Cart cleared after checkout",
                  CartItem.query.filter_by(user_id=cust_id).count() == 0)

        # order pages render
        r = c.get(f"/my-orders/{order_number}/")
        check("Order detail page", r.status_code == 200 and order_number.encode() in r.data)
        r = c.get("/my-orders/")
        check("My Orders list", r.status_code == 200 and order_number.encode() in r.data)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 3 checkout smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
