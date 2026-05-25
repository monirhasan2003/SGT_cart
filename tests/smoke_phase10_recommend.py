"""Phase 10 (Chunk B) smoke test — product recommendations.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase10_recommend.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.analytics import ProductView
from app.services.recommendation_service import (
    similar_products, also_viewed, for_you, best_sellers,
)

CUSTOMER = "smoke_p10r_customer@example.com"
VIEWER = "smoke_p10r_viewer@example.com"
SELLER = "smoke_p10r_seller@example.com"
PASSWORD = "test1234"
CAT_A = "smoke-p10r-a"
CAT_B = "smoke-p10r-b"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        users = [u for u in
                 (User.query.filter_by(email=e).first()
                  for e in (CUSTOMER, VIEWER, SELLER))
                 if u is not None]
        for u in users:
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)   # cascades ProductView via Phase 10 cascade
            OtpCode.query.filter_by(user_id=u.id).delete()
        db.session.flush()
        for u in users:
            db.session.delete(u)            # cascades that user's ProductView too
        for slug in (CAT_A, CAT_B):
            cat = Category.query.filter_by(slug=slug).first()
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


def web_login(app, c, email):
    c.post("/login/", data={"email": email, "password": PASSWORD,
                            "account_type": "customer"})
    c.post("/verify-otp/", data={"code": latest_otp(app, email)})


def seed(app):
    """A vendor with three products in cat A and one in cat B."""
    with app.app_context():
        cat_a = Category(name_en="P10R Cat A", slug=CAT_A, is_active=True)
        cat_b = Category(name_en="P10R Cat B", slug=CAT_B, is_active=True)
        db.session.add_all([cat_a, cat_b])

        customer = User(name="P10R Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        viewer = User(name="P10R Viewer", email=VIEWER, role="customer", is_active=True)
        viewer.set_password(PASSWORD)
        seller = User(name="P10R Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, viewer, seller])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P10R Store",
                           slug="p10r-store", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        a1 = Product(vendor_id=vp.id, category_id=cat_a.id, title_en="P10R Alpha One",
                     slug="p10r-alpha-one", base_price=100, stock=10,
                     status=PRODUCT_PUBLISHED)
        a2 = Product(vendor_id=vp.id, category_id=cat_a.id, title_en="P10R Alpha Two",
                     slug="p10r-alpha-two", base_price=100, stock=10,
                     status=PRODUCT_PUBLISHED)
        a3 = Product(vendor_id=vp.id, category_id=cat_a.id, title_en="P10R Alpha Three",
                     slug="p10r-alpha-three", base_price=100, stock=10,
                     status=PRODUCT_PUBLISHED)
        b1 = Product(vendor_id=vp.id, category_id=cat_b.id, title_en="P10R Beta One",
                     slug="p10r-beta-one", base_price=100, stock=10,
                     status=PRODUCT_PUBLISHED)
        db.session.add_all([a1, a2, a3, b1])
        db.session.commit()
        return {"customer_id": customer.id, "viewer_id": viewer.id,
                "a1": a1.id, "a2": a2.id, "a3": a3.id, "b1": b1.id,
                "a1_slug": a1.slug, "a2_slug": a2.slug}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # Seed product-view signals: viewer saw A1 + A2; customer saw A1.
    with app.app_context():
        db.session.add_all([
            ProductView(product_id=ids["a1"], user_id=ids["viewer_id"]),
            ProductView(product_id=ids["a2"], user_id=ids["viewer_id"]),
            ProductView(product_id=ids["a1"], user_id=ids["customer_id"]),
        ])
        db.session.commit()

    # ====================================================================
    # similar_products — same category, excludes self
    # ====================================================================
    with app.app_context():
        a1 = db.session.get(Product, ids["a1"])
        sims = similar_products(a1, limit=10)
        slugs = {p.slug for p in sims}
        check("similar_products is same-category and excludes self",
              "p10r-alpha-two" in slugs and "p10r-alpha-three" in slugs
              and "p10r-alpha-one" not in slugs)
        check("similar_products excludes other categories",
              "p10r-beta-one" not in slugs)

    # ====================================================================
    # also_viewed — co-view collaborative
    # ====================================================================
    with app.app_context():
        a1 = db.session.get(Product, ids["a1"])
        co = also_viewed(a1, limit=10)
        slugs = {p.slug for p in co}
        check("also_viewed returns co-viewed products",
              "p10r-alpha-two" in slugs)
        check("also_viewed excludes the seed product itself",
              "p10r-alpha-one" not in slugs)

    # ====================================================================
    # for_you — viewed category drives recommendations
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        recs = for_you(customer, limit=10)
        slugs = [p.slug for p in recs]
        check("for_you suggests unseen products in viewed categories",
              "p10r-alpha-two" in slugs and "p10r-alpha-three" in slugs
              and "p10r-alpha-one" not in slugs)

    # for_you anonymous -> falls back to best-sellers / ranked
    with app.app_context():
        anon = for_you(None, limit=4)
        check("for_you anonymous returns the best-seller fallback",
              len(anon) >= 1)

    # best_sellers fallback (no orders -> ranked products)
    with app.app_context():
        top = best_sellers(limit=4)
        check("best_sellers falls back to ranking when no sales",
              len(top) >= 1)

    # ====================================================================
    # web — product page sections + dashboard recommendations
    # ====================================================================
    with app.test_client() as c:
        r = c.get(f"/product/{ids['a1_slug']}/")
        check("product page shows Similar Products",
              r.status_code == 200 and b"Similar Products" in r.data)
        check("product page shows Customers Also Viewed",
              b"Customers Also Viewed" in r.data)

    with app.test_client() as c:
        web_login(app, c, CUSTOMER)
        r = c.get("/dashboard/")
        check("dashboard shows Recommended for you",
              r.status_code == 200 and b"Recommended for you" in r.data)

    # ====================================================================
    # REST API
    # ====================================================================
    with app.test_client() as c:
        r = c.get(f"/api/v1/products/{ids['a1_slug']}/similar")
        slugs = {p["slug"] for p in (r.get_json() or {}).get("products", [])}
        check("API /products/<slug>/similar",
              r.status_code == 200 and "p10r-alpha-two" in slugs)

        r = c.get(f"/api/v1/products/{ids['a1_slug']}/also-viewed")
        slugs = {p["slug"] for p in (r.get_json() or {}).get("products", [])}
        check("API /products/<slug>/also-viewed",
              r.status_code == 200 and "p10r-alpha-two" in slugs)

        token = api_token(app, c, CUSTOMER)
        r = c.get("/api/v1/recommendations",
                  headers={"Authorization": f"Bearer {token}"})
        slugs = [p["slug"] for p in (r.get_json() or {}).get("products", [])]
        check("API /recommendations is personalised",
              r.status_code == 200 and "p10r-alpha-two" in slugs
              and "p10r-alpha-one" not in slugs)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 10 recommendations smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
