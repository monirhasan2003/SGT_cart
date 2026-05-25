"""Order models — Phase 3.

A customer places ONE Order. Its items are split into per-vendor SubOrders
(each vendor fulfils independently). Platform commission is computed per
SubOrder at order time.
"""
from datetime import datetime

from app.extensions import db

# Payment
PAYMENT_COD = "cod"
PAYMENT_SSLCOMMERZ = "sslcommerz"
PAYMENT_PENDING = "pending"
PAYMENT_PAID = "paid"
PAYMENT_FAILED = "failed"

# Per-vendor sub-order fulfilment status
SUBORDER_PENDING = "pending"
SUBORDER_PROCESSING = "processing"
SUBORDER_SHIPPED = "shipped"
SUBORDER_DELIVERED = "delivered"
SUBORDER_CANCELLED = "cancelled"
SUBORDER_STATUSES = (
    SUBORDER_PENDING, SUBORDER_PROCESSING, SUBORDER_SHIPPED,
    SUBORDER_DELIVERED, SUBORDER_CANCELLED,
)


class Order(db.Model):
    """A customer's whole basket — one payment, one shipping address."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    order_number = db.Column(db.String(24), unique=True, nullable=False, index=True)

    subtotal = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    shipping_fee = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    # Coupon discount applied at checkout (Phase 9).
    discount_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    coupon_code = db.Column(db.String(40))
    # Reward-points redeemed against this order (Phase 9).
    points_redeemed = db.Column(db.Integer, nullable=False, default=0)
    points_discount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    payment_method = db.Column(db.String(20), nullable=False, default=PAYMENT_COD)
    payment_status = db.Column(db.String(20), nullable=False, default=PAYMENT_PENDING)

    # Shipping address — snapshot at order time (the saved Address may change).
    ship_name = db.Column(db.String(120), nullable=False)
    ship_phone = db.Column(db.String(20), nullable=False)
    ship_address_line = db.Column(db.String(255), nullable=False)
    ship_area = db.Column(db.String(120))
    ship_city = db.Column(db.String(120), nullable=False)
    ship_district = db.Column(db.String(120))
    ship_postal_code = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship("User", backref="orders")
    suborders = db.relationship(
        "SubOrder", back_populates="order", cascade="all, delete-orphan"
    )

    @property
    def item_count(self):
        return sum(len(s.items) for s in self.suborders)

    def __repr__(self):
        return f"<Order {self.order_number}>"


class SubOrder(db.Model):
    """The slice of an Order belonging to one vendor."""

    __tablename__ = "sub_orders"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)
    vendor_id = db.Column(
        db.Integer, db.ForeignKey("vendor_profiles.id"), nullable=False, index=True
    )

    subtotal = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    commission_rate = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    commission_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    vendor_earning = db.Column(db.Numeric(12, 2), nullable=False, default=0)

    status = db.Column(db.String(20), nullable=False, default=SUBORDER_PENDING, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship("Order", back_populates="suborders")
    vendor = db.relationship("VendorProfile", backref="sub_orders")
    items = db.relationship(
        "OrderItem", back_populates="sub_order", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<SubOrder {self.id} order={self.order_id} vendor={self.vendor_id}>"


class OrderItem(db.Model):
    """A single product line within a SubOrder (price/title snapshotted)."""

    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    sub_order_id = db.Column(
        db.Integer, db.ForeignKey("sub_orders.id"), nullable=False, index=True
    )
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    variant_id = db.Column(db.Integer, db.ForeignKey("product_variants.id"))

    title = db.Column(db.String(200), nullable=False)        # snapshot
    variant_label = db.Column(db.String(100))                # snapshot e.g. "L / Red"
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    line_total = db.Column(db.Numeric(12, 2), nullable=False)

    sub_order = db.relationship("SubOrder", back_populates="items")
    product = db.relationship("Product")

    def __repr__(self):
        return f"<OrderItem {self.title} x{self.quantity}>"


class SubOrderEvent(db.Model):
    """A timestamped entry in a sub-order's tracking history (Phase 8).

    One row per status change; the customer sees these as a live timeline.
    """

    __tablename__ = "sub_order_events"

    id = db.Column(db.Integer, primary_key=True)
    sub_order_id = db.Column(
        db.Integer, db.ForeignKey("sub_orders.id"), nullable=False, index=True
    )
    status = db.Column(db.String(20), nullable=False)
    note = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    sub_order = db.relationship(
        "SubOrder",
        backref=db.backref("events", cascade="all, delete-orphan",
                           order_by="SubOrderEvent.id"),
    )

    def __repr__(self):
        return f"<SubOrderEvent sub={self.sub_order_id} {self.status}>"
