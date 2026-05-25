"""Phase 5 smoke test — vendor wallet, earnings settlement, payout requests.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase5_wallet.py <admin_password>
"""
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.cart import CartItem
from app.models.order import Order, SubOrder
from app.models.wallet import VendorWallet, PayoutRequest
from app.models.marketing import RewardLedger
from app.services.order_service import place_order

ADMIN_EMAIL = "monirhasan2003@gmail.com"
CUSTOMER = "smoke_wallet_customer@example.com"
SELLER_B = "smoke_wallet_seller@example.com"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        cust = User.query.filter_by(email=CUSTOMER).first()
        if cust:
            RewardLedger.query.filter_by(user_id=cust.id).delete()
            for o in Order.query.filter_by(customer_id=cust.id).all():
                db.session.delete(o)
            CartItem.query.filter_by(user_id=cust.id).delete()
            Address.query.filter_by(user_id=cust.id).delete()
            OtpCode.query.filter_by(user_id=cust.id).delete()
            db.session.delete(cust)
            db.session.commit()
        sb = User.query.filter_by(email=SELLER_B).first()
        if sb:
            if sb.vendor_profile:
                PayoutRequest.query.filter_by(vendor_id=sb.vendor_profile.id).delete()
            OtpCode.query.filter_by(user_id=sb.id).delete()
            db.session.delete(sb)
            db.session.commit()


def seller_login(app, c, email):
    c.post("/login/", data={"email": email, "password": "test1234", "account_type": "seller"})
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query.filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
    c.post("/verify-otp/", data={"code": otp.code})


def main():
    admin_password = sys.argv[1] if len(sys.argv) > 1 else ""
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)

    # setup: customer + order from seller B (1000 base, 10% commission -> 900 earning)
    with app.app_context():
        cust = User(name="Wallet Buyer", email=CUSTOMER, role="customer",
                    is_active=True, is_email_verified=True)
        cust.set_password("test1234")
        db.session.add(cust)
        db.session.flush()
        addr = Address(user_id=cust.id, full_name="Wallet Buyer", phone="01700000000",
                       address_line="1 Rd", city="Dhaka", is_default=True)
        db.session.add(addr)

        sbu = User(name="Wallet Seller", email=SELLER_B, role="seller",
                   is_active=True, is_email_verified=True)
        sbu.set_password("test1234")
        db.session.add(sbu)
        db.session.flush()
        vb = VendorProfile(user_id=sbu.id, shop_name_en="Wallet Shop", slug="wallet-shop",
                           status=VENDOR_APPROVED, commission_rate=Decimal("10.00"),
                           bkash_number="01799999999")
        db.session.add(vb)
        db.session.flush()
        cat_id = Category.query.first().id
        pb = Product(vendor_id=vb.id, category_id=cat_id, title_en="Wallet Product",
                     slug="wallet-product", base_price=Decimal("1000.00"),
                     stock=50, status=PRODUCT_PUBLISHED)
        db.session.add(pb)
        db.session.flush()
        db.session.add(CartItem(user_id=cust.id, product_id=pb.id, quantity=1))
        db.session.commit()

        order = place_order(cust, addr, "cod")
        suborder_id = order.suborders[0].id
        vendor_id = vb.id

        wallet = VendorWallet.query.filter_by(vendor_id=vendor_id).first()
        check("Wallet credited on order (pending = 900)",
              wallet is not None and wallet.pending_balance == Decimal("900.00"),
              str(wallet.pending_balance) if wallet else "no wallet")
        check("Available balance still 0", wallet.available_balance == Decimal("0.00"))

    # seller marks the sub-order delivered -> settlement
    with app.test_client() as c:
        seller_login(app, c, SELLER_B)
        c.post(f"/seller/orders/{suborder_id}/status", data={"status": "delivered"})
        with app.app_context():
            w = VendorWallet.query.filter_by(vendor_id=vendor_id).first()
            check("Delivery settles pending -> available",
                  w.available_balance == Decimal("900.00") and w.pending_balance == Decimal("0.00"))
            check("Total earned recorded", w.total_earned == Decimal("900.00"))

        # earnings page renders
        r = c.get("/seller/earnings/")
        check("Seller earnings page", r.status_code == 200 and b"Available Balance" in r.data)

        # request a payout of 500
        r = c.post("/seller/earnings/", data={"amount": "500", "method": "bkash"})
        with app.app_context():
            w = VendorWallet.query.filter_by(vendor_id=vendor_id).first()
            pr = PayoutRequest.query.filter_by(vendor_id=vendor_id).order_by(PayoutRequest.id.desc()).first()
            check("Payout request created", pr is not None and pr.amount == Decimal("500.00"))
            check("Available reduced after request (900 - 500 = 400)",
                  w.available_balance == Decimal("400.00"), str(w.available_balance))
            payout_id = pr.id

        # request another payout of 300 (to be rejected)
        c.post("/seller/earnings/", data={"amount": "300", "method": "bkash"})
        with app.app_context():
            w = VendorWallet.query.filter_by(vendor_id=vendor_id).first()
            reject_pr = PayoutRequest.query.filter_by(vendor_id=vendor_id).order_by(PayoutRequest.id.desc()).first()
            check("Available reduced again (400 - 300 = 100)",
                  w.available_balance == Decimal("100.00"), str(w.available_balance))
            reject_id = reject_pr.id

    # admin approves one, rejects the other
    with app.test_client() as c:
        c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})
        r = c.get("/admin/payouts/")
        check("Admin payouts page", r.status_code == 200 and b"Wallet Shop" in r.data)

        c.post(f"/admin/payouts/{payout_id}/approve")
        with app.app_context():
            check("Payout approved", db.session.get(PayoutRequest, payout_id).status == "approved")

        c.post(f"/admin/payouts/{reject_id}/reject", data={"note": "test reject"})
        with app.app_context():
            check("Payout rejected", db.session.get(PayoutRequest, reject_id).status == "rejected")
            w = VendorWallet.query.filter_by(vendor_id=vendor_id).first()
            check("Rejected amount refunded (100 + 300 = 400)",
                  w.available_balance == Decimal("400.00"), str(w.available_balance))

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 5 wallet smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
