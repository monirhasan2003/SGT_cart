"""Phase 1 smoke test — auth core.

Exercises registration, OTP login, admin login, forgot/reset password against
the real app + database. Triggers real Gmail OTP emails (delivery is verified
by SMTP accepting the message). Test data is cleaned up at the end.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase1.py <admin_password>
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN, OTP_PURPOSE_RESET

TEST_EMAIL = "smoke_customer@example.com"
ADMIN_EMAIL = "monirhasan2003@gmail.com"

results = []


def check(name, ok, detail=""):
    results.append(ok)
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    admin_password = sys.argv[1] if len(sys.argv) > 1 else ""

    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False  # CSRF tested separately; off for the harness

    # remove leftovers from a previous run
    with app.app_context():
        stale = User.query.filter_by(email=TEST_EMAIL).first()
        if stale:
            OtpCode.query.filter_by(user_id=stale.id).delete()
            db.session.delete(stale)
            db.session.commit()

    with app.test_client() as c:
        # 1. pages render
        for path in ["/", "/login/", "/signup/", "/forgot-password/"]:
            r = c.get(path)
            check(f"GET {path}", r.status_code == 200, f"status {r.status_code}")

        # 2. admin logs in without OTP
        r = c.post("/login/", data={"email": ADMIN_EMAIL, "password": admin_password})
        loc = r.headers.get("Location", "")
        check("Admin login (no OTP)", r.status_code == 302 and "verify-otp" not in loc,
              f"-> {loc or r.status_code}")
        c.get("/logout/")

        # 3. customer registration
        r = c.post("/signup/", data={
            "first_name": "Smoke", "last_name": "Tester", "email": TEST_EMAIL,
            "phone": "01700000000", "role": "customer",
            "password": "test1234", "confirm_password": "test1234",
        })
        check("Customer registration", r.status_code == 302, f"status {r.status_code}")
        with app.app_context():
            u = User.query.filter_by(email=TEST_EMAIL).first()
            check("Customer row created", u is not None and u.role == "customer")

        # 4. customer login -> OTP
        r = c.post("/login/", data={"email": TEST_EMAIL, "password": "test1234"})
        loc = r.headers.get("Location", "")
        check("Customer login -> OTP page (email sent)",
              r.status_code == 302 and "verify-otp" in loc, f"-> {loc or r.status_code}")

        with app.app_context():
            u = User.query.filter_by(email=TEST_EMAIL).first()
            otp = (OtpCode.query
                   .filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
                   .order_by(OtpCode.id.desc()).first())
            otp_code = otp.code if otp else None
        check("Login OTP generated", otp_code is not None)

        # 5. verify OTP -> logged in
        if otp_code:
            r = c.post("/verify-otp/", data={"code": otp_code})
            loc = r.headers.get("Location", "")
            check("OTP verification -> logged in",
                  r.status_code == 302 and "verify-otp" not in loc, f"-> {loc}")
        c.get("/logout/")

        # 6. wrong password rejected
        r = c.post("/login/", data={"email": TEST_EMAIL, "password": "WRONG"})
        check("Wrong password rejected", r.status_code == 200)

        # 7. forgot password -> reset OTP
        r = c.post("/forgot-password/", data={"email": TEST_EMAIL})
        loc = r.headers.get("Location", "")
        check("Forgot-password -> reset code sent",
              r.status_code == 302 and "reset-password" in loc, f"-> {loc or r.status_code}")
        with app.app_context():
            u = User.query.filter_by(email=TEST_EMAIL).first()
            rotp = (OtpCode.query
                    .filter_by(user_id=u.id, purpose=OTP_PURPOSE_RESET, is_used=False)
                    .order_by(OtpCode.id.desc()).first())
            rotp_code = rotp.code if rotp else None
        check("Reset OTP generated", rotp_code is not None)

        # 8. reset password
        if rotp_code:
            r = c.post("/reset-password/", data={
                "code": rotp_code, "password": "newpass123", "confirm_password": "newpass123",
            })
            check("Password reset accepted",
                  r.status_code == 302 and "login" in r.headers.get("Location", ""))
            with app.app_context():
                u = User.query.filter_by(email=TEST_EMAIL).first()
                check("New password is active", u.check_password("newpass123"))

    # cleanup
    with app.app_context():
        u = User.query.filter_by(email=TEST_EMAIL).first()
        if u:
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)
            db.session.commit()
            print("(test customer cleaned up)")

    passed = sum(results)
    total = len(results)
    print(f"\n=== Phase 1 auth-core smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
