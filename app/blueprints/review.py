"""Product reviews — Phase 9 web views.

A review is verified-purchase only: the customer must have a delivered
sub-order containing the product. Reviews update the product & seller
rating aggregates via `review_service`.
"""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, abort,
)
from flask_login import login_required, current_user

from app.extensions import db
from app.models.catalog import Product
from app.models.review import Review, ReviewImage
from app.services.review_service import (
    submit_review, delete_review, can_review, existing_review, reviewable_products,
)
from app.utils.uploads import save_upload

review = Blueprint("review", __name__)


@review.route("/reviews/")
@login_required
def my_reviews():
    """Products the customer can still review + the reviews already written."""
    pending = reviewable_products(current_user)
    written = (
        Review.query.filter_by(user_id=current_user.id)
        .order_by(Review.id.desc()).all()
    )
    return render_template("pages/my-reviews.html", pending=pending, reviews=written)


@review.route("/reviews/write/<slug>", methods=["GET", "POST"])
@login_required
def write(slug):
    product = Product.query.filter_by(slug=slug).first() or abort(404)
    if not can_review(current_user, product):
        flash("You can review this product only after it has been delivered to you.",
              "warning")
        return redirect(url_for("storefront.product_detail", slug=slug))

    current = existing_review(current_user, product)
    if request.method == "POST":
        rev, error = submit_review(
            current_user, product,
            request.form.get("rating"),
            request.form.get("title"),
            request.form.get("comment"),
        )
        if error:
            flash(error, "danger")
            return render_template("pages/review-form.html",
                                   product=product, review=current)
        for file in request.files.getlist("images"):
            path = save_upload(file, "reviews")
            if path:
                db.session.add(ReviewImage(review_id=rev.id, image_path=path))
        db.session.commit()
        flash("Thank you! Your review has been posted.", "success")
        return redirect(url_for("storefront.product_detail", slug=slug))

    return render_template("pages/review-form.html", product=product, review=current)


@review.route("/reviews/<int:review_id>/delete", methods=["POST"])
@login_required
def remove(review_id):
    rev = db.session.get(Review, review_id)
    if rev is None or rev.user_id != current_user.id:
        abort(404)
    delete_review(rev)
    flash("Your review has been removed.", "info")
    return redirect(url_for("review.my_reviews"))
