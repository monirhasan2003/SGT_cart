"""Phase 2 smoke test — DB-backed storefront (catalog, detail, search, filter).

Assumes `flask seed-catalog` and `flask seed-products` have been run.
Run:  venv\\Scripts\\python.exe tests\\smoke_phase2_storefront.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models.catalog import Product, PRODUCT_PUBLISHED

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    app = create_app("development")

    with app.app_context():
        published = Product.query.filter_by(status=PRODUCT_PUBLISHED).count()
        check("Published products exist", published >= 10, f"{published} published")

    with app.test_client() as c:
        r = c.get("/shop/")
        # Catalog now has many demo products — page 1 is paginated by 12.
        # Just check the shop renders product cards.
        check("GET /shop/",
              r.status_code == 200 and b'href="/product/' in r.data)

        # The seed-products demo data leaves an "iPhone 13 Pro Max" listing —
        # search for it explicitly so pagination can't hide it.
        r = c.get("/shop/?q=iphone")
        check("Search ?q=iphone", r.status_code == 200 and b"iPhone" in r.data)

        r = c.get("/shop/?q=zzzznomatch")
        check("Empty search shows 'No products'",
              r.status_code == 200 and b"No products found" in r.data)

        r = c.get("/shop/?category=electronics&q=iphone")
        check("Category filter (electronics)",
              r.status_code == 200 and b"iPhone" in r.data)

        # Fashion filter — the seed-products "Women Summer Dress" lives in
        # Women's Wear (a child of Fashion).
        r = c.get("/shop/?category=fashion&q=summer")
        check("Category filter (fashion)",
              r.status_code == 200 and b"Summer Dress" in r.data)

        r = c.get("/shop/?min=100000")
        check("Price filter (min=100000)",
              r.status_code == 200 and b"iPhone 13 Pro Max" in r.data
              and b"Kids Cartoon" not in r.data)

        r = c.get("/product/iphone-13-pro-max/")
        check("Product detail page",
              r.status_code == 200 and b"iPhone 13 Pro Max" in r.data
              and b"SGT Demo Store" in r.data)

        r = c.get("/product/this-slug-does-not-exist/")
        check("Unknown product -> 404", r.status_code == 404)

        # the homepage Shop nav link now points to /shop/
        r = c.get("/")
        check("Home nav links to /shop/", r.status_code == 200 and b'href="/shop/"' in r.data)

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 2 storefront smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
