"""Product review models — Phase 9.

A review is a **verified purchase**: a customer may review a product only
after a sub-order containing it has been delivered to them (enforced in
`review_service`). Reviews feed the product and seller rating aggregates,
which drive search/homepage ranking in Phase 10.
"""
from datetime import datetime

from app.extensions import db

RATING_MIN = 1
RATING_MAX = 5


class Review(db.Model):
    """One customer's rating + comment for one product."""

    __tablename__ = "reviews"
    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="uq_review_user_product"),
    )

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )

    rating = db.Column(db.Integer, nullable=False)        # 1..5
    title = db.Column(db.String(160))
    comment = db.Column(db.Text)
    is_verified = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = db.relationship(
        "Product", backref=db.backref("reviews", cascade="all, delete-orphan")
    )
    user = db.relationship("User")
    images = db.relationship(
        "ReviewImage", backref="review", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Review {self.id} product={self.product_id} {self.rating}*>"


class ReviewImage(db.Model):
    """An optional photo attached to a review."""

    __tablename__ = "review_images"

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(
        db.Integer, db.ForeignKey("reviews.id"), nullable=False, index=True
    )
    image_path = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<ReviewImage {self.id} review={self.review_id}>"
