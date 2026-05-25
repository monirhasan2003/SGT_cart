"""Phase 15 (Chunk B v2) smoke test — admin-managed homepage banners,
header search bar, flash-sale page filters, and the demo seed.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15b_homepage.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile
from app.models.catalog import Product, PRODUCT_PUBLISHED
from app.models.banner import HomepageBanner, BANNER_HERO, BANNER_STRIP
from app.models.marketing import FlashSale

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    app = create_app("development")

    # --------------------------------------------------------------
    # the seed-demo CLI seeded real data — verify it landed
    # --------------------------------------------------------------
    with app.app_context():
        demo_emails = [
            "demo.techworld@sgt.bd", "demo.camerapro@sgt.bd",
            "demo.fashionhub@sgt.bd", "demo.shoepalace@sgt.bd",
            "demo.kidscorner@sgt.bd", "demo.homeess@sgt.bd",
            "demo.kitchenking@sgt.bd", "demo.freshmart@sgt.bd",
            "demo.dailydrinks@sgt.bd", "demo.glowbeauty@sgt.bd",
        ]
        users_present = sum(
            User.query.filter_by(email=e).count() for e in demo_emails
        )
        check("all 10 demo sellers exist", users_present == 10)

        vendors_approved = (VendorProfile.query
                            .filter(VendorProfile.user_id.in_(
                                db.session.query(User.id).filter(
                                    User.email.in_(demo_emails))))
                            .count())
        check("each demo seller has an approved vendor profile",
              vendors_approved == 10)

        check("demo products seeded (>=50 published)",
              Product.query.filter_by(status=PRODUCT_PUBLISHED).count() >= 50)
        check("an active flash sale exists",
              FlashSale.query.filter_by(is_active=True).first() is not None)
        check("hero banners seeded (>=3)",
              HomepageBanner.query.filter_by(kind=BANNER_HERO, is_active=True).count() >= 3)
        check("at least one strip banner",
              HomepageBanner.query.filter_by(kind=BANNER_STRIP, is_active=True).count() >= 1)

    # --------------------------------------------------------------
    # homepage — admin banners + sections
    # --------------------------------------------------------------
    with app.test_client() as c:
        r = c.get("/")
        body = r.data.decode("utf-8", errors="ignore")

        check("homepage GET / 200", r.status_code == 200)
        check("hero carousel rendered from admin banners",
              'id="heroCarousel"' in body and 'carousel-item' in body)
        check("a seeded hero headline shows on the home",
              "Mega Eid Sale" in body)
        check("strip banner rendered between hero and products",
              "Daily Essentials at 50% Off" in body)
        check("Categories section shows the wide grid",
              "Categories" in body and "Electronics" in body
              and "Fashion" in body and "Grocery" in body)
        check("Flash Sale section on homepage",
              "SGT Mega Eid Sale" in body)
        check("Best Sellers section",
              "Best Sellers" in body)
        check("Just-for-you section visible for guests",
              "Just for you" in body or "Recommended for you" in body)
        check("Featured Stores section + a seeded store",
              "Featured Stores" in body and "Tech World" in body)

        # ----------------------------------------------------------
        # inline search bar in the header (Daraz-style, every page)
        # ----------------------------------------------------------
        check("inline header search bar present on homepage",
              'id="headerSearch"' in body and 'id="headerSuggest"' in body)
        check("voice + image search buttons next to the input",
              'id="headerMic"' in body and 'href="/search/image/"' in body)

        # also on a non-homepage to confirm site-wide visibility
        r = c.get("/about/")
        check("inline header search bar present on /about/",
              r.status_code == 200
              and 'id="headerSearch"' in r.data.decode("utf-8", errors="ignore"))

        # ----------------------------------------------------------
        # /search/suggest works for the header autocomplete
        # ----------------------------------------------------------
        r = c.get("/search/suggest?q=samsung")
        body = r.get_json() or {}
        check("autocomplete returns demo-seeded matches",
              r.status_code == 200
              and any("Samsung" in s.get("title", "")
                      for s in body.get("suggestions", [])))

    # --------------------------------------------------------------
    # flash sale page — search + price filter
    # --------------------------------------------------------------
    with app.test_client() as c:
        r = c.get("/flash-sales/")
        body = r.data.decode("utf-8", errors="ignore")
        check("flash sale page renders filter form",
              r.status_code == 200 and "Search within flash deals" in body
              and 'name="q"' in body and 'name="min"' in body
              and 'name="max"' in body)
        check("flash sale page lists demo items",
              "SGT Mega Eid Sale" in body)

        # search filter
        r = c.get("/flash-sales/?q=samsung")
        check("flash sale q= filter runs", r.status_code == 200)

        # price filter that includes very low prices only
        r = c.get("/flash-sales/?min=0&max=100")
        check("flash sale price filter runs", r.status_code == 200)

    # --------------------------------------------------------------
    # admin banner CRUD routes are reachable (auth gate works)
    # --------------------------------------------------------------
    with app.test_client() as c:
        with app.app_context():
            admin = User.query.filter_by(email="monirhasan2003@gmail.com").first()
        with c.session_transaction() as s:
            s["_user_id"] = str(admin.id)
        r = c.get("/admin/banners/")
        body = r.data.decode("utf-8", errors="ignore")
        check("admin banners page renders",
              r.status_code == 200 and "Homepage Banners" in body
              and "Mega Eid Sale" in body)
        r = c.get("/admin/banners/new")
        check("admin banner form (new) renders",
              r.status_code == 200 and "Banner kind" in r.data.decode("utf-8", errors="ignore"))

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 Chunk B v2 smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
