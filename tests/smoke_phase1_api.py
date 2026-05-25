"""Phase 1 smoke test — REST API (JWT auth endpoints).

Run:  venv\\Scripts\\python.exe tests\\smoke_phase1_api.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN, OTP_PURPOSE_RESET

CUSTOMER = "smoke_api_customer@example.com"
SELLER = "smoke_api_seller@example.com"
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


def latest_otp(app, email, purpose):
    with app.app_context():
        u = User.query.filter_by(email=email).first()
        otp = (OtpCode.query
               .filter_by(user_id=u.id, purpose=purpose, is_used=False)
               .order_by(OtpCode.id.desc()).first())
        return otp.code if otp else None


def main():
    app = create_app("development")
    purge(app, CUSTOMER)
    purge(app, SELLER)

    with app.test_client() as c:
        # register customer
        r = c.post("/api/v1/auth/register", json={
            "name": "API Customer", "email": CUSTOMER, "phone": "01700000000",
            "password": "test1234", "role": "customer",
        })
        check("register customer (201)", r.status_code == 201)

        # duplicate email -> 409
        r = c.post("/api/v1/auth/register", json={
            "name": "Dup", "email": CUSTOMER, "password": "test1234", "role": "customer",
        })
        check("duplicate email rejected (409)", r.status_code == 409)

        # wrong password -> 401
        r = c.post("/api/v1/auth/login", json={"email": CUSTOMER, "password": "WRONG"})
        check("wrong password (401)", r.status_code == 401)

        # login -> otp_required
        r = c.post("/api/v1/auth/login", json={"email": CUSTOMER, "password": "test1234"})
        check("login -> otp_required", r.status_code == 200 and r.get_json().get("otp_required") is True)

        # verify-otp -> tokens
        code = latest_otp(app, CUSTOMER, OTP_PURPOSE_LOGIN)
        check("login OTP generated", code is not None)
        r = c.post("/api/v1/auth/verify-otp", json={"email": CUSTOMER, "code": code})
        body = r.get_json() or {}
        access = body.get("access_token")
        refresh = body.get("refresh_token")
        check("verify-otp -> JWT tokens", r.status_code == 200 and bool(access) and bool(refresh))

        # /me with access token
        r = c.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access}"})
        check("GET /auth/me with token", r.status_code == 200
              and (r.get_json() or {}).get("user", {}).get("email") == CUSTOMER)

        # /me without token -> 401
        r = c.get("/api/v1/auth/me")
        check("GET /auth/me without token (401)", r.status_code == 401)

        # refresh
        r = c.post("/api/v1/auth/refresh", headers={"Authorization": f"Bearer {refresh}"})
        new_access = (r.get_json() or {}).get("access_token")
        check("refresh -> new access token", r.status_code == 200 and bool(new_access))
        r = c.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {new_access}"})
        check("refreshed token works", r.status_code == 200)

        # forgot + reset password
        r = c.post("/api/v1/auth/forgot-password", json={"email": CUSTOMER})
        check("forgot-password (200)", r.status_code == 200)
        rcode = latest_otp(app, CUSTOMER, OTP_PURPOSE_RESET)
        r = c.post("/api/v1/auth/reset-password", json={
            "email": CUSTOMER, "code": rcode, "password": "newpass123",
        })
        check("reset-password (200)", r.status_code == 200)
        with app.app_context():
            u = User.query.filter_by(email=CUSTOMER).first()
            check("new password active", u.check_password("newpass123"))

        # register seller -> vendor in payload
        r = c.post("/api/v1/auth/register", json={
            "name": "API Seller", "email": SELLER, "password": "test1234",
            "role": "seller", "shop_name": "API Test Shop",
        })
        body = r.get_json() or {}
        check("register seller with vendor",
              r.status_code == 201 and body.get("user", {}).get("vendor", {}).get("status") == "pending")

    purge(app, CUSTOMER)
    purge(app, SELLER)
    print("(test users cleaned up)")

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 1 REST API smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
