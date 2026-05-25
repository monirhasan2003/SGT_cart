"""API v1 — product reviews (verified purchase).

Listing reviews is public; writing one requires a customer token and a
delivered purchase of the product.
"""
from flask import request, jsonify

from app.models.catalog import Product, PRODUCT_PUBLISHED
from app.models.review import Review
from app.services.review_service import (
    submit_review, can_review, existing_review, reviewable_products, review_json,
)
from .helpers import err, current_api_user, customer_required
from .serializers import product_card_json
from . import api_v1


@api_v1.route("/products/<slug>/reviews", methods=["GET"])
def list_reviews(slug):
    """Public — every review of a product, newest first."""
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        return err("Product not found.", 404)
    reviews = (
        Review.query.filter_by(product_id=product.id)
        .order_by(Review.id.desc()).all()
    )
    return jsonify({
        "rating": float(product.rating_avg or 0),
        "rating_count": product.rating_count or 0,
        "reviews": [review_json(r) for r in reviews],
    })


@api_v1.route("/products/<slug>/reviews", methods=["POST"])
@customer_required
def post_review(slug):
    """Create or update the customer's review (delivered purchase required)."""
    user = current_api_user()
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        return err("Product not found.", 404)

    data = request.get_json(silent=True) or {}
    review, error = submit_review(
        user, product, data.get("rating"), data.get("title"), data.get("comment"),
    )
    if error:
        return err(error, 403 if "delivered" in error else 400)
    return jsonify({"review": review_json(review)}), 201


@api_v1.route("/reviews/reviewable", methods=["GET"])
@customer_required
def reviewable():
    """Products the customer has received but not yet reviewed."""
    products = reviewable_products(current_api_user())
    return jsonify({"products": [product_card_json(p) for p in products]})


@api_v1.route("/reviews/mine", methods=["GET"])
@customer_required
def my_reviews():
    user = current_api_user()
    reviews = (
        Review.query.filter_by(user_id=user.id)
        .order_by(Review.id.desc()).all()
    )
    return jsonify({"reviews": [review_json(r) for r in reviews]})
