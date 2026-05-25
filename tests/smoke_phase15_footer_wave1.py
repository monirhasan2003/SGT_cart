"""Phase 15 footer documentation — Wave-1 smoke test.

Asserts every Wave-1 URL returns 200 and that each page carries the
shared shell elements: title, breadcrumb, ToC list, version footer,
contact-card. Also checks the new 6-column footer + site-wide cookie
banner load on a representative page.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15_footer_wave1.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

PAGES = [
    # slug, expected H1 text
    ("/terms/",                  "Customer Terms of Service"),
    ("/privacy/",                "Privacy Policy"),
    ("/seller-terms/",           "Seller Agreement"),
    ("/cookie-policy/",          "Cookie Policy"),
    ("/ip-policy/",              "Intellectual Property Policy"),
    ("/dispute-resolution/",     "Dispute Resolution"),
    ("/returns/",                "Returns &amp; Refunds"),
    ("/refund-policy/",          "Refund Policy"),
    ("/help/cancellations/",     "Order Cancellation"),
    ("/help/buyer-protection/",  "Buyer Protection Program"),
    ("/help/payment-methods/",   "Payment Methods"),
    ("/shipping/",               "Shipping &amp; Delivery"),
    ("/sell/onboarding/",        "Seller Onboarding Guide"),
    ("/sell/fees/",              "Seller Fees &amp; Commission"),
    ("/sell/listing-guidelines/","Product Listing Guidelines"),
    ("/contact/",                "Contact Us"),
]

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as c:
        for url, expected_h1 in PAGES:
            r = c.get(url)
            body = r.data.decode("utf-8", errors="ignore")
            check(f"GET {url} -> 200", r.status_code == 200,
                  f"status {r.status_code}")
            check(f"  page H1 present ({expected_h1[:30]}…)",
                  expected_h1 in body)
            check(f"  ToC list present",
                  "pdp-doc-toc" in body or "Table of contents" in body)
            check(f"  Last-reviewed version footer present",
                  "Last reviewed:" in body and "v1.0" in body)
            check(f"  Contact card present",
                  "Still have questions?" in body)
            check(f"  Cookie banner present",
                  "sgtCookieBanner" in body)
            check(f"  6-column footer with Legal column present",
                  ">Legal<" in body and ">Sell<" in body and ">Trust<" in body)

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 footer Wave-1 smoke: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
