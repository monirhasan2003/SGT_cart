"""Phase 9 (Chunk D) smoke test — referral, affiliate & abandoned-cart recovery.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase9_referral.py
"""
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.cart import CartItem
from app.models.order import Order
from app.models.marketing import (
    Referral, AffiliateCommission, AbandonedCart, RewardLedger,
)
from app.services import referral_service, abandoned_cart_service
from app.services.order_service import place_order

REFERRER = "smoke_p9d_referrer@example.com"
REFEREE = "smoke_p9d_referee@example.com"
BUYER = "smoke_p9d_buyer@example.com"
SELLER = "smoke_p9d_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p9d-cat"
EMAILS = (REFERRER, REFEREE, BUYER, SELLER)
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        users = [u for u in
                 (User.query.filter_by(email=e).first() for e in EMAILS)
                 if u is not None]
        uids = [u.id for u in users]
        if uids:
            Referral.query.filter(
                db.or_(Referral.referrer_id.in_(uids),
                       Referral.referee_id.in_(uids))).delete(synchronize_session=False)
            AffiliateCommission.query.filter(
                AffiliateCommission.affiliate_id.in_(uids)).delete(synchronize_session=False)
            AbandonedCart.query.filter(
                AbandonedCart.user_id.in_(uids)).delete(synchronize_session=False)
        for u in users:
            RewardLedger.query.filter_by(user_id=u.id).delete()
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
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


def seed(app):
    with app.app_context():
        cat = Category(name_en="Smoke P9D Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        referrer = User(name="P9D Referrer", email=REFERRER, role="customer",
                        is_active=True)
        referrer.set_password(PASSWORD)
        buyer = User(name="P9D Buyer", email=BUYER, role="customer", is_active=True)
        buyer.set_password(PASSWORD)
        seller = User(name="P9D Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([referrer, buyer, seller])
        db.session.flush()
        for uid in (referrer.id, buyer.id):
            db.session.add(Address(user_id=uid, full_name="P9D", phone="01700000007",
                                   address_line="4 Test Blvd", city="Dhaka",
                                   is_default=True))
        vp = VendorProfile(user_id=seller.id, shop_name_en="P9D Store",
                           slug="p9d-store", status=VENDOR_APPROVED, commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(vendor_id=vp.id, category_id=cat.id, title_en="P9D Product",
                          slug="p9d-product", base_price=500, stock=99,
                          status=PRODUCT_PUBLISHED)
        db.session.add(product)
        db.session.commit()
        return {"referrer_id": referrer.id, "buyer_id": buyer.id,
                "product_id": product.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # referral codes
    # ====================================================================
    with app.app_context():
        referrer = db.session.get(User, ids["referrer_id"])
        code = referral_service.ensure_code(referrer)
        check("referral code generated", bool(code) and len(code) == 8)
        check("ensure_code is idempotent",
              referral_service.ensure_code(referrer) == code)
        check("find_by_code resolves the referrer",
              referral_service.find_by_code(code).id == referrer.id)
        referrer_code = code

    # ====================================================================
    # signup with a referral code (web)
    # ====================================================================
    with app.test_client() as c:
        c.post("/signup/", data={
            "first_name": "P9D", "last_name": "Referee", "email": REFEREE,
            "phone": "01700000008", "role": "customer", "password": PASSWORD,
            "confirm_password": PASSWORD, "referral_code": referrer_code,
        })
    with app.app_context():
        referee = User.query.filter_by(email=REFEREE).first()
        check("referee account created via signup", referee is not None)
        check("referee got their own referral code", bool(referee.referral_code))
        referral = Referral.query.filter_by(referee_id=referee.id).first()
        check("referral recorded at signup",
              referral is not None and referral.referrer_id == ids["referrer_id"]
              and referral.is_rewarded is False)
        referee_id = referee.id

    # ====================================================================
    # referrer rewarded on the referee's first order
    # ====================================================================
    with app.app_context():
        referee = db.session.get(User, referee_id)
        db.session.add(CartItem(user_id=referee.id, product_id=ids["product_id"],
                                quantity=1))
        db.session.add(Address(user_id=referee.id, full_name="P9D Referee",
                               phone="01700000008", address_line="5 Test St",
                               city="Dhaka", is_default=True))
        db.session.commit()
        referee = db.session.get(User, referee_id)
        address = Address.query.filter_by(user_id=referee.id).first()
        before = db.session.get(User, ids["referrer_id"]).reward_points

        place_order(referee, address, "cod")
        referrer = db.session.get(User, ids["referrer_id"])
        check("referrer earned the referral reward",
              referrer.reward_points == before + referral_service.REFERRAL_REWARD_POINTS)
        check("referral marked rewarded",
              Referral.query.filter_by(referee_id=referee_id).first().is_rewarded)

    # ====================================================================
    # abandoned-cart detection
    # ====================================================================
    with app.app_context():
        buyer = db.session.get(User, ids["buyer_id"])
        stale = CartItem(user_id=buyer.id, product_id=ids["product_id"], quantity=2)
        stale.created_at = datetime.utcnow() - timedelta(hours=10)
        db.session.add(stale)
        db.session.commit()

        detected, _ = abandoned_cart_service.scan()
        check("abandoned-cart scan detects the stale cart", detected >= 1)
        record = AbandonedCart.query.filter_by(user_id=ids["buyer_id"]).first()
        check("abandoned cart recorded with its value",
              record is not None and record.item_count == 1
              and not record.is_recovered)

    # ====================================================================
    # affiliate commission + abandoned-cart recovery on purchase
    # ====================================================================
    with app.app_context():
        buyer = db.session.get(User, ids["buyer_id"])
        address = Address.query.filter_by(user_id=buyer.id).first()
        before = db.session.get(User, ids["referrer_id"]).reward_points

        # buyer checks out through the referrer's affiliate link
        order = place_order(buyer, address, "cod", affiliate_code=referrer_code)
        referrer = db.session.get(User, ids["referrer_id"])
        check("affiliate commission credited to the referrer",
              referrer.reward_points > before)
        check("affiliate commission recorded",
              AffiliateCommission.query.filter_by(
                  affiliate_id=ids["referrer_id"], order_id=order.id).first()
              is not None)
        record = AbandonedCart.query.filter_by(user_id=ids["buyer_id"]).first()
        check("abandoned cart marked recovered after the order",
              record is not None and record.is_recovered)

        # self-affiliate must not pay out
        n_before = AffiliateCommission.query.count()
        pts = referral_service.record_affiliate_commission(buyer.referral_code, order)
        check("self-referral earns no affiliate commission",
              pts == 0 and AffiliateCommission.query.count() == n_before)
        db.session.rollback()

    # ====================================================================
    # web Refer & Earn page + REST API
    # ====================================================================
    with app.test_client() as c:
        with c.session_transaction() as s:
            s["_user_id"] = str(ids["referrer_id"])
        r = c.get("/refer/")
        check("web Refer & Earn page renders",
              r.status_code == 200 and referrer_code.encode() in r.data)

    with app.test_client() as c:
        token = api_token(app, c, REFERRER)
        r = c.get("/api/v1/referral", headers={"Authorization": f"Bearer {token}"})
        body = r.get_json() or {}
        check("API /referral returns code + stats",
              r.status_code == 200 and body.get("code") == referrer_code
              and body.get("referral_count", 0) >= 1
              and body.get("affiliate_sales", 0) >= 1)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 9 referral smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
