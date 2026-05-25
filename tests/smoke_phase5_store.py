"""Phase 5 smoke test — seller store presentation (logo, banner, public store page).

Run:  venv\\Scripts\\python.exe tests\\smoke_phase5_store.py
"""
import os
import sys
from io import BytesIO
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.vendor import VendorProfile, VENDOR_APPROVED, VENDOR_PENDING
from app.models.catalog import Category, Product, ProductImage, PRODUCT_PUBLISHED

SELLER = "smoke_store_seller@example.com"
PENDING_SELLER = "smoke_store_pending@example.com"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for email in (SELLER, PENDING_SELLER):
            u = User.query.filter_by(email=email).first()
            if u:
                OtpCode.query.filter_by(user_id=u.id).delete()
                db.session.delete(u)
                db.session.commit()


def otp_login(app, c, email):
    c.post("/login/", data={"email": email, "password": "test1234", "account_type": "seller"})
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query.filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
    c.post("/verify-otp/", data={"code": otp.code})


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)

    # approved seller with a published product
    with app.app_context():
        u = User(name="Store Seller", email=SELLER, role="seller",
                 is_active=True, is_email_verified=True)
        u.set_password("test1234")
        db.session.add(u)
        db.session.flush()
        vp = VendorProfile(user_id=u.id, shop_name_en="Smoke Store", slug="smoke-store",
                           status=VENDOR_APPROVED)
        db.session.add(vp)
        db.session.flush()
        cat = Category.query.filter_by(parent_id=None).first()
        prod = Product(vendor_id=vp.id, category_id=cat.id, title_en="Smoke Store Widget",
                       slug="smoke-store-widget", base_price=Decimal("250.00"),
                       stock=10, status=PRODUCT_PUBLISHED)
        db.session.add(prod)
        db.session.flush()
        db.session.add(ProductImage(product_id=prod.id, image_path="assets/img/shop/9.png",
                                    is_primary=True))
        # a pending (unapproved) seller
        pu = User(name="Pending Seller", email=PENDING_SELLER, role="seller",
                  is_active=True, is_email_verified=True)
        pu.set_password("test1234")
        db.session.add(pu)
        db.session.flush()
        db.session.add(VendorProfile(user_id=pu.id, shop_name_en="Pending Store",
                                     slug="pending-store", status=VENDOR_PENDING))
        db.session.commit()
        cat_slug = cat.slug
        product_slug = prod.slug

    # --- seller edits shop profile (logo + banner) ---
    with app.test_client() as c:
        otp_login(app, c, SELLER)

        r = c.get("/seller/shop/")
        check("Seller shop profile page", r.status_code == 200)

        r = c.post("/seller/shop/", data={
            "shop_name_en": "Smoke Mega Store",
            "description_en": "The finest smoke-test goods in town.",
            "logo": (BytesIO(b"fake-logo"), "logo.png"),
            "banner": (BytesIO(b"fake-banner"), "banner.jpg"),
        }, content_type="multipart/form-data")
        check("Shop profile saved", r.status_code == 302)
        with app.app_context():
            vp = VendorProfile.query.filter_by(slug="smoke-store").first()
            check("Logo & banner stored",
                  bool(vp.logo) and bool(vp.banner) and vp.shop_name_en == "Smoke Mega Store")

    # --- public store page ---
    with app.test_client() as c:
        r = c.get("/store/smoke-store/")
        check("Public store page", r.status_code == 200
              and b"Smoke Mega Store" in r.data and b"Smoke Store Widget" in r.data)

        r = c.get("/store/smoke-store/?q=widget")
        check("In-store search (match)", r.status_code == 200 and b"Smoke Store Widget" in r.data)

        r = c.get("/store/smoke-store/?q=zzznomatch")
        check("In-store search (no match)",
              r.status_code == 200 and b"No products found in this store" in r.data)

        r = c.get(f"/store/smoke-store/?category={cat_slug}")
        check("In-store category filter", r.status_code == 200 and b"Smoke Store Widget" in r.data)

        r = c.get("/store/smoke-store/?min=1000")
        check("In-store price filter excludes cheap item",
              r.status_code == 200 and b"Smoke Store Widget" not in r.data)

        r = c.get("/store/no-such-store/")
        check("Unknown store -> 404", r.status_code == 404)

        r = c.get("/store/pending-store/")
        check("Unapproved vendor store -> 404", r.status_code == 404)

        r = c.get(f"/product/{product_slug}/")
        check("Product page has Visit Store link",
              r.status_code == 200 and b"Visit Store" in r.data
              and b"/store/smoke-store/" in r.data)

    purge(app)
    print("(test sellers cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 5 store smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
