"""Phase 3 smoke test — DB-backed delivery addresses.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase3_address.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN

CUSTOMER = "smoke_addr_customer@example.com"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        u = User.query.filter_by(email=CUSTOMER).first()
        if u:
            Address.query.filter_by(user_id=u.id).delete()
            OtpCode.query.filter_by(user_id=u.id).delete()
            db.session.delete(u)
            db.session.commit()


def otp_login(app, c):
    c.post("/login/", data={"email": CUSTOMER, "password": "test1234", "account_type": "customer"})
    with app.app_context():
        u = User.query.filter_by(email=CUSTOMER).first()
        otp = (OtpCode.query.filter_by(user_id=u.id, purpose=OTP_PURPOSE_LOGIN, is_used=False)
               .order_by(OtpCode.id.desc()).first())
    c.post("/verify-otp/", data={"code": otp.code})


def addr_form(name, default=False):
    data = {"label": "Home", "full_name": name, "phone": "01700000000",
            "address_line": "12 Test Road", "area": "Banani", "city": "Dhaka",
            "district": "Dhaka", "postal_code": "1213"}
    if default:
        data["is_default"] = "on"
    return data


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)

    with app.test_client() as anon:
        r = anon.get("/addresses/")
        check("Anonymous addresses -> redirect", r.status_code == 302)

    with app.test_client() as c:
        c.post("/signup/", data={
            "first_name": "Addr", "last_name": "Tester", "email": CUSTOMER,
            "role": "customer", "password": "test1234", "confirm_password": "test1234",
        })
        otp_login(app, c)

        r = c.get("/addresses/")
        check("Empty addresses page", r.status_code == 200 and b"no saved addresses" in r.data)

        # first address -> auto default
        c.post("/addresses/new", data=addr_form("First Person"))
        with app.app_context():
            u = User.query.filter_by(email=CUSTOMER).first()
            addrs = Address.query.filter_by(user_id=u.id).all()
            check("First address created + default",
                  len(addrs) == 1 and addrs[0].is_default)
            uid = u.id
            a1 = addrs[0].id

        r = c.get("/addresses/")
        check("Address shows on page", r.status_code == 200 and b"First Person" in r.data)

        # second address
        c.post("/addresses/new", data=addr_form("Second Person"))
        with app.app_context():
            addrs = Address.query.filter_by(user_id=uid).order_by(Address.id).all()
            check("Second address created", len(addrs) == 2)
            a2 = addrs[1].id

        # set second as default
        c.post(f"/addresses/{a2}/default")
        with app.app_context():
            check("Default switched",
                  db.session.get(Address, a2).is_default
                  and not db.session.get(Address, a1).is_default)

        # edit
        edit_data = addr_form("Renamed Person")
        c.post(f"/addresses/{a1}/edit", data=edit_data)
        with app.app_context():
            check("Address edited", db.session.get(Address, a1).full_name == "Renamed Person")

        # delete
        c.post(f"/addresses/{a1}/delete")
        with app.app_context():
            check("Address deleted", db.session.get(Address, a1) is None)
            check("Other address remains", db.session.get(Address, a2) is not None)

    purge(app)
    print("(test customer cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 3 address smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
