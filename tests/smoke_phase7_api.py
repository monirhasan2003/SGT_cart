"""Phase 7 smoke test — REST API finalization (catalog, cart, account, seller).

Exercises the customer & seller API surface end-to-end against the Flask test
client, plus the OpenAPI spec / Swagger UI. Login uses the real OTP flow
(emails are sent), mirroring the Phase 1 API test.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase7_api.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, ProductImage, PRODUCT_PUBLISHED
from app.models.order import Order, SubOrder
from app.models.payment import Transaction
from app.models.wallet import PayoutRequest
from app.models.marketing import RewardLedger

CUSTOMER = "smoke_p7_customer@example.com"
SELLER = "smoke_p7_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p7-category"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    """Remove all test data (FK-safe order, ORM cascades via session.delete)."""
    with app.app_context():
        for email in (CUSTOMER, SELLER):
            u = User.query.filter_by(email=email).first()
            if not u:
                continue
            RewardLedger.query.filter_by(user_id=u.id).delete()
            for o in Order.query.filter_by(customer_id=u.id).all():
                Transaction.query.filter_by(order_id=o.id).delete()
                db.session.delete(o)               # cascades sub-orders + items
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for s in SubOrder.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(s)
                PayoutRequest.query.filter_by(vendor_id=vp.id).delete()
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)           # cascades images + variants
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)                   # cascades vendor, wallet, cart, addresses
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()


def latest_otp(app, email):
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query
               .filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
        return otp.code if otp else None


def get_token(app, c, email):
    """Run the OTP login flow and return the JWT access token."""
    c.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
    code = latest_otp(app, email)
    r = c.post("/api/v1/auth/verify-otp", json={"email": email, "code": code})
    return (r.get_json() or {}).get("access_token")


def seed(app):
    """Create a category, an approved seller with a published product, a customer."""
    with app.app_context():
        cat = Category(name_en="Smoke P7 Category", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)

        customer = User(name="P7 Customer", email=CUSTOMER, phone="01700000001",
                        role="customer", is_active=True)
        customer.set_password(PASSWORD)
        db.session.add(customer)

        seller = User(name="P7 Seller", email=SELLER, phone="01700000002",
                      role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add(seller)
        db.session.flush()

        vp = VendorProfile(user_id=seller.id, shop_name_en="P7 Smoke Store",
                           slug="p7-smoke-store", status=VENDOR_APPROVED,
                           commission_rate=10, city="Dhaka")
        db.session.add(vp)
        db.session.flush()

        product = Product(vendor_id=vp.id, category_id=cat.id,
                          title_en="P7 Smoke Product", slug="p7-smoke-product",
                          base_price=500, stock=20, status=PRODUCT_PUBLISHED)
        db.session.add(product)
        db.session.flush()
        db.session.add(ProductImage(product_id=product.id,
                                    image_path="uploads/products/placeholder.jpg",
                                    is_primary=True))
        db.session.commit()
        return product.slug, vp.slug


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    product_slug, store_slug = seed(app)

    with app.test_client() as c:
        # ---- public catalog (no auth) ----
        r = c.get("/api/v1/categories")
        cats = (r.get_json() or {}).get("categories", [])
        check("GET /categories", r.status_code == 200
              and any(x["slug"] == CAT_SLUG for x in cats))

        r = c.get("/api/v1/products")
        check("GET /products", r.status_code == 200
              and "pagination" in (r.get_json() or {}))

        r = c.get(f"/api/v1/products?q=P7 Smoke&category={CAT_SLUG}")
        prods = (r.get_json() or {}).get("products", [])
        check("GET /products with q + category filter",
              r.status_code == 200 and any(p["slug"] == product_slug for p in prods))

        r = c.get(f"/api/v1/products/{product_slug}")
        body = r.get_json() or {}
        check("GET /products/<slug> detail",
              r.status_code == 200
              and body.get("product", {}).get("slug") == product_slug
              and "related" in body.get("product", {}))

        r = c.get("/api/v1/products/does-not-exist")
        check("GET /products/<slug> 404", r.status_code == 404)

        r = c.get("/api/v1/stores")
        stores = (r.get_json() or {}).get("stores", [])
        check("GET /stores", r.status_code == 200
              and any(s["slug"] == store_slug for s in stores))

        r = c.get(f"/api/v1/stores/{store_slug}")
        store = (r.get_json() or {}).get("store", {})
        check("GET /stores/<slug> with products & categories",
              r.status_code == 200 and "products" in store and "categories" in store)

        # ---- auth required ----
        r = c.get("/api/v1/cart")
        check("GET /cart without token (401)", r.status_code == 401)

        # ---- customer flow ----
        token = get_token(app, c, CUSTOMER)
        check("customer JWT obtained", bool(token))
        auth = {"Authorization": f"Bearer {token}"}

        # address CRUD
        r = c.post("/api/v1/addresses", headers=auth, json={
            "full_name": "P7 Customer", "phone": "01700000001",
            "address_line": "12 Test Road", "city": "Dhaka",
        })
        addr = (r.get_json() or {}).get("address", {})
        check("POST /addresses (first = default)",
              r.status_code == 201 and addr.get("is_default") is True)
        address_id = addr.get("id")

        r = c.get("/api/v1/addresses", headers=auth)
        check("GET /addresses", r.status_code == 200
              and len((r.get_json() or {}).get("addresses", [])) == 1)

        r = c.patch(f"/api/v1/addresses/{address_id}", headers=auth, json={
            "full_name": "P7 Customer Edited", "phone": "01700000001",
            "address_line": "12 Test Road", "city": "Chattogram",
        })
        check("PATCH /addresses/<id>",
              r.status_code == 200
              and (r.get_json() or {}).get("address", {}).get("city") == "Chattogram")

        # cart
        r = c.get(f"/api/v1/products/{product_slug}")
        product_id = (r.get_json() or {}).get("product", {}).get("id")
        r = c.post("/api/v1/cart/items", headers=auth,
                   json={"product_id": product_id, "quantity": 2})
        cart = r.get_json() or {}
        check("POST /cart/items", r.status_code == 201 and cart.get("count") == 2)
        item_id = cart["items"][0]["id"]

        r = c.patch(f"/api/v1/cart/items/{item_id}", headers=auth, json={"quantity": 3})
        check("PATCH /cart/items/<id>",
              r.status_code == 200 and (r.get_json() or {}).get("count") == 3)

        r = c.get("/api/v1/cart", headers=auth)
        check("GET /cart has totals",
              r.status_code == 200 and (r.get_json() or {}).get("total", 0) > 0)

        # checkout (COD)
        r = c.post("/api/v1/checkout", headers=auth,
                   json={"address_id": address_id, "payment_method": "cod"})
        body = r.get_json() or {}
        check("POST /checkout (COD)",
              r.status_code == 201
              and body.get("payment", {}).get("status") == "cod"
              and bool(body.get("order", {}).get("order_number")))
        order_number = body.get("order", {}).get("order_number")

        r = c.get("/api/v1/cart", headers=auth)
        check("cart emptied after checkout",
              r.status_code == 200 and (r.get_json() or {}).get("count") == 0)

        r = c.get("/api/v1/orders", headers=auth)
        check("GET /orders", r.status_code == 200
              and len((r.get_json() or {}).get("orders", [])) == 1)

        r = c.get(f"/api/v1/orders/{order_number}", headers=auth)
        check("GET /orders/<number> detail",
              r.status_code == 200
              and "suborders" in (r.get_json() or {}).get("order", {}))

        # customer blocked from seller endpoints
        r = c.get("/api/v1/seller/products", headers=auth)
        check("customer token blocked from /seller/* (403)", r.status_code == 403)

        # ---- seller flow ----
        s_token = get_token(app, c, SELLER)
        s_auth = {"Authorization": f"Bearer {s_token}"}
        check("seller JWT obtained", bool(s_token))

        r = c.get("/api/v1/seller/profile", headers=s_auth)
        check("GET /seller/profile with wallet",
              r.status_code == 200
              and "wallet" in (r.get_json() or {}).get("seller", {}))

        r = c.get("/api/v1/seller/products", headers=s_auth)
        check("GET /seller/products",
              r.status_code == 200
              and len((r.get_json() or {}).get("products", [])) == 1)

        with app.app_context():
            cat_id = Category.query.filter_by(slug=CAT_SLUG).first().id
        r = c.post("/api/v1/seller/products", headers=s_auth, json={
            "title_en": "P7 New Product", "category_id": cat_id,
            "base_price": 999, "stock": 5,
        })
        new_product = (r.get_json() or {}).get("product", {})
        check("POST /seller/products (draft)",
              r.status_code == 201 and new_product.get("status") == "draft")
        new_id = new_product.get("id")

        r = c.patch(f"/api/v1/seller/products/{new_id}", headers=s_auth,
                    json={"base_price": 1200})
        check("PATCH /seller/products/<id>",
              r.status_code == 200
              and (r.get_json() or {}).get("product", {}).get("base_price") == 1200.0)

        # submit without images -> 400
        r = c.post(f"/api/v1/seller/products/{new_id}/submit", headers=s_auth)
        check("submit product without images (400)", r.status_code == 400)

        r = c.post(f"/api/v1/seller/products/{new_id}/variants", headers=s_auth,
                   json={"size": "L", "color": "Red", "price": 1250, "stock": 3})
        check("POST /seller/products/<id>/variants", r.status_code == 201)

        r = c.get("/api/v1/seller/orders", headers=s_auth)
        sub_orders = (r.get_json() or {}).get("orders", [])
        check("GET /seller/orders (has the checkout sub-order)",
              r.status_code == 200 and len(sub_orders) == 1)
        sub_id = sub_orders[0]["id"] if sub_orders else None

        if sub_id:
            r = c.get(f"/api/v1/seller/orders/{sub_id}", headers=s_auth)
            check("GET /seller/orders/<id> detail",
                  r.status_code == 200
                  and "items" in (r.get_json() or {}).get("order", {}))

            r = c.post(f"/api/v1/seller/orders/{sub_id}/status", headers=s_auth,
                       json={"status": "delivered"})
            check("POST /seller/orders/<id>/status -> delivered",
                  r.status_code == 200
                  and (r.get_json() or {}).get("order", {}).get("status") == "delivered")

        r = c.get("/api/v1/seller/earnings", headers=s_auth)
        earn = r.get_json() or {}
        check("GET /seller/earnings (delivery settled wallet)",
              r.status_code == 200 and earn.get("wallet", {}).get("available", 0) > 0)

        # seller blocked from customer-only endpoint
        r = c.get("/api/v1/orders", headers=s_auth)
        check("seller token blocked from /orders (403)", r.status_code == 403)

        # ---- docs ----
        r = c.get("/api/v1/openapi.json")
        spec = r.get_json() or {}
        check("GET /openapi.json valid spec",
              r.status_code == 200
              and spec.get("openapi", "").startswith("3.")
              and len(spec.get("paths", {})) > 20)

        r = c.get("/api/v1/docs")
        check("GET /docs (Swagger UI)",
              r.status_code == 200 and b"swagger-ui" in r.data)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 7 REST API smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
