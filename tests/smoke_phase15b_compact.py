"""Phase 15 (Chunk B v3a) smoke test — compact cards + Shop Load More.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15b_compact.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models.catalog import Product, PRODUCT_PUBLISHED

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    app = create_app("development")

    with app.test_client() as c:
        # ------------------------------------------------------------------
        # homepage uses the compact card (6 per row on desktop)
        # ------------------------------------------------------------------
        r = c.get("/")
        body = r.data.decode("utf-8", errors="ignore")
        check("homepage 200", r.status_code == 200)
        check("compact col-lg-2 cards in use (>= 40)",
              body.count("col-lg-2") >= 40)
        check("old wide col-lg-3 product cards gone",
              "col-lg-3 col-md-4 col-6" not in body)
        check("homepage Categories grid is compact (col-4 col-md-3 col-lg-2)",
              'class="col-4 col-md-3 col-lg-2"' in body)

        # ------------------------------------------------------------------
        # /shop/ — 40/page + Load More button
        # ------------------------------------------------------------------
        r = c.get("/shop/")
        body = r.data.decode("utf-8", errors="ignore")
        check("shop 200", r.status_code == 200)
        check("shop page renders the Load-More button",
              'id="loadMoreBtn"' in body and "Load more products" in body)
        check("old 1/2/3 pagination links removed from shop",
              "pagination justify-content-center" not in body)
        check("shop grid container has the id productsGrid",
              'id="productsGrid"' in body)

        # ------------------------------------------------------------------
        # ?partial=1 returns only product cards (no layout chrome)
        # ------------------------------------------------------------------
        r = c.get("/shop/?partial=1&page=1")
        partial = r.data.decode("utf-8", errors="ignore")
        check("shop partial endpoint returns just cards",
              r.status_code == 200 and "<!DOCTYPE" not in partial
              and "productsGrid" not in partial
              and "col-lg-2" in partial)

        # Page 1 should be at most 40 products.
        with app.app_context():
            total = Product.query.filter_by(status=PRODUCT_PUBLISHED).count()
        expected_p1 = min(40, total)
        n_cards_p1 = partial.count("col-lg-2")
        check(f"shop page 1 partial has up to 40 cards (got {n_cards_p1})",
              n_cards_p1 == expected_p1)

        # Page 2 only when there are >40 products.
        if total > 40:
            r = c.get("/shop/?partial=1&page=2")
            check("shop page 2 partial 200",
                  r.status_code == 200
                  and r.data.decode("utf-8", errors="ignore").count("col-lg-2") > 0)
        else:
            check("shop has <=40 products — no page-2 partial expected",
                  True)

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 Chunk B v3a smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
