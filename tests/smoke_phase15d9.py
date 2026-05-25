"""Phase 15 Chunk D-9 smoke test — BD / Local features.

Covers:
  * `delivery_eta_service.eta_for_district` — case-insensitive lookup;
    falls back to (DEFAULT_MIN, DEFAULT_MAX, None) for unknown districts.
  * `bd_calendar_service.hijri_from_gregorian` — Kuwaiti algorithm
    matches the known mapping of a fixed date.
  * `bengali_digits` and `format_hijri_and_gregorian` produce the
    "৪ Ramadan / 14 March" surface.
  * `campaign_service.active_campaign` — gated by the platform settings
    and the end-date being in the future.
  * Address form persists the new `prayer_time_delivery` checkbox.
  * Product page renders:
      - district-specific ETA when the buyer has a default address,
      - same-city seller badge when the cities match,
      - prayer-time delivery line when the buyer's flag is on,
      - campaign strip + countdown JS when a campaign is active,
      - Hijri date in the Delivery card.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d9.py
"""
import os
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.district import DistrictEta
from app.services import (
    delivery_eta_service, bd_calendar_service, campaign_service,
)
from app.services.delivery_eta_service import DEFAULT_MIN, DEFAULT_MAX
from app.services.settings_service import set_setting

CUSTOMER = "smoke_p15d9_customer@example.com"
SELLER = "smoke_p15d9_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d9-cat"
PROD_SLUG = "p15d9-product-a"
TEST_DISTRICT = "Sylhet"     # one of the seeds
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        users = [u for u in
                 (User.query.filter_by(email=e).first()
                  for e in (CUSTOMER, SELLER))
                 if u is not None]
        for u in users:
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
        # Wipe the campaign settings so each test run starts clean.
        for key in ("campaign_label_en", "campaign_label_bn", "campaign_ends_at"):
            set_setting(key, "")
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
        cat = Category(name_en="Smoke P15D9", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P15D9 Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P15D9 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        vp = VendorProfile(
            user_id=seller.id, shop_name_en="P15D9 Shop",
            slug="p15d9-shop", status=VENDOR_APPROVED,
            commission_rate=10, city="Sylhet",
        )
        db.session.add(vp)
        db.session.flush()
        product = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D9 Product", slug=PROD_SLUG,
            base_price=400, stock=10, status=PRODUCT_PUBLISHED,
        )
        db.session.add(product)
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id, "product_id": product.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # delivery_eta_service
    # ====================================================================
    with app.app_context():
        # Seeded district resolves (CLI ran in dev).
        seed_row = DistrictEta.query.filter(
            DistrictEta.district.ilike(TEST_DISTRICT)).first()
        if seed_row is None:
            # Make the test self-sufficient: seed it directly.
            db.session.add(DistrictEta(district=TEST_DISTRICT,
                                        min_days=4, max_days=5))
            db.session.commit()
        mn, mx, matched = delivery_eta_service.eta_for_district("sylhet")
        check("eta_for_district resolves case-insensitively",
              matched and matched.lower() == "sylhet" and mn <= mx)
        mn, mx, matched = delivery_eta_service.eta_for_district("not-a-district")
        check("eta_for_district falls back to default for unknown",
              matched is None and mn == DEFAULT_MIN and mx == DEFAULT_MAX)
        mn, mx, matched = delivery_eta_service.eta_for_district("")
        check("eta_for_district falls back when input is blank",
              matched is None)

    # ====================================================================
    # bd_calendar_service
    # ====================================================================
    h_year, h_month, h_day, month_name = bd_calendar_service.hijri_from_gregorian(
        date(2024, 3, 14)
    )
    # 14 March 2024 is ~ 4 Ramadan 1445 per the Kuwaiti tabular calendar.
    check("Hijri conversion: 14 Mar 2024 -> Ramadan 1445",
          month_name == "Ramadan" and h_year == 1445 and 1 <= h_day <= 5,
          f"got {h_year}-{h_month}-{h_day} ({month_name})")
    check("bengali_digits maps ASCII digits to Bengali",
          bd_calendar_service.bengali_digits(2024) == "২০২৪")
    label = bd_calendar_service.format_hijri_and_gregorian(date(2024, 3, 14))
    check("format_hijri_and_gregorian renders both calendars",
          "Ramadan" in label and "March" in label and "১৪" not in label
          and any(c in label for c in "০১২৩৪৫৬৭৮৯"))

    # ====================================================================
    # campaign_service
    # ====================================================================
    with app.app_context():
        # No campaign set
        check("active_campaign returns None when nothing configured",
              campaign_service.active_campaign() is None)
        # Set + activate
        future = (datetime.utcnow() + timedelta(days=3)).date()
        set_setting("campaign_label_en", "Eid Special")
        set_setting("campaign_label_bn", "ঈদ স্পেশাল")
        set_setting("campaign_ends_at", future.isoformat())
        db.session.commit()
        c = campaign_service.active_campaign()
        check("active_campaign returns dict when configured + future",
              c is not None and c.get("label_en") == "Eid Special"
              and c.get("label_bn") == "ঈদ স্পেশাল")
        # Past end date deactivates
        past = (datetime.utcnow() - timedelta(days=1)).date()
        set_setting("campaign_ends_at", past.isoformat())
        db.session.commit()
        check("active_campaign hides when end-date already passed",
              campaign_service.active_campaign() is None)
        # Restore active for the rendering checks below
        set_setting("campaign_ends_at", future.isoformat())
        db.session.commit()

    # ====================================================================
    # address form persists prayer_time_delivery
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")
        c.post("/addresses/new", data={
            "label": "Home", "full_name": "P15D9 Customer",
            "phone": "01700000099", "address_line": "1 Sylhet Lane",
            "area": "Zindabazar", "city": "Sylhet", "district": "Sylhet",
            "postal_code": "3100", "is_default": "y",
            "prayer_time_delivery": "y",
        }, follow_redirects=True)
        with app.app_context():
            addr = Address.query.filter_by(user_id=ids["customer_id"]).first()
            check("address persists prayer_time_delivery=true",
                  addr is not None and addr.prayer_time_delivery is True)

    # ====================================================================
    # product page rendering
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("campaign strip rendered when active",
              "pdp-campaign-strip" in body and "Eid Special" in body
              and "ঈদ স্পেশাল" in body)
        check("campaign countdown JS hook present",
              'id="pdpCampaignCountdown"' in body
              and "data-ends-at" in body)
        check("district-specific ETA shown",
              "Sylhet" in body and "days" in body)
        check("same-city seller badge shown when buyer city == seller city",
              "Same-city seller" in body and "একই শহরের সেলার" in body)
        check("prayer-time line shown when buyer opted in",
              "Avoiding Jumma" in body)
        check("Hijri date line shown",
              "pdp-hijri" in body and "Ramadan" in body or any(
                  m in body for m in bd_calendar_service.HIJRI_MONTHS
              ))
        # Bengali digits appear at least somewhere in the hijri label.
        check("Hijri label uses Bengali digits",
              any(c in body for c in "০১২৩৪৫৬৭৮৯"))

    # Anonymous user: no district override, no same-city badge.
    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("anonymous user: no same-city badge",
              "Same-city seller" not in body)
        check("anonymous user: no prayer-time line",
              "Avoiding Jumma" not in body)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-9 BD/Local features smoke test: "
          f"{passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
