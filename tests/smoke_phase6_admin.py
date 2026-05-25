"""Phase 6 smoke test — platform settings, admin reports, audit log.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase6_admin.py <admin_password>
"""
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.otp import OtpCode
from app.models.vendor import VendorProfile
from app.models.setting import Setting, AuditLog
from app.services.settings_service import get_setting
from app.services.order_service import shipping_fee_per_vendor

ADMIN_EMAIL = "monirhasan2003@gmail.com"
SELLER = "smoke_p6_seller@example.com"
KEYS = ["default_commission_rate", "shipping_fee_per_vendor", "site_name", "currency_symbol"]
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        u = User.query.filter_by(email=SELLER).first()
        if u:
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)
            db.session.commit()


def main():
    admin_password = sys.argv[1] if len(sys.argv) > 1 else ""
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)

    # snapshot settings so the test can restore them
    with app.app_context():
        snapshot = {}
        for k in KEYS:
            row = db.session.get(Setting, k)
            snapshot[k] = row.value if row else None

    with app.test_client() as c:
        c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})

        r = c.get("/admin/")
        check("Admin dashboard (reports)",
              r.status_code == 200 and b"Commission Earned" in r.data
              and b"Top Sellers" in r.data)

        r = c.get("/admin/settings/")
        check("Admin settings page", r.status_code == 200)

        r = c.post("/admin/settings/", data={
            "site_name": "SGT Test Mart", "default_commission_rate": "12.50",
            "shipping_fee_per_vendor": "70.00", "currency_symbol": "Tk",
        })
        check("Settings saved", r.status_code == 302)
        with app.app_context():
            check("Commission setting persisted",
                  get_setting("default_commission_rate") == "12.50")
            check("Shipping setting used by order service",
                  shipping_fee_per_vendor() == Decimal("70.00"))

        r = c.get("/admin/audit-log/")
        check("Audit log records settings change",
              r.status_code == 200 and b"Updated platform settings" in r.data)

    # new seller picks up the configured default commission rate
    with app.test_client() as anon:
        anon.post("/signup/", data={
            "first_name": "P6", "last_name": "Seller", "email": SELLER,
            "phone": "01700000000", "role": "seller", "shop_name": "P6 Test Shop",
            "password": "test1234", "confirm_password": "test1234",
        })
    with app.app_context():
        u = User.query.filter_by(email=SELLER).first()
        vp = VendorProfile.query.filter_by(user_id=u.id).first()
        check("New seller uses configured commission rate (12.50)",
              vp is not None and vp.commission_rate == Decimal("12.50"),
              str(vp.commission_rate) if vp else "none")
        vendor_id = vp.id

    # admin approves -> audit log entry
    with app.test_client() as c:
        c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})
        # mark verification submitted so approval is allowed
        with app.app_context():
            from datetime import datetime
            v = db.session.get(VendorProfile, vendor_id)
            v.verification_submitted_at = datetime.utcnow()
            db.session.commit()
        c.post(f"/admin/vendors/{vendor_id}/approve")
        r = c.get("/admin/audit-log/")
        check("Vendor approval logged", b"Approved vendor" in r.data)

    # restore settings
    with app.app_context():
        for k, v in snapshot.items():
            row = db.session.get(Setting, k)
            if v is None:
                if row:
                    db.session.delete(row)
            elif row:
                row.value = v
            else:
                db.session.add(Setting(key=k, value=v))
        db.session.commit()

    purge(app)
    print("(test data cleaned up, settings restored)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 6 admin smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
