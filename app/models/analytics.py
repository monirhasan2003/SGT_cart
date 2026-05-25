"""Analytics / signal models — Phase 10.

`ProductView` and `SearchLog` capture browsing behaviour. They power smart
search, autocomplete and the recommendation engine, and feed the seller /
admin analytics dashboards in Phase 11.
"""
from datetime import datetime

from app.extensions import db


class ProductView(db.Model):
    """One visit to a product detail page (anonymous when user_id is null)."""

    __tablename__ = "product_views"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Views are disposable signal data — they go when the product/user goes.
    product = db.relationship(
        "Product", backref=db.backref("views", cascade="all, delete-orphan")
    )
    user = db.relationship(
        "User", backref=db.backref("product_views", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<ProductView product={self.product_id}>"


class SearchLog(db.Model):
    """One catalog search — drives autocomplete and trending queries.

    The search text column is `term` (not `query`) so it does not shadow
    Flask-SQLAlchemy's `Model.query`.
    """

    __tablename__ = "search_logs"

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(160), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    result_count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship(
        "User", backref=db.backref("search_logs", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<SearchLog {self.term!r}>"
