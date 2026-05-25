"""Phase 8 (Chunk C) smoke test — live order tracking, notifications, push.

Covers the notification service, order-placement + status-change notifications,
the tracking timeline, the REST API (notifications + device tokens), the web
notifications page, and graceful FCM degradation.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase8_notifications.py
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
from app.models.order import Order, SubOrder, SubOrderEvent
from app.models.notification import Notification, NOTIF_SYSTEM
from app.models.marketing import RewardLedger
from app.services.order_service import place_order, update_suborder_status
from app.services.notification_service import notify, unread_count, mark_all_read
from app.services import push_service

CUSTOMER = "smoke_p8c_customer@example.com"
SELLER = "smoke_p8c_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p8c-cat"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for email in (CUSTOMER, SELLER):
            u = User.query.filter_by(email=email).first()
            if not u:
                continue
            # Reward-ledger rows reference orders — clear them first.
            RewardLedger.query.filter_by(user_id=u.id).delete()
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)            # cascades sub-orders, events, items
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)                # cascades notifications, device tokens
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


def seed(app):
    with app.app_context():
        cat = Category(name_en="Smoke P8C Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P8C Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P8C Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        db.session.add(Address(user_id=customer.id, full_name="P8C Customer",
                               phone="01700000003", address_line="9 Test Ave",
                               city="Dhaka", is_default=True))
        vp = VendorProfile(user_id=seller.id, shop_name_en="P8C Smoke Store",
                           slug="p8c-smoke-store", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(vendor_id=vp.id, category_id=cat.id,
                          title_en="P8C Smoke Product", slug="p8c-smoke-product",
                          base_price=400, stock=10, status=PRODUCT_PUBLISHED)
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
    # notification service
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        notify(customer.id, NOTIF_SYSTEM, "Test notice", "Hello there", url="/")
        db.session.commit()
        check("notify() creates an in-app notification",
              Notification.query.filter_by(user_id=customer.id).count() == 1)
        check("unread_count reflects the new notification",
              unread_count(customer.id) == 1)
        mark_all_read(customer.id)
        check("mark_all_read clears the unread count", unread_count(customer.id) == 0)

    # ====================================================================
    # push service degrades gracefully (no Firebase configured)
    # ====================================================================
    with app.app_context():
        check("push disabled without Firebase creds", push_service.is_configured() is False)
        check("send_push returns 0 when disabled",
              push_service.send_push(ids["customer_id"], "x", "y") == 0)

    # ====================================================================
    # order placement -> notifications + tracking timeline
    # ====================================================================
    with app.app_context():
        customer = db.session.get(User, ids["customer_id"])
        product = db.session.get(Product, ids["product_id"])
        address = Address.query.filter_by(user_id=customer.id).first()
        db.session.add(CartItem(user_id=customer.id, product_id=product.id, quantity=2))
        db.session.commit()

        order = place_order(customer, address, "cod")
        check("order placed", order is not None and len(order.suborders) == 1)

        check("customer notified of placed order",
              Notification.query.filter_by(user_id=ids["customer_id"]).count() >= 1)
        check("seller notified of new order",
              Notification.query.filter_by(user_id=ids["seller_id"]).count() >= 1)

        sub = order.suborders[0]
        check("tracking timeline started (pending event)",
              len(sub.events) == 1 and sub.events[0].status == "pending")
        sub_id = sub.id
        order_number = order.order_number

    # ====================================================================
    # order status change -> tracking event + customer notification
    # ====================================================================
    with app.app_context():
        sub = db.session.get(SubOrder, sub_id)
        before_notes = Notification.query.filter_by(user_id=ids["customer_id"]).count()

        update_suborder_status(sub, "shipped", note="Handed to courier")
        db.session.commit()
        sub = db.session.get(SubOrder, sub_id)
        check("status change recorded on the timeline",
              len(sub.events) == 2 and sub.events[-1].status == "shipped")
        check("customer notified of status change",
              Notification.query.filter_by(user_id=ids["customer_id"]).count()
              == before_notes + 1)

        update_suborder_status(sub, "delivered")
        db.session.commit()
        sub = db.session.get(SubOrder, sub_id)
        check("delivery recorded on the timeline",
              sub.status == "delivered" and len(sub.events) == 3)
        vp = db.session.get(VendorProfile, ids["vendor_id"])
        check("delivery settled the vendor wallet",
              vp.wallet is not None and vp.wallet.available_balance > Decimal("0"))

    # ====================================================================
    # REST API — notifications + device tokens
    # ====================================================================
    with app.test_client() as c:
        token = api_token(app, c, CUSTOMER)
        auth = {"Authorization": f"Bearer {token}"}
        check("customer API token obtained", bool(token))

        r = c.get("/api/v1/notifications", headers=auth)
        body = r.get_json() or {}
        check("GET /notifications",
              r.status_code == 200 and len(body.get("notifications", [])) >= 3)
        check("notifications report an unread count", "unread" in body)

        r = c.get("/api/v1/notifications/unread-count", headers=auth)
        unread = (r.get_json() or {}).get("unread", 0)
        check("GET /notifications/unread-count", r.status_code == 200 and unread >= 1)

        first_id = body["notifications"][0]["id"]
        r = c.post(f"/api/v1/notifications/{first_id}/read", headers=auth)
        check("POST /notifications/<id>/read", r.status_code == 200)

        r = c.post("/api/v1/notifications/read-all", headers=auth)
        check("POST /notifications/read-all", r.status_code == 200)
        r = c.get("/api/v1/notifications/unread-count", headers=auth)
        check("unread count is zero after read-all",
              (r.get_json() or {}).get("unread") == 0)

        # device token registration
        r = c.post("/api/v1/devices", headers=auth,
                   json={"token": "smoke-fcm-token-p8c", "platform": "android"})
        check("POST /devices registers an FCM token", r.status_code == 201)
        r = c.post("/api/v1/devices", headers=auth,
                   json={"token": "smoke-fcm-token-p8c", "platform": "ios"})
        check("re-registering the same token is idempotent", r.status_code == 201)
        r = c.delete("/api/v1/devices", headers=auth,
                     json={"token": "smoke-fcm-token-p8c"})
        check("DELETE /devices unregisters the token", r.status_code == 200)

        # order detail carries the tracking timeline
        r = c.get(f"/api/v1/orders/{order_number}", headers=auth)
        sub0 = ((r.get_json() or {}).get("order", {}).get("suborders") or [{}])[0]
        check("API order detail includes the tracking timeline",
              r.status_code == 200 and len(sub0.get("tracking", [])) == 3)

        # OpenAPI spec covers the new endpoints
        r = c.get("/api/v1/openapi.json")
        paths = (r.get_json() or {}).get("paths", {})
        check("OpenAPI spec documents chat + notifications",
              "/chat/threads" in paths and "/notifications" in paths
              and "/devices" in paths)

    # ====================================================================
    # web — notifications page + navbar badge
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMER)
        r = c.get("/notifications/")
        check("web notifications page renders",
              r.status_code == 200 and b"Notifications" in r.data)

        r = c.get("/dashboard/")
        check("navbar shows the notification bell",
              r.status_code == 200 and b"js-notif-count" in r.data)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 8 notifications/tracking smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
