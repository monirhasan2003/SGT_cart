"""Phase 15 Chunk D-3 smoke test — reviews upgrade.

Covers:
  * `rating_distribution` returns one bucket per star 1..5.
  * `paginated_reviews` paginates and respects sort modes + star filter:
      - newest, highest, lowest sorts the rows in the expected direction.
      - rstar=N filters out the others.
  * `review_photos` aggregates ReviewImage rows across reviews.
  * Product page renders:
      - distribution bars (one row per star, with progress-bar elements),
      - sort + star-filter toolbar links,
      - customer photo gallery,
      - pagination (only when total > REVIEWS_PER_PAGE).
  * Query params on the product URL drive the rendered list:
      - ?rsort=highest puts the highest-rated review first,
      - ?rstar=1 shows only the 1-star review.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15d3.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.order import Order, SubOrder, OrderItem, SUBORDER_DELIVERED
from app.models.review import Review, ReviewImage
from app.services.review_service import (
    rating_distribution, paginated_reviews, review_photos,
    REVIEW_SORT_NEWEST, REVIEW_SORT_HIGHEST, REVIEW_SORT_LOWEST,
    REVIEWS_PER_PAGE,
)

CUSTOMERS = [f"smoke_p15d3_c{i}@example.com" for i in range(1, 9)]
SELLER = "smoke_p15d3_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p15d3-cat"
PROD_SLUG = "p15d3-product-a"
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
        # Use session.delete so ORM-level cascades on Review.images +
        # Order.sub_orders + SubOrder.items fire. Bulk .delete() bypasses
        # them and trips FK constraints.
        for u in users:
            for r in Review.query.filter_by(user_id=u.id).all():
                db.session.delete(r)
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)
        db.session.flush()
        for u in users:
            db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()


def seed(app):
    """Seller + 8 customers, each with a delivered order of the product,
    each leaving a review of a different star count. Two reviews carry a
    ReviewImage so the photo gallery has rows to aggregate.
    """
    with app.app_context():
        cat = Category(name_en="Smoke P15D3", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        seller = User(name="P15D3 Seller", email=SELLER, role="seller",
                      is_active=True)
        seller.set_password(PASSWORD)
        db.session.add(seller)
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P15D3 Shop",
                           slug="p15d3-shop", status=VENDOR_APPROVED,
                           commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        product = Product(
            vendor_id=vp.id, category_id=cat.id,
            title_en="P15D3 Product", slug=PROD_SLUG,
            base_price=500, stock=20, status=PRODUCT_PUBLISHED,
        )
        db.session.add(product)
        db.session.flush()

        # 8 reviews: 4 of 5-star, 2 of 4-star, 1 of 3-star, 1 of 1-star.
        review_plan = [
            (5, "5-star one", "Excellent"),
            (5, "5-star two", "Loved it"),
            (5, "5-star three", "Outstanding"),
            (5, "5-star four", "Perfect"),
            (4, "4-star one", "Very good"),
            (4, "4-star two", "Solid"),
            (3, "3-star one", "Average"),
            (1, "1-star one", "Disappointed"),
        ]
        review_ids = []
        for i, (rating, title, comment) in enumerate(review_plan):
            email = CUSTOMERS[i]
            cust = User(name=f"P15D3 C{i}", email=email, role="customer",
                        is_active=True)
            cust.set_password(PASSWORD)
            db.session.add(cust)
            db.session.flush()
            # Delivered order so the review counts as verified.
            order = Order(customer_id=cust.id,
                          order_number=f"SGTP15D3-T{i:02d}",
                          payment_method="cod", payment_status="pending",
                          ship_name=cust.name, ship_phone="01700000099",
                          ship_address_line="1 Test St", ship_city="Dhaka",
                          subtotal=500, shipping_fee=0, total_amount=500)
            db.session.add(order)
            db.session.flush()
            sub = SubOrder(order_id=order.id, vendor_id=vp.id, subtotal=500,
                           status=SUBORDER_DELIVERED)
            db.session.add(sub)
            db.session.flush()
            db.session.add(OrderItem(sub_order_id=sub.id, product_id=product.id,
                                     title="P15D3 Product", unit_price=500,
                                     quantity=1, line_total=500))
            r = Review(product_id=product.id, user_id=cust.id, rating=rating,
                       title=title, comment=comment, is_verified=True)
            db.session.add(r)
            db.session.flush()
            review_ids.append(r.id)

        # Two photos on the two 5-star reviews so the gallery has content.
        db.session.add_all([
            ReviewImage(review_id=review_ids[0], image_path="assets/img/r1.png"),
            ReviewImage(review_id=review_ids[1], image_path="assets/img/r2.png"),
        ])
        # Denormalize rating aggregates so the product page renders the
        # distribution / toolbar (those panels gate on rating_count > 0).
        from app.services.review_service import (
            recompute_product_rating, recompute_vendor_rating,
        )
        recompute_product_rating(product)
        recompute_vendor_rating(vp)
        db.session.commit()
        return {"product_id": product.id, "vendor_id": vp.id,
                "seller_id": seller.id}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # service helpers
    # ====================================================================
    with app.app_context():
        product = db.session.get(Product, ids["product_id"])

        dist = rating_distribution(product)
        check("rating_distribution has all 5 buckets",
              set(dist.keys()) == {1, 2, 3, 4, 5})
        check("rating_distribution counts match seed",
              dist == {5: 4, 4: 2, 3: 1, 2: 0, 1: 1})

        # Paginated reviews — default sort is newest (highest id first)
        page1 = paginated_reviews(product, sort=REVIEW_SORT_NEWEST, page=1)
        check("pagination page-1 size = REVIEWS_PER_PAGE",
              len(page1.items) == REVIEWS_PER_PAGE)
        check("pagination total = 8", page1.total == 8)
        ids_p1 = [r.id for r in page1.items]
        check("newest sort returns highest ids first",
              ids_p1 == sorted(ids_p1, reverse=True))

        page2 = paginated_reviews(product, sort=REVIEW_SORT_NEWEST, page=2)
        check("pagination page-2 has the remaining items",
              len(page2.items) == 8 - REVIEWS_PER_PAGE)

        # Sort: highest -> first item is 5-star
        high = paginated_reviews(product, sort=REVIEW_SORT_HIGHEST, page=1)
        check("highest sort puts a 5-star review first",
              high.items[0].rating == 5)
        # Lowest -> first item is 1-star
        low = paginated_reviews(product, sort=REVIEW_SORT_LOWEST, page=1)
        check("lowest sort puts a 1-star review first",
              low.items[0].rating == 1)

        # Star filter
        only5 = paginated_reviews(product, star_filter=5, page=1)
        check("rstar=5 filter returns exactly the 5-star reviews",
              only5.total == 4 and all(r.rating == 5 for r in only5.items))
        only2 = paginated_reviews(product, star_filter=2, page=1)
        check("rstar=2 filter returns 0 rows", only2.total == 0)

        # Photo gallery
        photos = review_photos(product)
        check("review_photos aggregates ReviewImage rows", len(photos) == 2)

    # ====================================================================
    # product page rendering
    # ====================================================================
    with app.test_client() as c:
        body = c.get(f"/product/{PROD_SLUG}/").data.decode("utf-8", errors="ignore")
        check("product page renders", "Ratings &amp; Reviews" in body or "Ratings & Reviews" in body)
        check("distribution bars rendered",
              "pdp-review-dist" in body and "progress-bar" in body)
        check("photo gallery rendered when ReviewImage rows exist",
              "pdp-review-photos" in body and "Customer Photos" in body)
        check("sort toolbar rendered with sort labels",
              "pdp-review-toolbar" in body
              and "Newest" in body and "Highest" in body and "Lowest" in body)
        check("star-filter chips rendered",
              "All stars" in body and "★" in body and "5 ★" in body)
        check("pagination rendered when reviews > per-page",
              "pdp-review-pagination" in body)

        # Highest sort — first review in the list should be a 5-star
        body_hi = c.get(f"/product/{PROD_SLUG}/?rsort=highest").data.decode(
            "utf-8", errors="ignore")
        # "5-star one" was the first 5-star seeded — but ties broken by id desc,
        # so the latest 5-star ("5-star four") wins. Either way the FIRST review
        # rendered should be 5-star text-wise.
        # Easier check: "1-star one" must not appear on page-1 of highest sort.
        check("highest sort hides the 1-star review from page-1",
              "1-star one" not in body_hi)

        # Filter — only 1-star
        body_f1 = c.get(f"/product/{PROD_SLUG}/?rstar=1").data.decode(
            "utf-8", errors="ignore")
        check("rstar=1 keeps the 1-star review", "1-star one" in body_f1)
        check("rstar=1 hides the 5-star reviews",
              "5-star one" not in body_f1 and "5-star two" not in body_f1)

        # Filter with no matches
        body_f2 = c.get(f"/product/{PROD_SLUG}/?rstar=2").data.decode(
            "utf-8", errors="ignore")
        check("rstar=2 shows empty-filter message",
              "No reviews match" in body_f2 and "Clear filter" in body_f2)

        # Bogus rsort falls back gracefully
        r = c.get(f"/product/{PROD_SLUG}/?rsort=bogus")
        check("bogus rsort param still 200", r.status_code == 200)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 D-3 reviews upgrade smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
