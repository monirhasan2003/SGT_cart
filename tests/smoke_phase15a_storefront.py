"""Phase 15 (Chunk A) smoke test — branding, menu, footer, static pages.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15a_storefront.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    app = create_app("development")
    static_pages = ["/about/", "/contact/", "/faq/", "/privacy/", "/terms/",
                    "/returns/", "/shipping/", "/sell/"]

    with app.test_client() as c:
        # ------------------------------------------------------------------
        # all 8 static pages render
        # ------------------------------------------------------------------
        for path in static_pages:
            r = c.get(path)
            check(f"GET {path} -> 200", r.status_code == 200)

        # ------------------------------------------------------------------
        # homepage / chrome
        # ------------------------------------------------------------------
        r = c.get("/")
        body = r.data.decode("utf-8", errors="ignore")

        check("homepage shows the SGT brand line",
              "SGT Cart" in body)
        check("homepage navbar exposes the cleaned-up menu",
              "Flash Sales" in body and "Sell on SGT" in body
              and 'href="/about/"' in body and 'href="/contact/"' in body)
        check("homepage navbar drops the KUMO theme demo links",
              "Home 1" not in body and "Shop Style 01" not in body
              and "Blog Detail" not in body)
        check("top bar uses BDT, not $USD",
              "৳ BDT" in body and "$USD" not in body)
        check("top bar language toggle has English + Bangla only",
              "English" in body and "বাংলা" in body
              and "Français" not in body and "اللغة العربية" not in body)
        check("footer carries the SGT support email",
              "support@sgtcart.com" in body)
        check("footer payments line lists local methods",
              "bKash" in body and "Nagad" in body)
        check("no leftover KUMO brand text in the rendered HTML",
              "KUMO" not in body and "Kumo" not in body
              and "kumo" not in body)

        # ------------------------------------------------------------------
        # static page content sanity
        # ------------------------------------------------------------------
        about = c.get("/about/").data.decode("utf-8", errors="ignore")
        check("About page mentions Bangladesh",
              "Bangladesh" in about)
        terms = c.get("/terms/").data.decode("utf-8", errors="ignore")
        check("Terms page mentions sellers / commission",
              "commission" in terms.lower() and "seller" in terms.lower())
        sell = c.get("/sell/").data.decode("utf-8", errors="ignore")
        check("Sell on SGT links to seller signup",
              "/signup/?role=seller" in sell)

        # ------------------------------------------------------------------
        # ?role=seller pre-selects the seller tab on signup
        # ------------------------------------------------------------------
        signup = c.get("/signup/?role=seller").data.decode("utf-8", errors="ignore")
        # The seller radio carries `checked` only when initial role is seller.
        seller_idx = signup.find('id="role_seller"')
        block = signup[seller_idx:seller_idx + 400] if seller_idx >= 0 else ""
        check("/signup/?role=seller pre-checks the seller radio",
              'value="seller"' in block and "checked" in block)

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 Chunk A storefront smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
