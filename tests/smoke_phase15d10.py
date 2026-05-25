"""Phase 15 Chunk D-10 smoke test — promotional polish (final D sub-chunk).

Covers:
  * `flash_sale_service.active_sale_for_product(product)` returns the
    live FlashSale containing the product, None otherwise.
  * Inactive / out-of-window sales do not surface.
  * `app_download_service.app_download_url()` reads the platform setting;
    `qr_image_url(url)` produces an api.qrserver.com URL.
  * Product page renders:
      - the flash-sale strip + countdown when a live sale contains the
        product,
      - the App QR panel when `app_download_url` is configured,
      - neither surface when no sale + no app URL.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d10.py
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
from app.services import (
    flash_sale_service, app_download_service,
)
from app.services.settings_service import set_setting

SELLER = "smoke_p15d10_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d10-cat"
PROD_SLUG = "p15d10-product-a"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        seller = User.query.filter_by(email=SELLER).first()
        if seller is not None:
            vp = VendorProfile.query.filter_by(user_id=seller.id).first()
            if vp:
                # FlashSaleItem rows reference Products; delete sales first.
                for sale in FlashSale.query.all():
                    for it in list(sale.items):
                        if it.product and it.product.vendor_id == vp.id:
                            db.session.delete(it)
                    if not sale.items:
                        db.session.delete(sale)
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)
            db.session.delete(seller)
        # Stale sales from previous runs
        for sale in FlashSale.query.filter(
            FlashSale.title.like("P15D10%")
        ).all():
            db.session.delete(sale)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        set_setting("app_download_url", "")
        db.session.commit()


def seed(app):
    with app.app_context():
        cat = Category(name_en="Smoke P15D10", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        seller = User(name="P15D10 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        db.session.add(seller)
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15D10 Shop",
                           slug="p15d10-shop", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D10 Product", slug=PROD_SLUG,
            base_price=500, stock=20, status=PRODUCT_PUBLISHED,
        )
        db.session.add(product)
        db.session.commit()
        return {"product_id": product.id, "vendor_id": vp.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # No active sale, no app URL → strips hidden
    # ====================================================================
    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("no flash-sale strip when no active sale",
              "pdp-flash-strip" not in body)
        check("no app-QR panel when app_download_url is unset",
              "pdp-app-qr" not in body)

    # ====================================================================
    # active_sale_for_product — without a sale
    # ====================================================================
    with app.app_context():
        product = db.session.get(Product, ids["product_id"])
        check("active_sale_for_product None without a sale",
              flash_sale_service.active_sale_for_product(product) is None)

    # ====================================================================
    # Create an inactive (un-activated) sale containing the product
    # ====================================================================
    with app.app_context():
        product = db.session.get(Product, ids["product_id"])
        sale_inactive = FlashSale(
            title="P15D10 Inactive", slug="p15d10-inactive",
            ends_at=datetime.utcnow() + timedelta(hours=2), is_active=False,
        )
        db.session.add(sale_inactive)
        db.session.flush()
        db.session.add(FlashSaleItem(
            flash_sale_id=sale_inactive.id, product_id=product.id,
            flash_price=Decimal("400.00"),
        ))
        db.session.commit()
        check("inactive sale does NOT surface",
              flash_sale_service.active_sale_for_product(product) is None)

    # ====================================================================
    # Activate the sale → strip + countdown render
    # ====================================================================
    with app.app_context():
        sale = (FlashSale.query.filter_by(title="P15D10 Inactive").first())
        flash_sale_service.activate(sale)
        db.session.commit()
        product = db.session.get(Product, ids["product_id"])
        live = flash_sale_service.active_sale_for_product(product)
        check("active live sale returned by helper",
              live is not None and live.title == "P15D10 Inactive")

    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("flash-sale strip renders title",
              "pdp-flash-strip" in body and "P15D10 Inactive" in body)
        check("flash-sale countdown hook present",
              'id="pdpFlashCountdown"' in body and "data-ends-at" in body)

    # ====================================================================
    # Past-end-date sale: live() guard → no strip
    # ====================================================================
    with app.app_context():
        sale = FlashSale.query.filter_by(title="P15D10 Inactive").first()
        sale.ends_at = datetime.utcnow() - timedelta(minutes=1)
        db.session.commit()
        product = db.session.get(Product, ids["product_id"])
        check("expired-end-date sale no longer 'live'",
              flash_sale_service.active_sale_for_product(product) is None)

    # ====================================================================
    # App QR — set + read
    # ====================================================================
    with app.app_context():
        check("app_download_url None when unset",
              app_download_service.app_download_url() is None)
        set_setting("app_download_url",
                    "https://sgt.example.com/app?ref=smoke")
        db.session.commit()
        url = app_download_service.app_download_url()
        check("app_download_url returns the setting",
              url == "https://sgt.example.com/app?ref=smoke")
        qr = app_download_service.qr_image_url(url)
        check("qr_image_url builds api.qrserver.com URL with encoded data",
              qr is not None
              and "api.qrserver.com" in qr
              and "data=" in qr
              and "ref%3Dsmoke" in qr)
        check("qr_image_url returns None for empty input",
              app_download_service.qr_image_url(None) is None
              and app_download_service.qr_image_url("") is None)

    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("app-QR panel renders when configured",
              "pdp-app-qr" in body and "api.qrserver.com" in body)
        check("app-QR panel links back to the configured URL",
              "https://sgt.example.com/app?ref=smoke" in body)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-10 promotional polish smoke test: "
          f"{passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
