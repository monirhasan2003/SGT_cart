"""Review service — Phase 9.

Enforces verified-purchase reviews and keeps the product / seller rating
aggregates in sync. Shared by the web views and the REST API.
"""
from sqlalchemy import func

from app.extensions import db
from app.models.catalog import Product
from app.models.order import Order, SubOrder, OrderItem, SUBORDER_DELIVERED
from app.models.review import Review, ReviewImage, RATING_MIN, RATING_MAX
from app.models.notification import NOTIF_PRODUCT
from app.models.policy import SURFACE_REVIEW
from app.services import policy_service
from app.services.notification_service import notify

# Sort modes for the public review list (Phase 15 D-3).
REVIEW_SORT_RELEVANCE = "relevance"
REVIEW_SORT_NEWEST = "newest"
REVIEW_SORT_HIGHEST = "highest"
REVIEW_SORT_LOWEST = "lowest"
REVIEW_SORTS = (
    REVIEW_SORT_RELEVANCE, REVIEW_SORT_NEWEST,
    REVIEW_SORT_HIGHEST, REVIEW_SORT_LOWEST,
)
REVIEW_SORT_LABELS = {
    REVIEW_SORT_RELEVANCE: "Relevance",
    REVIEW_SORT_NEWEST: "Newest",
    REVIEW_SORT_HIGHEST: "Highest rated",
    REVIEW_SORT_LOWEST: "Lowest rated",
}
REVIEWS_PER_PAGE = 5


# --------------------------------------------------------------------------
# eligibility
# --------------------------------------------------------------------------
def has_delivered_purchase(user, product):
    """True when `user` has a delivered sub-order containing `product`."""
    row = (
        db.session.query(OrderItem.id)
        .join(SubOrder, OrderItem.sub_order_id == SubOrder.id)
        .join(Order, SubOrder.order_id == Order.id)
        .filter(
            Order.customer_id == user.id,
            OrderItem.product_id == product.id,
            SubOrder.status == SUBORDER_DELIVERED,
        )
        .first()
    )
    return row is not None


def existing_review(user, product):
    return Review.query.filter_by(user_id=user.id, product_id=product.id).first()


def can_review(user, product):
    """A user may review only a delivered product (one review per product)."""
    return has_delivered_purchase(user, product)


def reviewable_products(user):
    """Products the user has received but not yet reviewed."""
    delivered = {
        row[0] for row in db.session.query(OrderItem.product_id)
        .join(SubOrder, OrderItem.sub_order_id == SubOrder.id)
        .join(Order, SubOrder.order_id == Order.id)
        .filter(
            Order.customer_id == user.id,
            SubOrder.status == SUBORDER_DELIVERED,
            OrderItem.product_id.isnot(None),
        ).distinct()
    }
    reviewed = {
        row[0] for row in
        db.session.query(Review.product_id).filter(Review.user_id == user.id)
    }
    pending = delivered - reviewed
    return Product.query.filter(Product.id.in_(pending)).all() if pending else []


# --------------------------------------------------------------------------
# rating aggregates
# --------------------------------------------------------------------------
def recompute_product_rating(product):
    """Refresh a product's `rating_avg` / `rating_count` from its reviews."""
    count, avg = (
        db.session.query(func.count(Review.id), func.avg(Review.rating))
        .filter(Review.product_id == product.id).first()
    )
    product.rating_count = count or 0
    product.rating_avg = round(float(avg), 2) if count else 0


def recompute_vendor_rating(vendor):
    """Refresh a vendor's rating — averaged over every review of its products."""
    count, avg = (
        db.session.query(func.count(Review.id), func.avg(Review.rating))
        .join(Product, Review.product_id == Product.id)
        .filter(Product.vendor_id == vendor.id).first()
    )
    vendor.rating_count = count or 0
    vendor.rating_avg = round(float(avg), 2) if count else 0


