"""Phase 1 smoke test — admin panel.

Covers the admin dashboard, user & vendor management, vendor approval and the
"log in as user" impersonation flow. Test data is cleaned up at the end.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase1_admin.py <admin_password>
"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile
from app.models.otp import OtpCode

ADMIN_EMAIL = "monirhasan2003@gmail.com"
SELLER_EMAIL = "smoke_seller@example.com"

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def cleanup(app):
    with app.app_context():
        u = User.query.filter_by(email=SELLER_EMAIL).first()
        if u:
            VendorProfile.query.filter_by(user_id=u.id).delete()
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)
            db.session.commit()


def main():
    admin_password = sys.argv[1] if len(sys.argv) > 1 else ""

    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    cleanup(app)

    # 1. anonymous user cannot reach the admin panel + registers a test seller
    with app.test_client() as anon:
        r = anon.get("/admin/")
        check("Anonymous blocked from /admin/", r.status_code in (302, 401, 403),
              f"status {r.status_code}")

        r = anon.post("/signup/", data={
            "first_name": "Smoke", "last_name": "Seller", "email": SELLER_EMAIL,
            "phone": "01800000000", "role": "seller", "shop_name": "Smoke Test Shop",
            "password": "test1234", "confirm_password": "test1234",
        })
        check("Seller registration", r.status_code == 302)

    with app.app_context():
        seller = User.query.filter_by(email=SELLER_EMAIL).first()
        vendor = VendorProfile.query.filter_by(user_id=seller.id).first() if seller else None
        check("Vendor profile created (pending)",
              vendor is not None and vendor.status == "pending")
        # Simulate a completed KYC submission so the admin can approve.
        # (The KYC flow itself is covered by smoke_phase1_vendor_kyc.py.)
        if vendor:
            vendor.verification_submitted_at = datetime.utcnow()
            db.session.commit()
        seller_id = seller.id if seller else None
        vendor_id = vendor.id if vendor else None

    if not vendor_id:
        print("\n!! seller/vendor not created — aborting")
        sys.exit(1)

    # 2. admin operations
    with app.test_client() as c:
        r = c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})
        check("Admin login", r.status_code == 302 and "/admin" in r.headers.get("Location", ""),
              f"-> {r.headers.get('Location')}")

        for path in ["/admin/", "/admin/users/", "/admin/vendors/"]:
            r = c.get(path)
            check(f"GET {path}", r.status_code == 200, f"status {r.status_code}")

        r = c.get("/admin/vendors/?status=pending")
        check("Pending vendors list", r.status_code == 200 and b"Smoke Test Shop" in r.data)

        c.post(f"/admin/vendors/{vendor_id}/approve")
        with app.app_context():
            check("Vendor approval", db.session.get(VendorProfile, vendor_id).status == "approved")

        r = c.get(f"/admin/users/{seller_id}/")
        check("User detail page", r.status_code == 200 and b"Smoke Seller" in r.data)

        # impersonation
        r = c.get(f"/admin/users/{seller_id}/login-as")
        check("Login-as (impersonate)", r.status_code == 302)
        r = c.get("/")
        check("Impersonation banner shown", b"Return to Admin" in r.data)
        r = c.get("/admin/")
        check("Impersonated user blocked from /admin/", r.status_code in (302, 403))

        r = c.get("/admin/stop-impersonating")
        check("Stop impersonating", r.status_code == 302)
        r = c.get("/admin/")
        check("Admin restored after impersonation", r.status_code == 200)

        c.post(f"/admin/users/{seller_id}/toggle-active")
        with app.app_context():
            check("Toggle account active", db.session.get(User, seller_id).is_active is False)

    cleanup(app)
    print("(test seller cleaned up)")

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 1 admin-panel smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
