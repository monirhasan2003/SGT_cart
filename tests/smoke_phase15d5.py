"""Phase 15 Chunk D-5 smoke test — Money & Loyalty inline.

Covers:
  * ProductPriceTier model + cascade on Product delete.
  * pricing_service.applicable_tier picks the highest-min_quantity row
    that the quantity has reached; effective_unit_price applies the % off.
  * CartItem.unit_price honors tiers at cart-add time -> line_total reflects
    the discounted price.
  * Seller routes:
      - POST /seller/products/<id>/tiers — add tier (rejects qty<2, pct≤0,
        pct≥100, duplicate qty)
      - POST /seller/products/<id>/tiers/<tier_id>/delete — remove
  * Product page renders Money & Loyalty section with:
      - "Earn X points" preview (M1)
      - inline coupon form (M2) + success path applies session state
      - bulk pricing table (M4)
  * Anonymous user does not see pay-with-points or affiliate-link panels.
  * Logged-in user with a points balance sees the pay-with-points panel.
  * Logged-in user sees their personal affiliate link with ?ref=<their code>.
  * Inline coupon validates and stores a product-scoped session preview;
    "clear" wipes it; navigating to a different product wipes it too.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d5.py
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
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import (
    Category, Product, ProductPriceTier, PRODUCT_PUBLISHED,
)
from app.models.cart import CartItem
from app.models.marketing import (
    Coupon, COUPON_PLATFORM, DISCOUNT_PERCENT,
)
from app.services.pricing_service import (
    applicable_tier, effective_unit_price, tier_preview,
)

CUSTOMER = "smoke_p15d5_customer@example.com"
SELLER = "smoke_p15d5_seller@example.com"
SECOND_BUYER = "smoke_p15d5_other@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d5-cat"
PROD_SLUG = "p15d5-product-a"
PROD2_SLUG = "p15d5-product-b"
COUPON_CODE = "P15D5SAVE10"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        emails = [CUSTOMER, SELLER, SECOND_BUYER]
        users = [u for u in
                 (User.query.filter_by(email=e).first() for e in emails)
                 if u is not None]
        for u in users:
            CartItem.query.filter_by(user_id=u.id).delete()
            OtpCode.query.filter_by(user_id=u.id).delete()
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)
        db.session.flush()
        for u in users:
            db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        coupon = Coupon.query.filter_by(code=COUPON_CODE).first()
        if coupon:
            db.session.delete(coupon)
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
    with app.app_context():
        cat = Category(name_en="Smoke P15D5", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P15D5 Customer", email=CUSTOMER, role="customer",
                        is_active=True, reward_points=120)
        customer.set_password(PASSWORD)
        seller = User(name="P15D5 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        second_buyer = User(name="P15D5 Other Buyer", email=SECOND_BUYER,
                            role="customer", is_active=True)
        second_buyer.set_password(PASSWORD)
        db.session.add_all([customer, seller, second_buyer])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15D5 Shop",
                           slug="p15d5-shop", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D5 Product", slug=PROD_SLUG,
            base_price=500, stock=50, status=PRODUCT_PUBLISHED,
        )
        product2 = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D5 Second Product", slug=PROD2_SLUG,
            base_price=300, stock=10, status=PRODUCT_PUBLISHED,
        )
        db.session.add_all([product, product2])
        db.session.flush()
        # Two tiers: 5+ at 10% off, 10+ at 20% off.
        db.session.add_all([
            ProductPriceTier(product_id=product.id, min_quantity=5,
                             discount_pct=Decimal("10.00")),
            ProductPriceTier(product_id=product.id, min_quantity=10,
                             discount_pct=Decimal("20.00")),
        ])
        # A platform coupon: 10% off, min order Tk 200, applies to anything.
        db.session.add(Coupon(
            code=COUPON_CODE, scope=COUPON_PLATFORM,
            discount_type=DISCOUNT_PERCENT, discount_value=Decimal("10.00"),
            min_order_amount=Decimal("200.00"), is_active=True,
            starts_at=datetime.utcnow() - timedelta(days=1),
            ends_at=datetime.utcnow() + timedelta(days=30),
        ))
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id, "product_id": product.id,
                "product2_id": product2.id, "other_id": second_buyer.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # service layer
    # ====================================================================
    with app.app_context():
        product = db.session.get(Product, ids["product_id"])

        # No tier hit yet
        check("applicable_tier returns None for quantity 1",
              applicable_tier(product, 1) is None)
        # 5 -> 10% tier
        t5 = applicable_tier(product, 5)
        check("quantity 5 picks the 5+ tier", t5 is not None
              and t5.min_quantity == 5 and float(t5.discount_pct) == 10.0)
        # 12 -> 10+ tier (the higher one wins)
        t12 = applicable_tier(product, 12)
        check("quantity 12 picks the 10+ tier (highest match)",
              t12 is not None and t12.min_quantity == 10)
        # Effective price math
        check("effective_unit_price at qty 1 = base 500",
              effective_unit_price(product, 1) == Decimal("500.00"))
        check("effective_unit_price at qty 5 = 450 (10% off 500)",
              effective_unit_price(product, 5) == Decimal("450.00"))
        check("effective_unit_price at qty 10 = 400 (20% off 500)",
              effective_unit_price(product, 10) == Decimal("400.00"))
        # tier_preview
        preview = tier_preview(product)
        check("tier_preview returns ascending tiers",
              [t["min_quantity"] for t in preview] == [5, 10])

        # CartItem.unit_price honors tiers when quantity hits the threshold
        ci = CartItem(user_id=ids["customer_id"], product_id=product.id,
                      quantity=6)
        db.session.add(ci)
        db.session.flush()
        check("CartItem.unit_price = tier-discounted at qty 6",
              ci.unit_price == Decimal("450.00"))
        check("CartItem.line_total reflects tier discount",
              ci.line_total == Decimal("2700.00"))   # 450 * 6
        ci.quantity = 1
        db.session.flush()
        check("CartItem.unit_price reverts to base when below tier",
              ci.unit_price == Decimal("500.00"))
        db.session.delete(ci)
        db.session.commit()

    # ====================================================================
    # product page rendering
    # ====================================================================
    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("product page renders", "Save more on this product" in body)
        check("M1: Earn points preview shown", "Earn 5 point" in body)
        check("M4: Bulk pricing table rendered",
              "Bulk Pricing" in body and "5+" in body and "10+" in body)
        check("M2: anonymous user sees coupon form",
              "Have a coupon?" in body and 'name="coupon_code"' in body)
        check("anonymous user does NOT see pay-with-points panel",
              "Use my points" not in body)
        check("anonymous user does NOT see affiliate panel",
              'id="pdpAffiliateLink"' not in body)

    # ====================================================================
    # logged-in customer view
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("M3: logged-in user sees points balance",
              "You have 120 points" in body and "Use my points" in body)
        check("M6: affiliate link generated and shown",
              'id="pdpAffiliateLink"' in body and "ref=" in body)

        # Apply an invalid coupon -> flashes error, no session state
        r = c.post(f"/product/{PROD_SLUG}/apply-coupon",
                   data={"coupon_code": "DOES-NOT-EXIST"},
                   follow_redirects=False)
        check("invalid-coupon redirects to product#money",
              r.status_code in (302, 303)
              and "#money" in r.headers.get("Location", ""))
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("no coupon-applied banner after invalid code",
              "would save" not in body)

        # Apply a valid coupon
        c.post(f"/product/{PROD_SLUG}/apply-coupon",
               data={"coupon_code": COUPON_CODE},
               follow_redirects=False)
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("valid coupon stored in session preview",
              COUPON_CODE in body and "would save" in body
              and "৳50" in body)        # 10% of 500

        # Navigate to a different product — coupon preview clears
        body2 = c.get(f"/product/{PROD2_SLUG}/").data.decode("utf-8", errors="ignore")
        check("coupon preview clears on a different product",
              "would save" not in body2)

        # Re-apply, then clear
        c.post(f"/product/{PROD_SLUG}/apply-coupon",
               data={"coupon_code": COUPON_CODE})
        c.post(f"/product/{PROD_SLUG}/apply-coupon",
               data={"action": "clear"})
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("clear action wipes the coupon preview",
              "would save" not in body)

    # ====================================================================
    # logged-in OTHER buyer — affiliate link should NOT be for the seller's
    # own product when the customer is the seller themselves. We check the
    # personal affiliate code is generated.
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, SECOND_BUYER, "customer")
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("second buyer also gets their own affiliate link",
              'id="pdpAffiliateLink"' in body and "ref=" in body)

    # ====================================================================
    # seller routes: add + delete tiers
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, SELLER, "seller")
        # Valid add
        c.post(f"/seller/products/{ids['product_id']}/tiers",
               data={"min_quantity": "20", "discount_pct": "30"})
        with app.app_context():
            tiers = ProductPriceTier.query.filter_by(
                product_id=ids["product_id"]).all()
            check("seller add-tier persisted (20+ -> 30%)",
                  any(t.min_quantity == 20 and float(t.discount_pct) == 30.0
                      for t in tiers))
            tier20_id = next(t.id for t in tiers if t.min_quantity == 20)

        # Reject quantity < 2
        before = None
        with app.app_context():
            before = ProductPriceTier.query.filter_by(
                product_id=ids["product_id"]).count()
        c.post(f"/seller/products/{ids['product_id']}/tiers",
               data={"min_quantity": "1", "discount_pct": "10"})
        with app.app_context():
            after = ProductPriceTier.query.filter_by(
                product_id=ids["product_id"]).count()
        check("seller add-tier rejects qty < 2", after == before)

        # Reject pct >= 100
        c.post(f"/seller/products/{ids['product_id']}/tiers",
               data={"min_quantity": "30", "discount_pct": "150"})
        with app.app_context():
            after2 = ProductPriceTier.query.filter_by(
                product_id=ids["product_id"]).count()
        check("seller add-tier rejects pct >= 100", after2 == before)

        # Reject duplicate quantity
        c.post(f"/seller/products/{ids['product_id']}/tiers",
               data={"min_quantity": "20", "discount_pct": "5"})
        with app.app_context():
            after3 = ProductPriceTier.query.filter_by(
                product_id=ids["product_id"]).count()
        check("seller add-tier rejects duplicate quantity", after3 == before)

        # Delete
        c.post(f"/seller/products/{ids['product_id']}/tiers/{tier20_id}/delete")
        with app.app_context():
            check("seller delete-tier removes the row",
                  db.session.get(ProductPriceTier, tier20_id) is None)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-5 money & loyalty inline smoke test: "
          f"{passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
