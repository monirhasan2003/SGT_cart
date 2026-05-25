"""Phase 15 (Chunk B v3c) smoke test — admin-controlled Sponsored promotion.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15c_sponsored.py
"""
import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.analytics import ProductView
from app.models.setting import AuditLog
from app.services.search_service import apply_ranking

SELLER = "smoke_p15c_seller@example.com"
ADMIN = "smoke_p15c_admin@example.com"
CAT_SLUG = "smoke-p15c-cat"
PASSWORD = "test1234"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for email in (SELLER, ADMIN):
            u = User.query.filter_by(email=email).first()
            if not u:
                continue
            AuditLog.query.filter_by(actor_id=u.id).delete()
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    ProductView.query.filter_by(product_id=p.id).delete()
                    db.session.delete(p)
        db.session.flush()
        for email in (SELLER, ADMIN):
            u = User.query.filter_by(email=email).first()
            if u:
                db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()


def seed(app):
    with app.app_context():
        cat = Category(name_en="P15c Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        admin = User(name="P15c Admin", email=ADMIN, role="admin", is_active=True)
        admin.set_password(PASSWORD)
        seller = User(name="P15c Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([admin, seller])
        db.session.flush()
        # Top vendor (high rating) vs sponsored vendor (low rating).
        # The sponsored product should still rank above the organic top product.
        vp_top = VendorProfile(user_id=admin.id, shop_name_en="P15c Top",
                               slug="p15c-top", status=VENDOR_APPROVED,
                               commission_rate=10,
                               rating_avg=Decimal("4.80"), rating_count=50)
        vp_low = VendorProfile(user_id=seller.id, shop_name_en="P15c Low",
                               slug="p15c-low", status=VENDOR_APPROVED,
                               commission_rate=10,
                               rating_avg=Decimal("3.00"), rating_count=10)
        db.session.add_all([vp_top, vp_low])
        db.session.flush()
        prod_top = Product(vendor_id=vp_top.id, category_id=cat.id,
                           title_en="P15c Organic Top", slug="p15c-organic-top",
                           base_price=100, stock=99, status=PRODUCT_PUBLISHED)
        prod_sponsored = Product(vendor_id=vp_low.id, category_id=cat.id,
                                 title_en="P15c Sponsored Item",
                                 slug="p15c-sponsored-item",
                                 base_price=100, stock=99, status=PRODUCT_PUBLISHED)
        db.session.add_all([prod_top, prod_sponsored])
        db.session.commit()
        return {
            "admin_email": ADMIN, "seller_email": SELLER,
            "prod_top": prod_top.id, "prod_sponsored": prod_sponsored.id,
        }


def main():
    app = create_app("development")
    purge(app)
    ids = seed(app)

    # ====================================================================
    # baseline — organic top wins on rating
    # ====================================================================
    with app.app_context():
        q = Product.query.filter(
            Product.id.in_([ids["prod_top"], ids["prod_sponsored"]]),
            Product.status == PRODUCT_PUBLISHED,
        )
        ranked = apply_ranking(q).all()
        check("baseline: high-rated product ranks first",
              ranked and ranked[0].id == ids["prod_top"],
              detail=str([p.slug for p in ranked]))

    # ====================================================================
    # admin marks low-rated product Sponsored (open-ended)
    # ====================================================================
    with app.app_context():
        prod = db.session.get(Product, ids["prod_sponsored"])
        prod.is_sponsored = True
        prod.sponsored_until = None
        db.session.commit()
        check("is_sponsored_active true with no expiry",
              prod.is_sponsored_active)

        q = Product.query.filter(
            Product.id.in_([ids["prod_top"], ids["prod_sponsored"]]),
            Product.status == PRODUCT_PUBLISHED,
        )
        ranked = apply_ranking(q).all()
        check("sponsored product jumps above the high-rated organic one",
              ranked and ranked[0].id == ids["prod_sponsored"],
              detail=str([p.slug for p in ranked]))

    # ====================================================================
    # expired sponsorship is ignored — organic order returns
    # ====================================================================
    with app.app_context():
        prod = db.session.get(Product, ids["prod_sponsored"])
        prod.sponsored_until = datetime.utcnow() - timedelta(days=1)
        db.session.commit()
        check("is_sponsored_active false once past sponsored_until",
              not prod.is_sponsored_active)

        q = Product.query.filter(
            Product.id.in_([ids["prod_top"], ids["prod_sponsored"]]),
            Product.status == PRODUCT_PUBLISHED,
        )
        ranked = apply_ranking(q).all()
        check("expired sponsored no longer beats organic top",
              ranked and ranked[0].id == ids["prod_top"],
              detail=str([p.slug for p in ranked]))

    # ====================================================================
    # admin route smoke — page renders + POST toggles state
    # ====================================================================
    with app.app_context():
        admin = User.query.filter_by(email=ADMIN).first()
        admin.role = "admin"
        db.session.commit()
        app.config["WTF_CSRF_ENABLED"] = False

    with app.test_client() as c:
        r = c.post("/admin/login",
                   data={"email": ADMIN, "password": PASSWORD},
                   follow_redirects=True)
        check("admin login ok",
              r.status_code == 200 and b"Dashboard" in r.data)

        r = c.get("/admin/sponsored/")
        check("/admin/sponsored/ renders",
              r.status_code == 200 and b"Sponsored Products" in r.data)

        # Sponsor the organic-top product via the admin form (with a future date).
        future = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")
        r = c.post(f"/admin/sponsored/{ids['prod_top']}",
                   data={"sponsored_until": future}, follow_redirects=True)
        check("admin POST marks product sponsored", r.status_code == 200)

        with app.app_context():
            prod = db.session.get(Product, ids["prod_top"])
            check("admin POST persisted is_sponsored=True", prod.is_sponsored)
            check("admin POST persisted sponsored_until in future",
                  prod.sponsored_until is not None
                  and prod.sponsored_until > datetime.utcnow())

        # Disable via the same form.
        r = c.post(f"/admin/sponsored/{ids['prod_top']}",
                   data={"action": "disable"}, follow_redirects=True)
        with app.app_context():
            prod = db.session.get(Product, ids["prod_top"])
            check("admin POST action=disable clears sponsorship",
                  not prod.is_sponsored and prod.sponsored_until is None)

    # ====================================================================
    # storefront product card shows the Sponsored badge
    # ====================================================================
    with app.app_context():
        prod = db.session.get(Product, ids["prod_sponsored"])
        prod.is_sponsored = True
        prod.sponsored_until = None
        db.session.commit()
        slug = prod.slug

    with app.test_client() as c:
        r = c.get(f"/shop/?q=p15c")
        body = r.data.decode("utf-8", errors="ignore")
        # The Sponsored badge is rendered next to the sponsored product card.
        check("shop page exposes Sponsored badge",
              r.status_code == 200 and "Sponsored" in body
              and slug in body)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 Chunk B v3c sponsored smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
