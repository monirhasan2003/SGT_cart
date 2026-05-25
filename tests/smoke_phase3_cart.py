"""Phase 3 smoke test — DB-backed shopping cart.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase3_cart.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Product, PRODUCT_PUBLISHED
from app.models.cart import CartItem

CUSTOMER = "smoke_cart_customer@example.com"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        u = User.query.filter_by(email=CUSTOMER).first()
        if u:
            CartItem.query.filter_by(user_id=u.id).delete()
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)
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

    with app.app_context():
        product = Product.query.filter_by(status=PRODUCT_PUBLISHED).first()
        product_id = product.id
        product_title = product.title_en

    # anonymous cannot view the cart
    with app.test_client() as anon:
        r = anon.get("/cart/")
        check("Anonymous cart -> login redirect", r.status_code == 302)

    with app.test_client() as c:
        c.post("/signup/", data={
            "first_name": "Cart", "last_name": "Tester", "email": CUSTOMER,
            "role": "customer", "password": "test1234", "confirm_password": "test1234",
        })
        otp_login(app, c, CUSTOMER)

        r = c.get("/cart/")
        check("Empty cart page", r.status_code == 200 and b"cart is empty" in r.data)

        # add to cart
        r = c.post("/cart/add", data={"product_id": str(product_id), "quantity": "1"})
        check("Add to cart", r.status_code == 302 and "/cart/" in r.headers.get("Location", ""))
        with app.app_context():
            u = User.query.filter_by(email=CUSTOMER).first()
            items = CartItem.query.filter_by(user_id=u.id).all()
            check("Cart item created", len(items) == 1 and items[0].quantity == 1)
            uid = u.id

        r = c.get("/cart/")
        check("Cart page shows product", r.status_code == 200
              and product_title.encode() in r.data)

        # adding the same product merges quantity
        c.post("/cart/add", data={"product_id": str(product_id), "quantity": "2"})
        with app.app_context():
            items = CartItem.query.filter_by(user_id=uid).all()
            check("Same product merges quantity", len(items) == 1 and items[0].quantity == 3)
            item_id = items[0].id

        # update quantity
        c.post("/cart/update", data={"item_id": str(item_id), "quantity": "5"})
        with app.app_context():
            check("Update quantity", db.session.get(CartItem, item_id).quantity == 5)

        # remove
        c.post("/cart/remove", data={"item_id": str(item_id)})
        with app.app_context():
            check("Remove item", db.session.get(CartItem, item_id) is None)

        # checkout placeholder with empty cart -> redirect
        r = c.get("/cart/checkout/")
        check("Checkout (empty cart) redirects", r.status_code == 302)

    purge(app)
    print("(test customer cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 3 cart smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
