"""Phase 10 (Chunk A) smoke test — ranking, autocomplete & search signals.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase10_search.py
"""
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.analytics import ProductView, SearchLog
from app.services.search_service import apply_ranking, autocomplete

ADMIN_EMAIL = "monirhasan2003@gmail.com"
SELLER_A = "smoke_p10_sellera@example.com"
SELLER_B = "smoke_p10_sellerb@example.com"
CAT_SLUG = "smoke-p10-cat"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        SearchLog.query.filter(SearchLog.term.like("P10%")).delete(
            synchronize_session=False)
        users = [u for u in
                 (User.query.filter_by(email=e).first() for e in (SELLER_A, SELLER_B))
                 if u is not None]
        for u in users:
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    ProductView.query.filter_by(product_id=p.id).delete(
                        synchronize_session=False)
                    db.session.delete(p)
        db.session.flush()
        for u in users:
            db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()


def seed(app):
    """Two sellers — A highly rated, B poorly rated — each with one product."""
    with app.app_context():
        cat = Category(name_en="Smoke P10 Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        sa = User(name="P10 Seller A", email=SELLER_A, role="seller", is_active=True)
        sa.set_password("test1234")
        sb = User(name="P10 Seller B", email=SELLER_B, role="seller", is_active=True)
        sb.set_password("test1234")
        db.session.add_all([sa, sb])
        db.session.flush()
        vp_a = VendorProfile(user_id=sa.id, shop_name_en="P10 Store A",
                             slug="p10-store-a", status=VENDOR_APPROVED,
                             commission_rate=10, rating_avg=Decimal("4.80"),
                             rating_count=20)
        vp_b = VendorProfile(user_id=sb.id, shop_name_en="P10 Store B",
                             slug="p10-store-b", status=VENDOR_APPROVED,
                             commission_rate=10, rating_avg=Decimal("2.10"),
                             rating_count=8)
        db.session.add_all([vp_a, vp_b])
        db.session.flush()
        prod_a = Product(vendor_id=vp_a.id, category_id=cat.id,
                         title_en="P10 Alpha Widget", slug="p10-alpha-widget",
                         base_price=300, stock=50, status=PRODUCT_PUBLISHED)
        prod_b = Product(vendor_id=vp_b.id, category_id=cat.id,
                         title_en="P10 Beta Widget", slug="p10-beta-widget",
                         base_price=300, stock=50, status=PRODUCT_PUBLISHED)
        db.session.add_all([prod_a, prod_b])
        db.session.commit()
        return {"vendor_a": vp_a.id, "vendor_b": vp_b.id,
                "prod_a": prod_a.id, "prod_b": prod_b.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)
    with app.app_context():
        admin_id = User.query.filter_by(email=ADMIN_EMAIL).first().id

    # ====================================================================
    # ranking — higher-rated seller first
    # ====================================================================
    with app.app_context():
        base = Product.query.filter(
            Product.vendor_id.in_([ids["vendor_a"], ids["vendor_b"]]),
            Product.status == PRODUCT_PUBLISHED,
        )
        ranked = apply_ranking(base).all()
        check("higher-rated seller's product ranks first",
              ranked and ranked[0].id == ids["prod_a"])

    # ====================================================================
    # admin ranking override
    # ====================================================================
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["_user_id"] = str(admin_id)
        r = c.post(f"/admin/vendors/{ids['vendor_b']}/ranking",
                   data={"ranking_boost": "5"}, follow_redirects=True)
        check("admin sets a ranking boost", r.status_code == 200)

    with app.app_context():
        vp_b = db.session.get(VendorProfile, ids["vendor_b"])
        check("ranking boost persisted", vp_b.ranking_boost == Decimal("5.00"))
        base = Product.query.filter(
            Product.vendor_id.in_([ids["vendor_a"], ids["vendor_b"]]),
            Product.status == PRODUCT_PUBLISHED,
        )
        ranked = apply_ranking(base).all()
        check("boost overrides rating-based order (B now first)",
              ranked and ranked[0].id == ids["prod_b"])
        # reset so the rest of the test reads naturally
        vp_b.ranking_boost = Decimal("0")
        db.session.commit()

    # ====================================================================
    # autocomplete
    # ====================================================================
    with app.app_context():
        suggestions = autocomplete("Widget")
        slugs = {s["slug"] for s in suggestions}
        check("autocomplete matches product titles",
              "p10-alpha-widget" in slugs and "p10-beta-widget" in slugs)
        check("autocomplete ignores too-short prefixes", autocomplete("W") == [])

    # ====================================================================
    # web — search logging, view logging, suggest endpoint
    # ====================================================================
    with app.test_client() as c:
        r = c.get("/shop/?q=P10 Widget")
        check("web shop search renders", r.status_code == 200)

        r = c.get("/product/p10-alpha-widget/")
        check("web product page renders", r.status_code == 200)

        r = c.get("/search/suggest?q=Widget")
        body = r.get_json() or {}
        check("web /search/suggest returns suggestions",
              r.status_code == 200 and len(body.get("suggestions", [])) >= 2)

    with app.app_context():
        check("search was logged",
              SearchLog.query.filter(SearchLog.term == "P10 Widget").count() >= 1)
        check("product view was logged",
              ProductView.query.filter_by(product_id=ids["prod_a"]).count() >= 1)

    # ====================================================================
    # REST API
    # ====================================================================
    with app.test_client() as c:
        r = c.get("/api/v1/products?q=P10")
        prods = (r.get_json() or {}).get("products", [])
        order = [p["slug"] for p in prods if p["slug"].startswith("p10-")]
        check("API products applies ranking (A before B)",
              order[:2] == ["p10-alpha-widget", "p10-beta-widget"])

        r = c.get("/api/v1/products/p10-beta-widget")
        check("API product detail renders", r.status_code == 200)

        r = c.get("/api/v1/search/suggest?q=Widget")
        check("API /search/suggest returns suggestions",
              r.status_code == 200
              and len((r.get_json() or {}).get("suggestions", [])) >= 2)

    with app.app_context():
        check("API product view was logged",
              ProductView.query.filter_by(product_id=ids["prod_b"]).count() >= 1)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 10 search smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
