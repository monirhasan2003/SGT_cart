"""Phase 1 smoke test — account profile + seller dashboard.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase1_account.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN

CUSTOMER_EMAIL = "smoke_acct_customer@example.com"
SELLER_EMAIL = "smoke_acct_seller@example.com"

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


def login_with_otp(app, c, email, password, account_type="customer"):
    """Full email+password -> OTP -> verified login. Returns True on success."""
    r = c.post("/login/", data={"email": email, "password": password,
                                "account_type": account_type})
    if "verify-otp" not in r.headers.get("Location", ""):
        return False
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query
               .filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
    if not otp:
        return False
    r = c.post("/verify-otp/", data={"code": otp.code})
    return r.status_code == 302 and "verify-otp" not in r.headers.get("Location", "")


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app, CUSTOMER_EMAIL)
    purge(app, SELLER_EMAIL)

    # anonymous cannot view the profile page
    with app.test_client() as anon:
        r = anon.get("/profile-info/")
        check("Anonymous blocked from /profile-info/", r.status_code == 302)

    # ---- customer: register, OTP login, profile, password ----
    with app.test_client() as c:
        r = c.post("/signup/", data={
            "first_name": "Acct", "last_name": "Customer", "email": CUSTOMER_EMAIL,
            "phone": "01710000000", "role": "customer",
            "password": "test1234", "confirm_password": "test1234",
        })
        check("Customer registration", r.status_code == 302)
        check("Customer OTP login", login_with_otp(app, c, CUSTOMER_EMAIL, "test1234"))

        r = c.get("/profile-info/")
        check("GET /profile-info/", r.status_code == 200)

        r = c.post("/profile-info/update", data={
            "first_name": "Renamed", "last_name": "User", "phone": "01999999999",
        })
        with app.app_context():
            u = User.query.filter_by(email=CUSTOMER_EMAIL).first()
            check("Profile update", u.name == "Renamed User" and u.phone == "01999999999")

        r = c.post("/profile-info/change-password", data={
            "current_password": "WRONG", "new_password": "abcdef1", "confirm_password": "abcdef1",
        })
        with app.app_context():
            u = User.query.filter_by(email=CUSTOMER_EMAIL).first()
            check("Wrong current password rejected", u.check_password("test1234"))

        r = c.post("/profile-info/change-password", data={
            "current_password": "test1234", "new_password": "abcdef1", "confirm_password": "abcdef1",
        })
        with app.app_context():
            u = User.query.filter_by(email=CUSTOMER_EMAIL).first()
            check("Password change succeeds", u.check_password("abcdef1"))

    # ---- seller: register, OTP login, dashboard ----
    with app.test_client() as c:
        r = c.post("/signup/", data={
            "first_name": "Acct", "last_name": "Seller", "email": SELLER_EMAIL,
            "phone": "01720000000", "role": "seller", "shop_name": "Acct Test Shop",
            "password": "test1234", "confirm_password": "test1234",
        })
        check("Seller registration", r.status_code == 302)
        check("Seller OTP login", login_with_otp(app, c, SELLER_EMAIL, "test1234", "seller"))

        r = c.get("/seller/")
        check("GET /seller/ dashboard", r.status_code == 200 and b"Acct Test Shop" in r.data)
        check("Dashboard shows verification prompt", b"not verified yet" in r.data)

    purge(app, CUSTOMER_EMAIL)
    purge(app, SELLER_EMAIL)
    print("(test users cleaned up)")

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 1 account/seller smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
