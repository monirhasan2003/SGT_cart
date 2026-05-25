"""Phase 9 (Chunk C) smoke test — flash sales & reward points.

Covers flash-sale activation/restore pricing, loyalty earn-on-delivery and
redeem-at-checkout, the admin flash-sale UI, and the REST API.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase9_promotions.py
"""
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.cart import CartItem
from app.models.order import Order, SubOrder, SUBORDER_DELIVERED
from app.models.marketing import FlashSale, FlashSaleItem, RewardLedger
from app.services import flash_sale_service
from app.services.order_service import place_order, update_suborder_status

ADMIN_EMAIL = "monirhasan2003@gmail.com"
CUSTOMER = "smoke_p9c_customer@example.com"
SELLER = "smoke_p9c_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p9c-cat"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for s in FlashSale.query.filter(FlashSale.title.like("P9C%")).all():
            if s.is_active:
                flash_sale_service.deactivate(s)
            db.session.delete(s)
        db.session.flush()
        for email in (CUSTOMER, SELLER):
            u = User.query.filter_by(email=email).first()
            if not u:
                continue
            RewardLedger.query.filter_by(user_id=u.id).delete()
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)
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


def api_token(app, c, email):
    c.post("/api/v1/auth/login", json={"email": email, "password": PASSWORD})
    r = c.post("/api/v1/auth/verify-otp",
               json={"email": email, "code": latest_otp(app, email)})
    return (r.get_json() or {}).get("access_token")


def web_login(app, c, email):
    c.post("/login/", data={"email": email, "password": PASSWORD,
                            "account_type": "customer"})
    c.post("/verify-otp/", data={"code": latest_otp(app, email)})


def add_cart(app, customer_id, product_id, qty):
    with app.app_context():
        db.session.add(CartItem(user_id=customer_id, product_id=product_id,
                                quantity=qty))
        db.session.commit()


