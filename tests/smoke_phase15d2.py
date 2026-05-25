"""Phase 15 Chunk D-2 smoke test — Specs list + public Q&A system.

Covers:
  * Seller can add + delete ProductSpec rows on product_edit.
  * Product page renders the Specs table when specs exist.
  * "View More" toggle button only shows when there are more than 6 specs.
  * Q&A counter ("X Answered Questions") near the rating.
  * Anonymous user is prompted to log in (no ask form rendered).
  * Logged-in customer can POST /product/<slug>/qa/ask → Question created.
  * Seller answer is flagged with `is_seller_answer = True` and the
    "Seller" badge appears in HTML.
  * Phone numbers in Q&A answers are redacted via policy_service and a
    PolicyViolation row is logged (SURFACE_QA) for the seller.
  * Asker gets a NOTIF_PRODUCT notification when answered.
  * Seller gets a NOTIF_PRODUCT notification when a customer asks.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d2.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import (
    Category, Brand, Product, ProductSpec, PRODUCT_PUBLISHED,
)
from app.models.qa import Question, Answer
from app.models.notification import Notification, NOTIF_PRODUCT
from app.models.policy import PolicyViolation, SURFACE_QA

CUSTOMER = "smoke_p15d2_customer@example.com"
SELLER = "smoke_p15d2_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d2-cat"
PROD_SLUG = "p15d2-product-a"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        users = [u for u in
                 (User.query.filter_by(email=e).first()
                  for e in (CUSTOMER, SELLER))
                 if u is not None]
        uids = [u.id for u in users]
        # Answers reference questions (FK) — drop answers across all users
        # before questions, and Q&A before products (Question.product_id FK).
        if uids:
            Answer.query.filter(Answer.responder_id.in_(uids)).delete(
                synchronize_session=False)
            Question.query.filter(Question.asker_id.in_(uids)).delete(
                synchronize_session=False)
        for u in users:
            PolicyViolation.query.filter_by(user_id=u.id).delete()
            Notification.query.filter_by(user_id=u.id).delete()
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


def web_login(app, c, email, account_type):
    c.post("/login/", data={"email": email, "password": PASSWORD,
                            "account_type": account_type})
    c.post("/verify-otp/", data={"code": latest_otp(app, email)})


def seed(app):
    with app.app_context():
        cat = Category(name_en="Smoke P15D2", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P15D2 Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        seller = User(name="P15D2 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        db.session.add_all([customer, seller])
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15D2 Shop",
                           slug="p15d2-shop", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D2 Product", slug=PROD_SLUG,
            base_price=500, stock=10, status=PRODUCT_PUBLISHED,
        )
        db.session.add(product)
        db.session.flush()
        # Two specs up-front so the rendered table is visible.
        db.session.add_all([
            ProductSpec(product_id=product.id, label="Material",
                        value="Cotton 100%", sort_order=0),
            ProductSpec(product_id=product.id, label="Origin",
                        value="Bangladesh", sort_order=1),
        ])
        db.session.commit()
        return {"customer_id": customer.id, "seller_id": seller.id,
                "vendor_id": vp.id, "product_id": product.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # service layer — qa_service
    # ====================================================================
    with app.app_context():
        from app.services.qa_service import (
            ask_question, post_answer, public_questions, answered_count,
        )
        customer = db.session.get(User, ids["customer_id"])
        seller = db.session.get(User, ids["seller_id"])
        product = db.session.get(Product, ids["product_id"])

        # Empty body rejected
        q, error = ask_question(customer, product, "   ")
        check("ask_question rejects empty body", q is None and error)

        # Valid question
        q, error = ask_question(customer, product, "Is this original?")
        check("ask_question succeeds", error is None and q is not None)
        check("question stored as public + unflagged",
              q.is_public is True and q.is_flagged is False)
        check("seller notified of new question",
              Notification.query.filter_by(
                  user_id=seller.id, kind=NOTIF_PRODUCT
              ).filter(Notification.title.like("%question%")).count() >= 1)

        # Seller answers; phone number is redacted + policy violation logged
        before_violations = PolicyViolation.query.filter_by(
            user_id=seller.id, surface=SURFACE_QA
        ).count()
        a, error = post_answer(
            seller, q,
            "Yes — call 01712345678 for any issue, original ছাড়া কিছু না।",
        )
        check("post_answer succeeds", error is None and a is not None)
        check("seller answer flagged + phone redacted",
              a.is_flagged is True
              and "01712345678" not in a.body
              and "[number removed]" in a.body)
        check("seller answer carries the Seller badge",
              a.is_seller_answer is True)
        after_violations = PolicyViolation.query.filter_by(
            user_id=seller.id, surface=SURFACE_QA
        ).count()
        check("seller phone-share in Q&A logged as PolicyViolation",
              after_violations == before_violations + 1)

        # Asker notified of the answer
        check("asker notified of answer",
              Notification.query.filter(
                  Notification.user_id == ids["customer_id"],
                  Notification.kind == NOTIF_PRODUCT,
                  Notification.title.like("%answer%"),
              ).count() >= 1)

        # answered_count + public_questions
        check("answered_count returns 1", answered_count(product) == 1)
        check("public_questions lists the question",
              len(public_questions(product)) >= 1)

    # ====================================================================
    # web flow — public product page renders Specs + Q&A
    # ====================================================================
    with app.test_client() as c:
        r = c.get(f"/product/{PROD_SLUG}/")
        body = r.data.decode("utf-8", errors="ignore")
        check("product page renders", r.status_code == 200)
        check("Specifications section present",
              "Specifications" in body and "Material" in body
              and "Cotton 100%" in body)
        # 2 specs <= 6 → no toggle button rendered
        check("View More toggle hidden when <= 6 specs",
              'id="pdpSpecsToggle"' not in body)
        check("Q&A section anchor present",
              'id="qa"' in body and "Questions" in body)
        check("Answered Questions counter present",
              "Answered Question" in body)
        check("the existing question appears in the page",
              "Is this original?" in body)
        check("seller Seller badge on answer",
              "Seller" in body and "[number removed]" in body)
        check("anonymous users see Log-in CTA, not the Q&A ask form",
              "Log in" in body and f'/product/{PROD_SLUG}/qa/ask' not in body)

    # ====================================================================
    # web flow — logged-in customer asks via the public route
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMER, "customer")
        r = c.post(f"/product/{PROD_SLUG}/qa/ask",
                   data={"body": "Warranty আছে কি?"}, follow_redirects=False)
        check("POST qa/ask redirects to product#qa",
              r.status_code in (302, 303)
              and "/product/" in r.headers.get("Location", ""))
        with app.app_context():
            q = (Question.query.filter_by(asker_id=ids["customer_id"])
                 .filter(Question.body.like("Warranty%")).first())
            check("customer question persisted via web", q is not None)

    # ====================================================================
    # web flow — seller adds and removes a spec via /seller/products/<id>/specs
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, SELLER, "seller")
        r = c.post(f"/seller/products/{ids['product_id']}/specs",
                   data={"label": "Weight", "value": "250g"},
                   follow_redirects=False)
        check("seller add-spec redirects", r.status_code in (302, 303))
        with app.app_context():
            spec = ProductSpec.query.filter_by(
                product_id=ids["product_id"], label="Weight"
            ).first()
            check("spec persisted via web", spec is not None)
            spec_id = spec.id

        # Empty label rejected (no row added)
        before = ProductSpec.query.filter_by(product_id=ids["product_id"]).count() \
            if False else None
        with app.app_context():
            before = ProductSpec.query.filter_by(
                product_id=ids["product_id"]
            ).count()
        c.post(f"/seller/products/{ids['product_id']}/specs",
               data={"label": "", "value": "no label"})
        with app.app_context():
            after = ProductSpec.query.filter_by(
                product_id=ids["product_id"]
            ).count()
        check("spec without label rejected (count unchanged)", after == before)

        # Delete
        c.post(f"/seller/products/{ids['product_id']}/specs/{spec_id}/delete")
        with app.app_context():
            check("spec deleted via web",
                  db.session.get(ProductSpec, spec_id) is None)

    # ====================================================================
    # View More toggle visibility — needs > 6 specs
    # ====================================================================
    with app.app_context():
        existing = ProductSpec.query.filter_by(
            product_id=ids["product_id"]
        ).count()
        for i in range(existing, 8):
            db.session.add(ProductSpec(
                product_id=ids["product_id"], label=f"Spec{i}",
                value=f"Value{i}", sort_order=i,
            ))
        db.session.commit()
    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("View More toggle rendered when > 6 specs",
              'id="pdpSpecsToggle"' in body and "pdp-spec-extra" in body)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-2 specs + Q&A smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
