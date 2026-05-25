"""Stock-notification model — Phase 15 D-6.

A customer (or an anonymous visitor giving their email) can subscribe to be
notified when an out-of-stock product is restocked. When the seller raises
stock from 0 to a positive number, `stock_service.notify_back_in_stock`
emails everyone with `notified_at IS NULL` and stamps the column.
"""
from datetime import datetime

from app.extensions import db


class StockNotification(db.Model):
    """One pending back-in-stock subscription for a product."""

    __tablename__ = "stock_notifications"
    __table_args__ = (
        # One pending subscription per (product, email) avoids spamming
        # someone who clicks twice. A user can re-subscribe after delivery
        # because the next subscription is created with a fresh row only
        # when an existing one is already notified (logic in service).
        db.UniqueConstraint(
            "product_id", "email", name="uq_stock_notif_product_email",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    notified_at = db.Column(db.DateTime, index=True)

    product = db.relationship(
        "Product",
        backref=db.backref(
            "stock_notifications", cascade="all, delete-orphan",
        ),
    )
    user = db.relationship("User")

    def __repr__(self):
        return f"<StockNotification {self.id} product={self.product_id} {self.email}>"
