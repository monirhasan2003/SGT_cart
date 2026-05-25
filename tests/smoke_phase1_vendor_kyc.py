"""Phase 1 smoke test — seller verification (KYC), payout settings, admin review.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase1_vendor_kyc.py <admin_password>
"""
import os
import sys
from io import BytesIO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN

ADMIN_EMAIL = "monirhasan2003@gmail.com"
SELLER_A = "smoke_kyc_a@example.com"
SELLER_B = "smoke_kyc_b@example.com"

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app, email):
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        if u:
            VendorProfile.query.filter_by(user_id=u.id).delete()
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)
            db.session.commit()


def register_seller(app, c, email, shop):
    c.post("/signup/", data={
        "first_name": "KYC", "last_name": "Seller", "email": email,
        "phone": "01700000000", "role": "seller", "shop_name": shop,
        "password": "test1234", "confirm_password": "test1234",
    })


def otp_login(app, c, email):
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
    purge(app, SELLER_A)
    purge(app, SELLER_B)

    # ---- Seller A: register, verify (KYC), payout ----
    with app.test_client() as c:
        register_seller(app, c, SELLER_A, "KYC Test Shop A")
        otp_login(app, c, SELLER_A)

        r = c.get("/seller/")
        check("Seller dashboard before KYC", r.status_code == 200 and b"not verified" in r.data)

        r = c.get("/seller/verification")
        check("Verification form loads", r.status_code == 200)

        r = c.post("/seller/verification", data={
            "business_type": "Individual", "address": "123 Test Road", "city": "Dhaka",
            "trade_license_no": "TL-12345", "nid_number": "NID-99887766",
            "description_en": "A smoke test shop.",
            "trade_license_doc": (BytesIO(b"%PDF-1.4 fake license"), "license.pdf"),
            "nid_doc": (BytesIO(b"fake-nid-image"), "nid.jpg"),
        }, content_type="multipart/form-data")
        check("Verification submitted", r.status_code == 302)
        with app.app_context():
            v = VendorProfile.query.join(User).filter(User.email == SELLER_A).first()
            check("KYC saved to DB", v.is_verification_submitted and v.trade_license_no == "TL-12345")
            check("Documents stored", bool(v.trade_license_doc) and bool(v.nid_doc))

        r = c.post("/seller/payout", data={
            "bkash_number": "01711111111", "nagad_number": "",
            "bank_account_name": "KYC Seller", "bank_account_number": "1234567890",
            "bank_name": "Test Bank",
        })
        check("Payout settings saved", r.status_code == 302)
        with app.app_context():
            v = VendorProfile.query.join(User).filter(User.email == SELLER_A).first()
            check("Payout in DB", v.bkash_number == "01711111111")

    # ---- Seller B: register only (no KYC) ----
    with app.test_client() as c:
        register_seller(app, c, SELLER_B, "KYC Test Shop B")

    with app.app_context():
        va = VendorProfile.query.join(User).filter(User.email == SELLER_A).first()
        vb = VendorProfile.query.join(User).filter(User.email == SELLER_B).first()
        a_id, b_id = va.id, vb.id

    # ---- Admin review ----
    with app.test_client() as c:
        c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})

        r = c.get(f"/admin/vendors/{a_id}/")
        check("Admin sees KYC docs", r.status_code == 200 and b"TL-12345" in r.data
              and b"View Document" in r.data)

        # B has no KYC -> approve must be blocked
        c.post(f"/admin/vendors/{b_id}/approve")
        with app.app_context():
            check("Approve blocked without KYC",
                  db.session.get(VendorProfile, b_id).status == "pending")

        # A has KYC -> approve works
        c.post(f"/admin/vendors/{a_id}/approve")
        with app.app_context():
            check("Approve works with KYC",
                  db.session.get(VendorProfile, a_id).status == "approved")

    purge(app, SELLER_A)
    purge(app, SELLER_B)
    print("(test sellers cleaned up)")

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 1 vendor-KYC smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