def seed(app):
    with app.app_context():
        cat = Category(name_en="Smoke P9C Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P9C Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P9C Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        db.session.add(Address(user_id=customer.id, full_name="P9C Customer",
                               phone="01700000006", address_line="3 Test Ln",
                               city="Dhaka", is_default=True))
        vp = VendorProfile(user_id=seller.id, shop_name_en="P9C Store",
                           slug="p9c-store", status=VENDOR_APPROVED, commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(vendor_id=vp.id, category_id=cat.id, title_en="P9C Product",
                          slug="p9c-product", base_price=400, stock=99,
                          status=PRODUCT_PUBLISHED)
        db.session.add(product)
        db.session.commit()
        return {"customer_id": customer.id, "product_id": product.id,
                "vendor_id": vp.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)
    with app.app_context():
        admin_id = User.query.filter_by(email=ADMIN_EMAIL).first().id

    # ====================================================================
    # flash sale — activation applies & restores prices
    # ====================================================================
    with app.app_context():
        product = db.session.get(Product, ids["product_id"])
        sale = FlashSale(title="P9C Service Sale", slug="p9c-service-sale")
        db.session.add(sale)
        db.session.flush()
        flash_sale_service.add_item(sale, product, Decimal("250.00"))
        db.session.commit()

        check("product unaffected before activation",
              product.discount_price is None)

        flash_sale_service.activate(sale)
        db.session.commit()
        product = db.session.get(Product, ids["product_id"])
        check("activation applies the flash price",
              product.discount_price == Decimal("250.00")
              and product.current_price == Decimal("250.00"))
        check("flash sale is live", sale in flash_sale_service.live_sales())
        check("product_on_active_sale detects the product",
              flash_sale_service.product_on_active_sale(product.id))

        flash_sale_service.deactivate(sale)
        db.session.commit()
        product = db.session.get(Product, ids["product_id"])
        check("deactivation restores the original price",
              product.discount_price is None)

        # clean this service-test sale up
        db.session.delete(sale)
        db.session.commit()

    # ====================================================================
    # loyalty — earn on delivery
    # ====================================================================
    add_cart(app, ids["customer_id"], ids["product_id"], qty=2)   # 2 × 400 = 800
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        address = Address.query.filter_by(user_id=customer.id).first()
        order = place_order(customer, address, "cod")
        sub_id = order.suborders[0].id

        customer = db.session.get(User, ids["customer_id"])
        check("no points before delivery", customer.reward_points == 0)

        sub = db.session.get(SubOrder, sub_id)
        update_suborder_status(sub, SUBORDER_DELIVERED)
        db.session.commit()
        customer = db.session.get(User, ids["customer_id"])
        check("points earned on delivery (800 / 100 = 8)",
              customer.reward_points == 8)
        check("earn recorded in the ledger",
              RewardLedger.query.filter_by(user_id=customer.id)
              .filter(RewardLedger.points > 0).count() == 1)

        # re-delivering must not double-credit
        update_suborder_status(sub, "shipped")
        db.session.commit()
        update_suborder_status(db.session.get(SubOrder, sub_id), SUBORDER_DELIVERED)
        db.session.commit()
        customer = db.session.get(User, ids["customer_id"])
        check("re-delivery does not double-credit points",
              customer.reward_points == 8)

    # ====================================================================
    # loyalty — redeem at checkout
    # ====================================================================
    add_cart(app, ids["customer_id"], ids["product_id"], qty=1)   # 1 × 400
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        address = Address.query.filter_by(user_id=customer.id).first()
        order = place_order(customer, address, "cod", points_to_redeem=5)
        check("points redeemed at checkout",
              order.points_redeemed == 5
              and order.points_discount == Decimal("5.00"))
        check("order total reduced by the points discount",
              order.total_amount == order.subtotal + order.shipping_fee
              - order.points_discount)
        customer = db.session.get(User, ids["customer_id"])
        check("balance reduced after redeeming (8 - 5 = 3)",
              customer.reward_points == 3)

    add_cart(app, ids["customer_id"], ids["product_id"], qty=1)
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        address = Address.query.filter_by(user_id=customer.id).first()
        order = place_order(customer, address, "cod", points_to_redeem=999)
        check("redemption capped at the available balance",
              order.points_redeemed == 3)

    # ====================================================================
    # admin flash-sale UI
    # ====================================================================
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["_user_id"] = str(admin_id)

        r = c.post("/admin/flash-sales/new",
                   data={"title": "P9C Admin Sale"}, follow_redirects=True)
        check("admin creates a flash sale", r.status_code == 200)
        with app.app_context():
            sale = FlashSale.query.filter_by(title="P9C Admin Sale").first()
            sale_id = sale.id

        r = c.post(f"/admin/flash-sales/{sale_id}/items",
                   data={"product_id": ids["product_id"], "flash_price": "199"},
                   follow_redirects=True)
        check("admin adds a product to the sale", b"199" in r.data)

        r = c.post(f"/admin/flash-sales/{sale_id}/activate", follow_redirects=True)
        check("admin activates the flash sale", b"live" in r.data.lower())
        with app.app_context():
            check("activation applied the admin flash price",
                  db.session.get(Product, ids["product_id"]).discount_price
                  == Decimal("199.00"))

        r = c.post(f"/admin/flash-sales/{sale_id}/deactivate", follow_redirects=True)
        with app.app_context():
            check("deactivation restored the price",
                  db.session.get(Product, ids["product_id"]).discount_price is None)

        # reactivate so the public page + API have something live
        c.post(f"/admin/flash-sales/{sale_id}/activate")

    # ====================================================================
    # public page + REST API
    # ====================================================================
    with app.test_client() as c:
        r = c.get("/flash-sales/")
        check("public flash-sales page renders",
              r.status_code == 200 and b"P9C Admin Sale" in r.data)

        r = c.get("/api/v1/flash-sales")
        sales = (r.get_json() or {}).get("flash_sales", [])
        check("API lists live flash sales",
              r.status_code == 200
              and any(s["title"] == "P9C Admin Sale" for s in sales))

        token = api_token(app, c, CUSTOMER)
        auth = {"Authorization": f"Bearer {token}"}
        r = c.get("/api/v1/rewards", headers=auth)
        body = r.get_json() or {}
        check("API /rewards reports the balance & history",
              r.status_code == 200 and body.get("balance") == 0
              and len(body.get("history", [])) >= 1)

    # ====================================================================
    # web — rewards page + checkout with points
    # ====================================================================
    with app.app_context():
        # give the customer points to spend on the web checkout
        u = db.session.get(User, ids["customer_id"])
        u.reward_points = 50
        db.session.add(RewardLedger(user_id=u.id, points=50, reason="Smoke top-up"))
        db.session.commit()
    add_cart(app, ids["customer_id"], ids["product_id"], qty=1)
    with app.test_client() as c:
        web_login(app, c, CUSTOMER)

        r = c.get("/rewards/")
        check("web rewards page renders",
              r.status_code == 200 and b"reward points balance" in r.data)

        r = c.get("/cart/checkout/")
        check("checkout offers the points option",
              r.status_code == 200 and b"use_points" in r.data)

        with app.app_context():
            addr_id = Address.query.filter_by(user_id=ids["customer_id"]).first().id
        r = c.post("/cart/checkout/", data={"address_id": addr_id,
                                            "payment_method": "cod",
                                            "use_points": "on"},
                   follow_redirects=True)
        check("web checkout with points succeeds", r.status_code == 200)
        with app.app_context():
            o = (Order.query.filter_by(customer_id=ids["customer_id"])
                 .order_by(Order.id.desc()).first())
            check("web order redeemed reward points", o.points_redeemed > 0)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 9 promotions smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
