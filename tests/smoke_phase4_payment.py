"""Phase 4 smoke test — payment transactions, SSLCommerz wiring, callbacks.

SSLCommerz credentials are not required: the gateway-validation step is mocked
so the callback logic can be verified. COD is tested end to end.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase4_payment.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import app.services.sslcommerz as ssl_module
from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Product, PRODUCT_PUBLISHED
from app.models.cart import CartItem
from app.models.order import Order
from app.models.payment import Transaction

CUSTOMER = "smoke_pay_customer@example.com"
results = []
_mock = {"amount": "0"}


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        u = User.query.filter_by(email=CUSTOMER).first()
        if u:
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
            CartItem.query.filter_by(user_id=u.id).delete()
            Address.query.filter_by(user_id=u.id).delete()
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)
            db.session.commit()


def otp_login(app, c):
    c.post("/login/", data={"email": CUSTOMER, "password": "test1234", "account_type": "customer"})
    with app.app_context():
        u = User.query.filter_by(email=CUSTOMER).first()
        otp = (OtpCode.query.filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
    c.post("/verify-otp/", data={"code": otp.code})


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)

    # Mock SSLCommerz validation (no sandbox credentials needed).
    ssl_module.validate_payment = lambda val_id: {
        "status": "VALID", "amount": _mock["amount"],
        "bank_tran_id": "TESTBANK01", "card_type": "VISA",
    }

    with app.app_context():
        product_id = Product.query.filter_by(status=PRODUCT_PUBLISHED).first().id

    with app.test_client() as c:
        c.post("/signup/", data={
            "first_name": "Pay", "last_name": "Tester", "email": CUSTOMER,
            "role": "customer", "password": "test1234", "confirm_password": "test1234",
        })
        otp_login(app, c)
        with app.app_context():
            cust_id = User.query.filter_by(email=CUSTOMER).first().id
        c.post("/addresses/new", data={"full_name": "Pay Tester", "phone": "01700000000",
                                       "address_line": "1 Rd", "city": "Dhaka"})
        with app.app_context():
            address_id = Address.query.filter_by(user_id=cust_id).first().id

        # ---- COD order ----
        c.post("/cart/add", data={"product_id": str(product_id), "quantity": "1"})
        r = c.post("/cart/checkout/", data={"address_id": str(address_id), "payment_method": "cod"})
        check("COD checkout -> order", r.status_code == 302)
        with app.app_context():
            cod_order = Order.query.filter_by(customer_id=cust_id).order_by(Order.id.desc()).first()
            txn = Transaction.query.filter_by(order_id=cod_order.id).first()
            check("COD transaction created (pending)",
                  txn is not None and txn.gateway == "cod" and txn.status == "pending")

        # ---- SSLCommerz order (gateway not configured -> graceful) ----
        c.post("/cart/add", data={"product_id": str(product_id), "quantity": "1"})
        r = c.post("/cart/checkout/", data={"address_id": str(address_id),
                                            "payment_method": "sslcommerz"})
        check("SSLCommerz checkout handled gracefully", r.status_code == 302)
        with app.app_context():
            ssl_order = Order.query.filter_by(customer_id=cust_id).order_by(Order.id.desc()).first()
            txn = Transaction.query.filter_by(order_id=ssl_order.id).first()
            check("SSLCommerz transaction created (initiated)",
                  txn is not None and txn.gateway == "sslcommerz" and txn.status == "initiated")
            check("Order starts unpaid", ssl_order.payment_status == "pending")
            ssl_order_number = ssl_order.order_number
            ssl_order_total = str(ssl_order.total_amount)

        # ---- success callback (mocked validation) ----
        _mock["amount"] = ssl_order_total
        r = c.post("/payment/success", data={"tran_id": ssl_order_number, "val_id": "TESTVAL01"})
        check("Success callback redirects", r.status_code == 302)
        with app.app_context():
            o = Order.query.filter_by(order_number=ssl_order_number).first()
            txn = Transaction.query.filter_by(order_id=o.id).first()
            check("Order marked paid after success", o.payment_status == "paid")
            check("Transaction marked success", txn.status == "success"
                  and txn.gateway_txn_id == "TESTVAL01")

        # ---- fail callback on a fresh SSLCommerz order ----
        c.post("/cart/add", data={"product_id": str(product_id), "quantity": "1"})
        c.post("/cart/checkout/", data={"address_id": str(address_id),
                                        "payment_method": "sslcommerz"})
        with app.app_context():
            fail_order = Order.query.filter_by(customer_id=cust_id).order_by(Order.id.desc()).first()
            fail_number = fail_order.order_number
        r = c.post("/payment/fail", data={"tran_id": fail_number})
        with app.app_context():
            o = Order.query.filter_by(order_number=fail_number).first()
            check("Fail callback marks order failed", o.payment_status == "failed")

        # ---- IPN (idempotent) on a fresh SSLCommerz order ----
        c.post("/cart/add", data={"product_id": str(product_id), "quantity": "1"})
        c.post("/cart/checkout/", data={"address_id": str(address_id),
                                        "payment_method": "sslcommerz"})
        with app.app_context():
            ipn_order = Order.query.filter_by(customer_id=cust_id).order_by(Order.id.desc()).first()
            ipn_number = ipn_order.order_number
            _mock["amount"] = str(ipn_order.total_amount)
        r = c.post("/payment/ipn", data={"tran_id": ipn_number, "val_id": "TESTVAL02"})
        check("IPN returns 200", r.status_code == 200)
        with app.app_context():
            o = Order.query.filter_by(order_number=ipn_number).first()
            check("IPN marks order paid", o.payment_status == "paid")

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 4 payment smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
