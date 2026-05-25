"""Phase 15 Chunk D-1 smoke test — product page layout & Daraz parity.

Covers:
  * Right Delivery sidebar (location, ETA, shipping fee, COD, return, warranty).
  * Sold By panel with Chat Now + Visit Store + Verified + Mall tier badge.
  * Buy Now button posts cart.add with buy_now=1 and lands on /cart/checkout/.
  * Quantity ± selector + qty hidden inputs.
  * Color / variant text swatches rendered for products with variants.
  * Share + Wishlist icons present on the product header.
  * COD + Free Shipping inline stickers.
  * Image zoom magnifier wired (data-zoom + #zoomLens + #zoomResult).
  * Brand "More from <brand>" link uses /shop/?brand=<slug>.
  * Shop endpoint filters by ?brand=.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d1.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import (
    Category, Brand, Product, ProductVariant, ProductImage, PRODUCT_PUBLISHED,
)
from app.models.cart import CartItem
from app.models.user import Address

CUSTOMER = "smoke_p15d1_customer@example.com"
SELLER_MALL = "smoke_p15d1_mall@example.com"
SELLER_PLAIN = "smoke_p15d1_plain@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d1-cat"
BRAND_SLUG = "smoke-p15d1-brand"
PROD_SLUG = "p15d1-product-a"
PROD2_SLUG = "p15d1-product-b"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        users = [u for u in
                 (User.query.filter_by(email=e).first()
                  for e in (CUSTOMER, SELLER_MALL, SELLER_PLAIN))
                 if u is not None]
        for u in users:
            CartItem.query.filter_by(user_id=u.id).delete()
            Address.query.filter_by(user_id=u.id).delete()
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
        brand = Brand.query.filter_by(slug=BRAND_SLUG).first()
        if brand:
            db.session.delete(brand)
        db.session.commit()


def latest_otp(app, email):
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query
               .filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
        return otp.code if otp else None


def web_login(app, c, email, account_type):
    c.post("/login/", data={"email": email, "password": PASSWORD,
                            "account_type": account_type})
    c.post("/verify-otp/", data={"code": latest_otp(app, email)})


def seed(app):
    """Two sellers (mall-tier + plain), one branded product with variants."""
    with app.app_context():
        cat = Category(name_en="Smoke P15D1", slug=CAT_SLUG, is_active=True)
        brand = Brand(name="P15D1 Brand", slug=BRAND_SLUG, is_active=True)
        db.session.add_all([cat, brand])
        customer = User(name="P15D1 Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller_mall = User(name="P15D1 Mall Seller", email=SELLER_MALL,
                           role="seller", is_active=True)
        seller_mall.set_password(PASSWORD)
        seller_plain = User(name="P15D1 Plain Seller", email=SELLER_PLAIN,
                            role="seller", is_active=True)
        seller_plain.set_password(PASSWORD)
        db.session.add_all([customer, seller_mall, seller_plain])
        db.session.flush()

        # Mall-tier vendor — verified, high rating, many reviews. Full KYC
        # (both docs uploaded) so the strict D-4 Verified-by-SGT badge fires.
        vp_mall = VendorProfile(
            user_id=seller_mall.id, shop_name_en="P15D1 Mall Shop",
            slug="p15d1-mall-shop", status=VENDOR_APPROVED,
            commission_rate=10, rating_avg=4.7, rating_count=25,
            verification_submitted_at=db.func.now(),
            trade_license_no="TL-P15D1", trade_license_doc="kyc/tl.pdf",
            nid_number="NID-P15D1", nid_doc="kyc/nid.pdf",
        )
        vp_plain = VendorProfile(
            user_id=seller_plain.id, shop_name_en="P15D1 Plain Shop",
            slug="p15d1-plain-shop", status=VENDOR_APPROVED,
            commission_rate=10, rating_avg=3.5, rating_count=3,
        )
        db.session.add_all([vp_mall, vp_plain])
        db.session.flush()

        product = Product(
            vendor_id=vp_mall.id, category_id=cat.id, brand_id=brand.id,
            title_en="P15D1 Product A", slug=PROD_SLUG,
            base_price=750, stock=10, status=PRODUCT_PUBLISHED,
        )
        # Sibling product under same brand for "More from Brand".
        product2 = Product(
            vendor_id=vp_mall.id, category_id=cat.id, brand_id=brand.id,
            title_en="P15D1 Product B", slug=PROD2_SLUG,
            base_price=500, stock=5, status=PRODUCT_PUBLISHED,
        )
        db.session.add_all([product, product2])
        db.session.flush()
        db.session.add_all([
            ProductVariant(product_id=product.id, color="Red", size="S",
                           price=750, stock=5),
            ProductVariant(product_id=product.id, color="Blue", size="M",
                           price=770, stock=5),
            # A primary image so the zoom magnifier (and `data-zoom`) render.
            ProductImage(product_id=product.id,
                         image_path="assets/img/placeholder.png", is_primary=True),
        ])
        db.session.commit()
        return {"customer_id": customer.id, "vendor_mall_id": vp_mall.id,
                "vendor_plain_id": vp_plain.id, "product_id": product.id,
                "product2_id": product2.id, "brand_id": brand.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # service-level: is_mall_tier property
    # ====================================================================
    with app.app_context():
        vp_mall = db.session.get(VendorProfile, ids["vendor_mall_id"])
        vp_plain = db.session.get(VendorProfile, ids["vendor_plain_id"])
        check("mall-tier vendor flagged as Mall", vp_mall.is_mall_tier is True)
        check("low-rating vendor NOT Mall", vp_plain.is_mall_tier is False)

    # ====================================================================
    # product detail page — anonymous render
    # ====================================================================
    with app.test_client() as c:
        r = c.get(f"/product/{PROD_SLUG}/")
        body = r.data.decode("utf-8", errors="ignore")
        check("product page renders", r.status_code == 200)

        # Layout chunks
        check("Delivery sidebar present",
              "Delivery" in body and "Estimated" in body
              and "Return policy" in body and "Warranty" in body)
        check("Shipping fee shown in Delivery sidebar", "Shipping fee" in body)
        check("Sold By panel present",
              "Sold By" in body and "Visit Store" in body)
        check("Mall badge shown on mall-tier seller",
              "lni-crown" in body and ">Mall<" in body)
        check("Verified-by-SGT badge shown for fully KYC-verified vendor",
              "Verified by SGT" in body)
        check("Buy Now button present + carries hidden flag",
              "pdpBuyNowBtn" in body and 'name="buy_now"' in body)
        check("Quantity ± selector present",
              "pdpQtyMinus" in body and "pdpQtyPlus" in body
              and 'id="pdpQty"' in body)
        check("variant color swatches rendered",
              'data-swatch-kind="color"' in body
              and "Red" in body and "Blue" in body)
        check("variant size swatches rendered",
              'data-swatch-kind="size"' in body
              and ">S<" in body and ">M<" in body)
        check("Share button present", 'id="pdpShareBtn"' in body)
        check("Wishlist button present", 'id="pdpWishlistBtn"' in body)
        check("COD inline sticker present", "Cash on Delivery" in body)
        # Product is 750 < 1000 threshold so Free Shipping sticker should be absent
        check("Free Shipping helper offered when below threshold",
              "Add" in body and "unlock" in body and "Free Shipping" in body)
        check("image zoom wiring present",
              'id="zoomLens"' in body and 'id="zoomResult"' in body
              and 'data-zoom=' in body)
        check("More from Brand section present",
              "More from" in body and "P15D1 Brand" in body)
        check("More from Brand link uses brand slug",
              f"brand={BRAND_SLUG}" in body)

    # ====================================================================
    # brand filter on /shop/
    # ====================================================================
    with app.test_client() as c:
        r = c.get(f"/shop/?brand={BRAND_SLUG}")
        body = r.data.decode("utf-8", errors="ignore")
        check("shop?brand=<slug> filters by brand",
              r.status_code == 200
              and PROD_SLUG in body and PROD2_SLUG in body)

        r = c.get("/shop/?brand=does-not-exist")
        # unknown brand returns the unfiltered shop (active_brand is None)
        check("shop with bogus brand still 200", r.status_code == 200)

    # ====================================================================
    # Buy Now flow — POST cart.add with buy_now=1 -> /cart/checkout/
    # ====================================================================
    with app.test_client() as c:
        # Need a delivery address so /cart/checkout/ doesn't bounce.
        web_login(app, c, CUSTOMER, "customer")
        c.post("/account/addresses/new", data={
            "label": "Home", "full_name": "P15D1 Customer",
            "phone": "01700000099", "address_line": "1 Buy-Now St",
            "area": "Test", "city": "Dhaka", "district": "Dhaka",
            "postal_code": "1000", "is_default": "y",
        })
        r = c.post("/cart/add", data={
            "product_id": ids["product_id"], "quantity": "2", "buy_now": "1",
        })
        check("Buy Now redirects somewhere", r.status_code in (302, 303))
        check("Buy Now redirects to /cart/checkout/",
              "/cart/checkout" in r.headers.get("Location", ""))

        r = c.get("/cart/checkout/")
        check("checkout page loads after Buy Now",
              r.status_code == 200 and b"Checkout" in r.data)

        # cart was populated
        with app.app_context():
            count = CartItem.query.filter_by(user_id=ids["customer_id"]).count()
            check("cart item written by Buy Now", count >= 1)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-1 product page smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