# --------------------------------------------------------------------------
# create / update / delete
# --------------------------------------------------------------------------
def submit_review(user, product, rating, title=None, comment=None):
    """Create or update the user's review of a product.

    Returns ``(Review, None)`` on success or ``(None, error_str)``.
    """
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return None, "Please give a star rating."
    if not RATING_MIN <= rating <= RATING_MAX:
        return None, f"Rating must be between {RATING_MIN} and {RATING_MAX}."
    if not can_review(user, product):
        return None, ("You can review a product only after it has been "
                      "delivered to you.")

    review = existing_review(user, product)
    is_new = review is None
    if is_new:
        review = Review(user_id=user.id, product_id=product.id, rating=rating)
        db.session.add(review)
        db.session.flush()                # need review.id for the policy ref

    # Anti-disintermediation: redact phone numbers from review text. Customers
    # are not logged (they cannot be auto-suspended); a seller using this
    # surface (rare — only happens if they review their own customer's
    # product) is logged via `policy_service`.
    clean_title, _, _ = policy_service.redact_and_log(
        user, (title or "").strip(),
        SURFACE_REVIEW, ref_kind="review", ref_id=review.id,
    )
    clean_comment, _, _ = policy_service.redact_and_log(
        user, (comment or "").strip(),
        SURFACE_REVIEW, ref_kind="review", ref_id=review.id,
    )

    review.rating = rating
    review.title = clean_title or None
    review.comment = clean_comment or None
    review.is_verified = True
    db.session.flush()

    recompute_product_rating(product)
    if product.vendor is not None:
        recompute_vendor_rating(product.vendor)
        if is_new:
            notify(
                product.vendor.user_id, NOTIF_PRODUCT,
                f"New {rating}★ review",
                f"{user.name} reviewed '{product.title_en}'.",
                url=f"/product/{product.slug}/",
            )
    db.session.commit()
    return review, None


# --------------------------------------------------------------------------
# distribution / pagination / photo gallery (Phase 15 D-3)
# --------------------------------------------------------------------------
def rating_distribution(product):
    """Return ``{5: n5, 4: n4, 3: n3, 2: n2, 1: n1}`` for a product."""
    rows = (
        db.session.query(Review.rating, func.count(Review.id))
        .filter(Review.product_id == product.id)
        .group_by(Review.rating).all()
    )
    counts = {r: 0 for r in range(RATING_MIN, RATING_MAX + 1)}
    for rating, n in rows:
        if rating in counts:
            counts[rating] = int(n)
    return counts


def paginated_reviews(product, sort=REVIEW_SORT_NEWEST,
                      star_filter=None, page=1, per_page=REVIEWS_PER_PAGE):
    """Filter + sort + paginate a product's reviews for the public listing.

    `sort` is one of `REVIEW_SORTS`; `star_filter` is an int 1..5 to keep
    only those ratings, otherwise None for all stars.
    """
    if sort not in REVIEW_SORTS:
        sort = REVIEW_SORT_NEWEST

    query = Review.query.filter(Review.product_id == product.id)
    if star_filter in range(RATING_MIN, RATING_MAX + 1):
        query = query.filter(Review.rating == star_filter)

    if sort == REVIEW_SORT_HIGHEST:
        query = query.order_by(Review.rating.desc(), Review.id.desc())
    elif sort == REVIEW_SORT_LOWEST:
        query = query.order_by(Review.rating.asc(), Review.id.desc())
    elif sort == REVIEW_SORT_RELEVANCE:
        # Reviews with a comment and images surface first, then newest.
        has_comment = func.coalesce(func.length(Review.comment), 0)
        photo_count = (
            db.session.query(func.count(ReviewImage.id))
            .filter(ReviewImage.review_id == Review.id)
            .correlate(Review).scalar_subquery()
        )
        query = query.order_by(
            (photo_count > 0).desc(), (has_comment > 0).desc(),
            Review.id.desc(),
        )
    else:                                 # newest (default)
        query = query.order_by(Review.id.desc())

    return query.paginate(page=max(1, page), per_page=per_page, error_out=False)


def review_photos(product, limit=24):
    """Aggregate `ReviewImage` rows across all reviews of a product."""
    return (
        ReviewImage.query.join(Review, ReviewImage.review_id == Review.id)
        .filter(Review.product_id == product.id)
        .order_by(ReviewImage.id.desc()).limit(limit).all()
    )


def delete_review(review):
    """Remove a review and refresh the affected aggregates."""
    product = review.product
    db.session.delete(review)
    db.session.flush()
    recompute_product_rating(product)
    if product.vendor is not None:
        recompute_vendor_rating(product.vendor)
    db.session.commit()


# --------------------------------------------------------------------------
# serialization (REST API)
# --------------------------------------------------------------------------
def review_json(review):
    return {
        "id": review.id,
        "product_id": review.product_id,
        "rating": review.rating,
        "title": review.title,
        "comment": review.comment,
        "is_verified": review.is_verified,
        "author": review.user.name if review.user else "Customer",
        "created_at": review.created_at.isoformat() if review.created_at else None,
    }
