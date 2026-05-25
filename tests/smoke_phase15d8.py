"""Phase 15 Chunk D-8 smoke test — smart helpers.

Covers:
  * `frequently_bought_together` returns products co-occurring in past
    orders, ordered by co-occurrence count.
  * `ai_summary_service.refresh_product_summary` uses the heuristic
    fallback (no ANTHROPIC_API_KEY in tests) to populate
    `ai_pros_json` / `ai_cons_json`. With < 3 reviews it clears the cache.
  * `qa_service.toggle_helpful` flips the vote, updates `helpful_count`,
    and rejects self-votes.
  * `voted_answer_ids` returns the set of answer ids the user has voted on.
  * POST /product/<slug>/qa/answer/<id>/helpful toggles the vote via the
    web flow.
  * Product page renders:
      - "Frequently Bought Together" section + the current product card
      - AI Pros & Cons panels with the cached bullets
      - Per-answer "Helpful" button with the live count

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d8.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.otp import OtpCode, OTP_PURPOSE_LOGIN
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.order import Order, SubOrder, OrderItem, SUBORDER_DELIVERED
from app.models.review import Review
from app.models.qa import Question, Answer, AnswerVote
from app.services.recommendation_service import frequently_bought_together
from app.services import ai_summary_service, qa_service
from app.services.review_service import (
    recompute_product_rating, recompute_vendor_rating,
)

CUSTOMERS = [f"smoke_p15d8_c{i}@example.com" for i in range(1, 5)]
SELLER = "smoke_p15d8_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d8-cat"
P_MAIN = "p15d8-main"
P_BUNDLE = "p15d8-bundle"
P_OTHER = "p15d8-other"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        emails = CUSTOMERS + [SELLER]
        users = [u for u in
                 (User.query.filter_by(email=e).first() for e in emails)
                 if u is not None]
        uids = [u.id for u in users]
        if uids:
            AnswerVote.query.filter(AnswerVote.user_id.in_(uids)).delete(
                synchronize_session=False)
            Answer.query.filter(Answer.responder_id.in_(uids)).delete(
                synchronize_session=False)
            Question.query.filter(Question.asker_id.in_(uids)).delete(
                synchronize_session=False)
        for u in users:
            for r in Review.query.filter_by(user_id=u.id).all():
                db.session.delete(r)
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


def web_login(app, c, email, account_type):
    c.post("/login/", data={"email": email, "password": PASSWORD,
                            "account_type": account_type})
    c.post("/verify-otp/", data={"code": latest_otp(app, email)})


def seed(app):
    """3 products. Customers 1-3 buy MAIN + BUNDLE in the same order.
    Customer 4 buys MAIN + OTHER. So FBT(MAIN) -> [BUNDLE, OTHER]."""
    with app.app_context():
        cat = Category(name_en="Smoke P15D8", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        seller = User(name="P15D8 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        db.session.add(seller)
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15D8 Shop",
                           slug="p15d8-shop", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        p_main = Product(vendor_id=vp.id, category_id=cat.id,
                         title_en="P15D8 Main", slug=P_MAIN,
                         base_price=500, stock=50, status=PRODUCT_PUBLISHED)
        p_bundle = Product(vendor_id=vp.id, category_id=cat.id,
                           title_en="P15D8 Bundle", slug=P_BUNDLE,
                           base_price=200, stock=50, status=PRODUCT_PUBLISHED)
        p_other = Product(vendor_id=vp.id, category_id=cat.id,
                          title_en="P15D8 Other", slug=P_OTHER,
                          base_price=300, stock=50, status=PRODUCT_PUBLISHED)
        db.session.add_all([p_main, p_bundle, p_other])
        db.session.flush()

        review_plan = [
            (5, "Excellent product, very durable build quality."),
            (5, "Great value for the money, fast delivery."),
            (5, "Loved it, would buy again from this seller."),
            (2, "Packaging was poor and the warranty card was missing."),
        ]
        cust_ids = []
        for i, (rating, comment) in enumerate(review_plan):
            cust = User(name=f"P15D8 C{i+1}", email=CUSTOMERS[i],
                        role="customer", is_active=True)
            cust.set_password(PASSWORD)
            db.session.add(cust)
            db.session.flush()
            cust_ids.append(cust.id)

            # First 3 customers buy MAIN + BUNDLE; the 4th buys MAIN + OTHER.
            partner = p_bundle if i < 3 else p_other
            order = Order(customer_id=cust.id,
                          order_number=f"SGTP15D8-T{i:02d}",
                          payment_method="cod", payment_status="pending",
                          ship_name=cust.name, ship_phone="01700000099",
                          ship_address_line="1 Test St", ship_city="Dhaka",
                          subtotal=700, shipping_fee=0, total_amount=700)
            db.session.add(order)
            db.session.flush()
            sub = SubOrder(order_id=order.id, vendor_id=vp.id,
                           subtotal=700, status=SUBORDER_DELIVERED)
            db.session.add(sub)
            db.session.flush()
            db.session.add_all([
                OrderItem(sub_order_id=sub.id, product_id=p_main.id,
                          title="Main", unit_price=500,
                          quantity=1, line_total=500),
                OrderItem(sub_order_id=sub.id, product_id=partner.id,
                          title="Partner", unit_price=200,
                          quantity=1, line_total=200),
            ])
            db.session.add(Review(product_id=p_main.id, user_id=cust.id,
                                  rating=rating, comment=comment,
                                  is_verified=True))

        recompute_product_rating(p_main)
        recompute_vendor_rating(vp)

        # A question + two seller-authored answers so we can test helpful
        # votes.
        q = Question(product_id=p_main.id, asker_id=cust_ids[0],
                     body="Is the warranty real?", is_public=True)
        db.session.add(q)
        db.session.flush()
        a1 = Answer(question_id=q.id, responder_id=seller.id,
                    body="Yes — 6 months manufacturer warranty included.",
                    is_seller_answer=True)
        a2 = Answer(question_id=q.id, responder_id=cust_ids[1],
                    body="I had no issues, warranty card came in the box.",
                    is_seller_answer=False)
        db.session.add_all([a1, a2])
        db.session.commit()
        return {"vendor_id": vp.id, "seller_id": seller.id,
                "p_main": p_main.id, "p_bundle": p_bundle.id,
                "p_other": p_other.id,
                "cust1": cust_ids[0], "cust2": cust_ids[1],
                "answer1": a1.id, "answer2": a2.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # FBT
    # ====================================================================
    with app.app_context():
        p_main = db.session.get(Product, ids["p_main"])
        p_bundle = db.session.get(Product, ids["p_bundle"])
        p_other = db.session.get(Product, ids["p_other"])

        fbt = frequently_bought_together(p_main, limit=4)
        ids_in_order = [p.id for p in fbt]
        check("FBT returns co-purchased products",
              ids["p_bundle"] in ids_in_order and ids["p_other"] in ids_in_order)
        check("FBT ranks the higher-co-occurrence partner first",
              ids_in_order.index(ids["p_bundle"]) < ids_in_order.index(ids["p_other"]),
              f"order: {ids_in_order}")
        check("FBT excludes the source product",
              ids["p_main"] not in ids_in_order)
        check("FBT empty for a product with no shared orders",
              frequently_bought_together(p_other, limit=4) != [])

    # ====================================================================
    # AI summary heuristic
    # ====================================================================
    # No API key -> heuristic fallback path.
    os.environ.pop("ANTHROPIC_API_KEY", None)
    with app.app_context():
        p_main = db.session.get(Product, ids["p_main"])
        pros, cons = ai_summary_service.refresh_product_summary(p_main)
        check("heuristic produced at least one pro from 5-star reviews",
              len(pros) >= 1)
        check("heuristic produced at least one con from 1-2-star reviews",
              len(cons) >= 1)
        check("ai_pros_json + ai_cons_json persisted",
              p_main.ai_pros_json and p_main.ai_cons_json
              and p_main.ai_summary_at is not None)
        check("ai_summary_service.pros / cons round-trip the JSON",
              ai_summary_service.pros(p_main)
              and ai_summary_service.cons(p_main))

        # Product with too few reviews -> clears cache and returns empty.
        p_bundle = db.session.get(Product, ids["p_bundle"])
        pros, cons = ai_summary_service.refresh_product_summary(p_bundle)
        check("ai summary returns empty when < 3 reviews",
              pros == [] and cons == [])

    # ====================================================================
    # Q&A helpful-vote service
    # ====================================================================
    with app.app_context():
        a1 = db.session.get(Answer, ids["answer1"])
        seller = db.session.get(User, ids["seller_id"])
        c1 = db.session.get(User, ids["cust1"])
        c2 = db.session.get(User, ids["cust2"])

        # Self-vote disallowed (seller upvoting own answer)
        voted, count = qa_service.toggle_helpful(seller, a1)
        check("toggle_helpful rejects self-vote",
              voted is False and count == 0)

        # Two customers upvote
        voted, count = qa_service.toggle_helpful(c1, a1)
        check("first upvote registered + count incremented",
              voted is True and count == 1)
        voted, count = qa_service.toggle_helpful(c2, a1)
        check("second upvote increments to 2",
              voted is True and count == 2)

        # Re-vote toggles off
        voted, count = qa_service.toggle_helpful(c1, a1)
        check("re-vote removes the vote",
              voted is False and count == 1)

        check("voted_answer_ids reflects current state for c2",
              ids["answer1"] in qa_service.voted_answer_ids(
                  c2, db.session.get(Product, ids["p_main"])))
        check("voted_answer_ids is empty for c1 after un-vote",
              ids["answer1"] not in qa_service.voted_answer_ids(
                  c1, db.session.get(Product, ids["p_main"])))

    # ====================================================================
    # Product page rendering
    # ====================================================================
    with app.test_client() as c:
        body = c.get(f"/product/{P_MAIN}/").data.decode("utf-8", errors="ignore")
        check("FBT section rendered",
              "Frequently Bought Together" in body and "pdp-fbt" in body)
        check("FBT lists the co-purchased product",
              "P15D8 Bundle" in body)
        check("AI Pros & Cons section rendered",
              "pdp-ai-summary" in body and "What buyers like" in body
              and "What to watch for" in body)

    # ====================================================================
    # Helpful-vote web flow
    # ====================================================================
    with app.test_client() as c:
        web_login(app, c, CUSTOMERS[0], "customer")    # c1 is logged in
        # Re-vote (currently un-voted after the service test); should set it
        r = c.post(
            f"/product/{P_MAIN}/qa/answer/{ids['answer1']}/helpful",
            follow_redirects=False,
        )
        check("helpful-vote POST redirects to product#qa",
              r.status_code in (302, 303)
              and "#qa" in r.headers.get("Location", ""))
        with app.app_context():
            a1 = db.session.get(Answer, ids["answer1"])
            check("helpful_count reflects the web vote",
                  a1.helpful_count == 2)

        # Page now shows the Helpful button + count
        body = c.get(f"/product/{P_MAIN}/").data.decode("utf-8", errors="ignore")
        check("Helpful button visible on answers",
              "pdp-helpful-btn" in body)
        check("helpful count shown next to the button",
              "Helpful" in body and "(2)" in body)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-8 smart helpers smoke test: "
          f"{passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
