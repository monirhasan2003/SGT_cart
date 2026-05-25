"""Phase 2 smoke test — seller product management + admin product review.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase2_products.py <admin_password>
"""
import os
import sys
from io import BytesIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product

ADMIN_EMAIL = "monirhasan2003@gmail.com"
SELLER = "smoke_prod_seller@example.com"
UNAPPROVED = "smoke_prod_unapproved@example.com"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app, email):
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        if u:
            OtpCode.query.filter_by(user_id=u.id).delete()
            # ORM delete cascades: user -> vendor_profile -> products -> images/variants
            db.session.delete(u)
            db.session.commit()


def register_seller(c, email, shop):
    c.post("/signup/", data={
        "first_name": "Prod", "last_name": "Seller", "email": email,
        "phone": "01700000000", "role": "seller", "shop_name": shop,
        "password": "test1234", "confirm_password": "test1234",
    })


def otp_login(app, c, email):
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
    purge(app, SELLER)
    purge(app, UNAPPROVED)

    # approved seller
    with app.test_client() as c:
        register_seller(c, SELLER, "Product Test Shop")
    with app.app_context():
        u = User.query.filter_by(email=SELLER).first()
        vp = VendorProfile.query.filter_by(user_id=u.id).first()
        vp.status = VENDOR_APPROVED
        db.session.commit()
        category_id = Category.query.filter_by(parent_id=None).first().id

    with app.test_client() as c:
        otp_login(app, c, SELLER)

        r = c.get("/seller/products/")
        check("Seller products page", r.status_code == 200)

        r = c.post("/seller/products/create", data={
            "title_en": "Smoke Test Product", "title_bn": "স্মোক",
            "category_id": str(category_id), "base_price": "199.99",
            "discount_price": "149.99", "stock": "25", "sku": "SMK-1",
            "description_en": "A great test product.",
            "images": (BytesIO(b"fake-image-bytes"), "p1.jpg"),
        }, content_type="multipart/form-data")
        check("Product created (-> edit)", r.status_code == 302 and "/edit" in r.headers.get("Location", ""))

        with app.app_context():
            p = Product.query.filter_by(title_en="Smoke Test Product").first()
            check("Product saved as draft", p is not None and p.status == "draft")
            check("Product has image", p is not None and len(p.images) == 1)
            pid = p.id if p else None

        r = c.get(f"/seller/products/{pid}/edit")
        check("Product edit page", r.status_code == 200)

        # update core fields
        c.post(f"/seller/products/{pid}/edit", data={
            "title_en": "Smoke Test Product", "category_id": str(category_id),
            "base_price": "180", "stock": "30",
        })
        with app.app_context():
            check("Product updated", int(db.session.get(Product, pid).stock) == 30)

        # add a variant
        c.post(f"/seller/products/{pid}/variants", data={
            "size": "L", "color": "Red", "price": "185", "stock": "10",
        })
        with app.app_context():
            check("Variant added", len(db.session.get(Product, pid).variants) == 1)

        # add another image
        c.post(f"/seller/products/{pid}/images", data={
            "images": (BytesIO(b"img2"), "p2.jpg"),
        }, content_type="multipart/form-data")
        with app.app_context():
            check("Image added", len(db.session.get(Product, pid).images) == 2)

        # submit for review
        c.post(f"/seller/products/{pid}/submit")
        with app.app_context():
            check("Product submitted (pending)", db.session.get(Product, pid).status == "pending")

    # unapproved seller is blocked from product management
    with app.test_client() as c:
        register_seller(c, UNAPPROVED, "Unapproved Shop")
        otp_login(app, c, UNAPPROVED)
        r = c.get("/seller/products/", follow_redirects=False)
        check("Unapproved seller blocked", r.status_code == 302
              and "/seller" in r.headers.get("Location", ""))

    # admin reviews + publishes
    with app.test_client() as c:
        c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})
        r = c.get("/admin/products/?status=pending")
        check("Admin sees pending product", r.status_code == 200 and b"Smoke Test Product" in r.data)
        c.post(f"/admin/products/{pid}/approve")
        with app.app_context():
            check("Admin published product", db.session.get(Product, pid).status == "published")

    purge(app, SELLER)
    purge(app, UNAPPROVED)
    print("(test data cleaned up)")

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 2 products smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
