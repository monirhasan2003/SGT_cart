"""Phase 15 (Chunk C) smoke test — seller-led flash sales + store promotion.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15c_seller_promo.py
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
from app.models.marketing import FlashSale, FlashSaleItem
from app.models.analytics import ProductView
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN

SELLER = "smoke_p15c_promo_seller@example.com"
OTHER_SELLER = "smoke_p15c_promo_other@example.com"
CAT_SLUG = "smoke-p15c-promo-cat"
PASSWORD = "test1234"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for email in (SELLER, OTHER_SELLER):
            u = User.query.filter_by(email=email).first()
            if not u:
                continue
            OtpCode.query.filter_by(user_id=u.id).delete()
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for s in FlashSale.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(s)
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    ProductView.query.filter_by(product_id=p.id).delete()
                    db.session.delete(p)
        db.session.flush()
        for email in (SELLER, OTHER_SELLER):
            u = User.query.filter_by(email=email).first()
            if u:
                db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()


def seller_login(app, c, email):
    """Two-step OTP login used by all seller / customer accounts."""
    c.post("/login/", data={"email": email, "password": PASSWORD,
                            "account_type": "seller"})
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query
               .filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
    if otp is None:
        return False
    r = c.post("/verify-otp/", data={"code": otp.code}, follow_redirects=True)
    return r.status_code == 200


def seed(app):
    with app.app_context():
        cat = Category(name_en="P15c Promo Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        seller = User(name="P15c Promo Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        other = User(name="P15c Other Seller", email=OTHER_SELLER, role="seller",
                     is_active=True)
        other.set_password(PASSWORD)
        db.session.add_all([seller, other])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15c Promo Shop",
                           slug="p15c-promo-shop", status=VENDOR_APPROVED,
                           commission_rate=10)
        vp_other = VendorProfile(user_id=other.id, shop_name_en="P15c Other Shop",
                                 slug="p15c-other-shop", status=VENDOR_APPROVED,
                                 commission_rate=10)
        db.session.add_all([vp, vp_other])
        db.session.flush()
        my_prod = Product(vendor_id=vp.id, category_id=cat.id,
                          title_en="P15c My Product", slug="p15c-my-product",
                          base_price=200, stock=99, status=PRODUCT_PUBLISHED)
        other_prod = Product(vendor_id=vp_other.id, category_id=cat.id,
                             title_en="P15c Other Product",
                             slug="p15c-other-product",
                             base_price=200, stock=99, status=PRODUCT_PUBLISHED)
        db.session.add_all([my_prod, other_prod])
        db.session.commit()
        return {
            "seller_email": SELLER, "vendor_id": vp.id, "vendor_slug": vp.slug,
            "my_prod_id": my_prod.id, "other_prod_id": other_prod.id,
        }


def main():
    app = create_app("development")
    purge(app)
    ids = seed(app)
    app.config["WTF_CSRF_ENABLED"] = False

    # ====================================================================
    # seller logs in, creates flash sale, adds own product, activates it
    # ====================================================================
    with app.test_client() as c:
        check("seller login ok", seller_login(app, c, SELLER))

        # Flash sale list page renders.
        r = c.get("/seller/flash-sales/")
        check("/seller/flash-sales/ renders",
              r.status_code == 200 and b"Flash Sales" in r.data)

        # Create a new sale.
        future = (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
        r = c.post("/seller/flash-sales/new",
                   data={"title": "Smoke P15c Seller Sale", "ends_at": future},
                   follow_redirects=True)
        check("seller can create flash sale", r.status_code == 200)

        with app.app_context():
            sale = FlashSale.query.filter_by(vendor_id=ids["vendor_id"]).first()
            check("new sale persisted with vendor_id",
                  sale is not None and sale.vendor_id == ids["vendor_id"])
            sale_id = sale.id

        # Reject cross-vendor product.
        r = c.post(f"/seller/flash-sales/{sale_id}/items",
                   data={"product_id": ids["other_prod_id"], "flash_price": "150"},
                   follow_redirects=True)
        with app.app_context():
            sale = db.session.get(FlashSale, sale_id)
            check("cross-vendor product is NOT added",
                  not any(it.product_id == ids["other_prod_id"]
                          for it in sale.items))

        # Reject price >= base price.
        r = c.post(f"/seller/flash-sales/{sale_id}/items",
                   data={"product_id": ids["my_prod_id"], "flash_price": "200"},
                   follow_redirects=True)
        with app.app_context():
            sale = db.session.get(FlashSale, sale_id)
            check("flash price >= regular price rejected",
                  not any(it.product_id == ids["my_prod_id"]
                          for it in sale.items))

        # Add own product at a valid lower price.
        r = c.post(f"/seller/flash-sales/{sale_id}/items",
                   data={"product_id": ids["my_prod_id"], "flash_price": "120"},
                   follow_redirects=True)
        with app.app_context():
            sale = db.session.get(FlashSale, sale_id)
            check("own product added at lower price",
                  any(it.product_id == ids["my_prod_id"] for it in sale.items))

        # Activate the sale.
        r = c.post(f"/seller/flash-sales/{sale_id}/activate",
                   follow_redirects=True)
        with app.app_context():
            sale = db.session.get(FlashSale, sale_id)
            prod = db.session.get(Product, ids["my_prod_id"])
            check("sale activated", sale.is_active)
            check("activation pushed flash price onto product.discount_price",
                  prod.discount_price == Decimal("120.00"))

    # ====================================================================
    # public /flash-sales/ surfaces the seller's live sale
    # ====================================================================
    with app.test_client() as c:
        r = c.get("/flash-sales/")
        body = r.data.decode("utf-8", errors="ignore")
        check("public flash-sales page lists seller sale",
              r.status_code == 200 and "Smoke P15c Seller Sale" in body
              and "P15c Promo Shop" in body)

    # ====================================================================
    # seller deactivates → product price restored
    # ====================================================================
    with app.test_client() as c:
        seller_login(app, c, SELLER)
        with app.app_context():
            sale_id = FlashSale.query.filter_by(vendor_id=ids["vendor_id"]).first().id
        r = c.post(f"/seller/flash-sales/{sale_id}/deactivate",
                   follow_redirects=True)
        with app.app_context():
            sale = db.session.get(FlashSale, sale_id)
            prod = db.session.get(Product, ids["my_prod_id"])
            check("sale deactivated", not sale.is_active)
            check("product price restored after deactivation",
                  prod.discount_price is None)

    # ====================================================================
    # store promotion banner round-trip
    # ====================================================================
    with app.test_client() as c:
        seller_login(app, c, SELLER)

        r = c.get("/seller/store-promo/")
        check("/seller/store-promo/ renders",
              r.status_code == 200 and b"Store Promotion" in r.data)

        future = (datetime.utcnow() + timedelta(days=14)).strftime("%Y-%m-%d")
        r = c.post("/seller/store-promo/",
                   data={"promo_banner_text": "Eid Mega Sale — 40% off!",
                         "promo_until": future},
                   follow_redirects=True)
        with app.app_context():
            vp = db.session.get(VendorProfile, ids["vendor_id"])
            check("promo text saved", vp.promo_banner_text
                  == "Eid Mega Sale — 40% off!")
            check("promo until saved", vp.promo_until is not None)
            check("has_active_promo is True", vp.has_active_promo)

    # ====================================================================
    # store page shows the promo banner
    # ====================================================================
    with app.test_client() as c:
        r = c.get(f"/store/{ids['vendor_slug']}/")
        body = r.data.decode("utf-8", errors="ignore")
        check("store page shows the promo banner",
              r.status_code == 200 and "Eid Mega Sale" in body)

    # ====================================================================
    # promo auto-hides once expired
    # ====================================================================
    with app.app_context():
        vp = db.session.get(VendorProfile, ids["vendor_id"])
        vp.promo_until = datetime.utcnow() - timedelta(days=1)
        db.session.commit()
        check("has_active_promo False once past promo_until",
              not vp.has_active_promo)

    with app.test_client() as c:
        r = c.get(f"/store/{ids['vendor_slug']}/")
        body = r.data.decode("utf-8", errors="ignore")
        check("expired promo no longer shown on store page",
              r.status_code == 200 and "Eid Mega Sale" not in body)

    # ====================================================================
    # clear promo via the form
    # ====================================================================
    with app.test_client() as c:
        seller_login(app, c, SELLER)
        r = c.post("/seller/store-promo/",
                   data={"action": "clear"}, follow_redirects=True)
        with app.app_context():
            vp = db.session.get(VendorProfile, ids["vendor_id"])
            check("clear action wipes promo fields",
                  vp.promo_banner_text is None
                  and vp.promo_banner_image is None
                  and vp.promo_until is None)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 Chunk C seller promo smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
