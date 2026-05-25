"""Shopping cart model — Phase 3.

A DB-backed cart per logged-in customer (replaces KUMO's session cart).
The cart is simply the set of CartItem rows for a user.
"""
from datetime import datetime

from app.extensions import db


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"))
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        "User", backref=db.backref("cart_items", cascade="all, delete-orphan")
    )
    product = db.relationship("Product")
    variant = db.relationship("ProductVariant")

    @property
    def base_unit_price(self):
        """Variant price when the variant sets one, else the product price."""
        if self.variant is not None and self.variant.price is not None:
            return self.variant.price
        return self.product.current_price

    @property
    def unit_price(self):
        """Effective price after any bulk-pricing tier (Phase 15 D-5)."""
        # Lazy import — the pricing service imports a catalog model.
        from app.services.pricing_service import effective_unit_price
        return effective_unit_price(
            self.product, self.quantity, self.base_unit_price,
        )

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __repr__(self):
        return f"<CartItem user={self.user_id} product={self.product_id}>"
