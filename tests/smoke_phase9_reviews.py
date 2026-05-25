"""Phase 9 (Chunk A) smoke test — product reviews (verified purchase).

Covers the review service, rating aggregates, the REST API, the web review
flow and the seller reviews page.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase9_reviews.py
"""
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.order import Order, SubOrder, OrderItem, SUBORDER_DELIVERED
from app.models.review import Review
from app.services.review_service import (
    can_review, submit_review, delete_review, reviewable_products,
)

CUSTOMER = "smoke_p9a_customer@example.com"
SELLER = "smoke_p9a_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p9a-cat"
ORDER_NO = "SGTP9A-TEST01"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        users = [u for u in
                 (User.query.filter_by(email=e).first() for e in (CUSTOMER, SELLER))
                 if u is not None]
        # Reviews reference users — clear them before deleting the rows.
        for u in users:
            for rv in Review.query.filter_by(user_id=u.id).all():
                db.session.delete(rv)
        for u in users:
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
    """A customer with a DELIVERED order for product A, plus an un-ordered B."""
    with app.app_context():
        cat = Category(name_en="Smoke P9A Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P9A Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P9A Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P9A Smoke Store",
                           slug="p9a-smoke-store", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        prod_a = Product(vendor_id=vp.id, category_id=cat.id, title_en="P9A Product A",
                         slug="p9a-product-a", base_price=400, stock=5,
                         status=PRODUCT_PUBLISHED)
        prod_b = Product(vendor_id=vp.id, category_id=cat.id, title_en="P9A Product B",
                         slug="p9a-product-b", base_price=200, stock=5,
                         status=PRODUCT_PUBLISHED)
        db.session.add_all([prod_a, prod_b])
        db.session.flush()

        # A delivered order containing product A only.
        order = Order(customer_id=customer.id, order_number=ORDER_NO,
                      payment_method="cod", payment_status="pending",
                      ship_name="P9A Customer", ship_phone="01700000004",
                      ship_address_line="1 Test St", ship_city="Dhaka",
                      subtotal=400, shipping_fee=0, total_amount=400)
        db.session.add(order)
        db.session.flush()
        sub = SubOrder(order_id=order.id, vendor_id=vp.id, subtotal=400,
                       status=SUBORDER_DELIVERED)
        db.session.add(sub)
        db.session.flush()
        db.session.add(OrderItem(sub_order_id=sub.id, product_id=prod_a.id,
                                 title="P9A Product A", unit_price=400,
                                 quantity=1, line_total=400))
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id, "prod_a": prod_a.id, "prod_b": prod_b.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # service layer — eligibility & aggregates
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        prod_a = db.session.get(Product, ids["prod_a"])
        prod_b = db.session.get(Product, ids["prod_b"])

        check("can review a delivered product", can_review(customer, prod_a))
        check("cannot review an un-ordered product", not can_review(customer, prod_b))

        rev, error = submit_review(customer, prod_b, 5, "x", "y")
        check("submit_review blocked without delivery", rev is None and error is not None)

        rev, error = submit_review(customer, prod_a, 4, "Good", "Works well")
        check("submit_review succeeds for delivered product",
              error is None and rev is not None)

        prod_a = db.session.get(Product, ids["prod_a"])
        check("product rating aggregate updated",
              prod_a.rating_count == 1 and prod_a.rating_avg == Decimal("4.00"))
        vp = db.session.get(VendorProfile, ids["vendor_id"])
        check("vendor rating aggregate updated",
              vp.rating_count == 1 and vp.rating_avg == Decimal("4.00"))

        # re-submitting updates the same review (no duplicate)
        rev2, _ = submit_review(customer, prod_a, 2, "Changed mind", "Meh")
        check("re-submit updates the existing review (no duplicate)",
              Review.query.filter_by(user_id=customer.id,
                                     product_id=prod_a.id).count() == 1)
        prod_a = db.session.get(Product, ids["prod_a"])
        check("aggregate reflects the updated rating",
              prod_a.rating_avg == Decimal("2.00"))

        check("reviewable_products excludes the already-reviewed product",
              prod_a.id not in {p.id for p in reviewable_products(customer)})

        delete_review(rev2)
        prod_a = db.session.get(Product, ids["prod_a"])
        check("delete_review resets the aggregate",
              prod_a.rating_count == 0 and prod_a.rating_avg == Decimal("0.00"))

    # ====================================================================
    # REST API
    # ====================================================================
    with app.test_client() as c:
        token = api_token(app, c, CUSTOMER)
        auth = {"Authorization": f"Bearer {token}"}
        check("customer API token obtained", bool(token))

        # public listing
        r = c.get("/api/v1/products/p9a-product-a/reviews")
        check("GET /products/<slug>/reviews (public)",
              r.status_code == 200 and "reviews" in (r.get_json() or {}))

        # blocked without a delivered purchase
        r = c.post("/api/v1/products/p9a-product-b/reviews", headers=auth,
                   json={"rating": 5, "comment": "nice"})
        check("API review blocked without delivery (403)", r.status_code == 403)

        # allowed for the delivered product
        r = c.post("/api/v1/products/p9a-product-a/reviews", headers=auth,
                   json={"rating": 5, "title": "Excellent", "comment": "Loved it"})
        check("API review accepted for delivered product",
              r.status_code == 201
              and (r.get_json() or {}).get("review", {}).get("rating") == 5)

        r = c.get("/api/v1/products/p9a-product-a/reviews")
        body = r.get_json() or {}
        check("review appears in the public listing",
              body.get("rating_count") == 1 and len(body.get("reviews", [])) == 1)

        r = c.get("/api/v1/reviews/mine", headers=auth)
        check("GET /reviews/mine", r.status_code == 200
              and len((r.get_json() or {}).get("reviews", [])) == 1)

        r = c.get("/api/v1/reviews/reviewable", headers=auth)
        slugs = {p["slug"] for p in (r.get_json() or {}).get("products", [])}
        check("reviewable list excludes the reviewed product",
              "p9a-product-a" not in slugs)

        # rating shows up on the product card
        r = c.get("/api/v1/products/p9a-product-a")
        check("product detail carries the rating",
              (r.get_json() or {}).get("product", {}).get("rating") == 5.0)

    # remove the API review so the web flow starts clean
    with app.app_context():
        rv = Review.query.filter_by(user_id=ids["customer_id"],
                                    product_id=ids["prod_a"]).first()
        if rv:
            delete_review(rv)

    # ====================================================================
    # web flow
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")

        r = c.get("/reviews/")
        check("web My Reviews page renders",
              r.status_code == 200 and b"Waiting for your review" in r.data)

        r = c.get("/reviews/write/p9a-product-a")
        check("web review form renders", r.status_code == 200 and b"Your rating" in r.data)

        r = c.post("/reviews/write/p9a-product-a",
                   data={"rating": "5", "title": "Web review", "comment": "Great"},
                   follow_redirects=True)
        check("web review submitted", r.status_code == 200)
        with app.app_context():
            check("web review stored + aggregate updated",
                  db.session.get(Product, ids["prod_a"]).rating_count == 1)

        # blocked from reviewing an un-ordered product (redirected away from the form)
        r = c.get("/reviews/write/p9a-product-b")
        check("web blocks review of an un-ordered product",
              r.status_code == 302
              and "p9a-product-b" in r.headers.get("Location", ""))

        # product page shows the review + rating
        r = c.get("/product/p9a-product-a/")
        check("product page shows the rating & review",
              r.status_code == 200 and b"Web review" in r.data
              and b"Verified Purchase" in r.data)

    # ====================================================================
    # seller reviews page
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, SELLER, "seller")
        r = c.get("/seller/reviews/")
        check("seller reviews page lists the review",
              r.status_code == 200 and b"Web review" in r.data)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 9 reviews smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
