"""Marketing models — Phase 9.

Coupons come in two scopes:
  * platform — created by admins, valid across the whole marketplace.
  * vendor   — created by a seller, valid only on that seller's items.

`CouponRedemption` records each use so per-user and total usage limits can
be enforced.
"""
from datetime import datetime

from app.extensions import db
from app.utils.i18n import localized

COUPON_PLATFORM = "platform"
COUPON_VENDOR = "vendor"
COUPON_SCOPES = (COUPON_PLATFORM, COUPON_VENDOR)

DISCOUNT_PERCENT = "percent"   # discount_value is a percentage (0-100)
DISCOUNT_FIXED = "fixed"       # discount_value is a flat amount in Taka
DISCOUNT_TYPES = (DISCOUNT_PERCENT, DISCOUNT_FIXED)


class Coupon(db.Model):
    """A discount code applied at checkout."""

    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(40), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200))
    description_bn = db.Column(db.String(200))

    scope = db.Column(db.String(20), nullable=False, default=COUPON_PLATFORM)
    # Set for vendor coupons — the only store the coupon is valid on.
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor_profiles.id"), index=True)

    discount_type = db.Column(db.String(10), nullable=False, default=DISCOUNT_PERCENT)
    discount_value = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    # Eligible-amount floor and (for percentage coupons) a discount cap.
    min_order_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    max_discount = db.Column(db.Numeric(12, 2))

    # Usage limits — None means unlimited.
    usage_limit = db.Column(db.Integer)
    per_user_limit = db.Column(db.Integer, nullable=False, default=1)
    used_count = db.Column(db.Integer, nullable=False, default=0)

    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vendor = db.relationship("VendorProfile", backref="coupons")
    redemptions = db.relationship(
        "CouponRedemption", backref="coupon", cascade="all, delete-orphan"
    )

    @property
    def is_vendor_coupon(self):
        return self.scope == COUPON_VENDOR

    @property
    def localized_description(self):
        return localized(self.description, self.description_bn)

    def __repr__(self):
        return f"<Coupon {self.code} ({self.scope})>"


class FlashSale(db.Model):
    """A time-boxed sale event. Activating it applies the flash prices to the
    listed products; deactivating restores them (see flash_sale_service).

    When `vendor_id` is set, the sale is seller-owned — only that seller's
    products can be in it, and only that seller (or admin) can manage it.
    Null vendor = platform-wide sale (admin-owned).
    """

    __tablename__ = "flash_sales"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    title_bn = db.Column(db.String(160))
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    description_bn = db.Column(db.Text)
    banner = db.Column(db.String(255))

    # Seller-led flash sales (Phase 15 Chunk C). Null = admin/platform sale.
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor_profiles.id"), index=True)

    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    # True once the sale's prices have been applied to its products.
    is_active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship(
        "FlashSaleItem", backref="flash_sale", cascade="all, delete-orphan"
    )
    vendor = db.relationship("VendorProfile", backref="flash_sales")

    @property
    def is_seller_owned(self):
        return self.vendor_id is not None

    @property
    def localized_title(self):
        return localized(self.title, self.title_bn)

    @property
    def localized_description(self):
        return localized(self.description, self.description_bn)

    def __repr__(self):
        return f"<FlashSale {self.slug}>"


class FlashSaleItem(db.Model):
    """A product on sale within a flash sale, with its discounted price."""

    __tablename__ = "flash_sale_items"
    __table_args__ = (
        db.UniqueConstraint("flash_sale_id", "product_id",
                            name="uq_flash_sale_product"),
    )

    id = db.Column(db.Integer, primary_key=True)
    flash_sale_id = db.Column(
        db.Integer, db.ForeignKey("flash_sales.id"), nullable=False, index=True
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    flash_price = db.Column(db.Numeric(12, 2), nullable=False)
    # The product's discount_price before this sale — restored on deactivation.
    original_discount_price = db.Column(db.Numeric(12, 2))

    product = db.relationship("Product")

    def __repr__(self):
        return f"<FlashSaleItem sale={self.flash_sale_id} product={self.product_id}>"


class RewardLedger(db.Model):
    """One reward-points movement — positive on earn, negative on redeem.

    The user's running balance lives on `User.reward_points`; this table is
    the audit trail.
    """

    __tablename__ = "reward_ledger"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    points = db.Column(db.Integer, nullable=False)        # signed
    reason = db.Column(db.String(200))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship(
        "User", backref=db.backref("reward_ledger", cascade="all, delete-orphan")
    )
    order = db.relationship("Order")

    def __repr__(self):
        return f"<RewardLedger user={self.user_id} {self.points:+d}>"


class Referral(db.Model):
    """A signup referral — the referrer is rewarded when the referee's first
    order is placed."""

    __tablename__ = "referrals"

    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    # Each new account can be referred at most once.
    referee_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    reward_points = db.Column(db.Integer, nullable=False, default=0)
    is_rewarded = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    referrer = db.relationship("User", foreign_keys=[referrer_id])
    referee = db.relationship("User", foreign_keys=[referee_id])

    def __repr__(self):
        return f"<Referral {self.referrer_id} -> {self.referee_id}>"


class AffiliateCommission(db.Model):
    """A commission earned when a purchase is made through an affiliate's
    share link (a product/store URL carrying their referral code)."""

    __tablename__ = "affiliate_commissions"

    id = db.Column(db.Integer, primary_key=True)
    affiliate_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    affiliate = db.relationship("User", foreign_keys=[affiliate_id])
    order = db.relationship("Order")

    def __repr__(self):
        return f"<AffiliateCommission affiliate={self.affiliate_id} +{self.points}>"


class AbandonedCart(db.Model):
    """A snapshot of a customer's stale cart — one row per customer, refreshed
    by the abandoned-cart scan, used to send (one) recovery reminder."""

    __tablename__ = "abandoned_carts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )
    item_count = db.Column(db.Integer, nullable=False, default=0)
    cart_value = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    reminder_sent_at = db.Column(db.DateTime)
    is_recovered = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")

    def __repr__(self):
        return f"<AbandonedCart user={self.user_id} items={self.item_count}>"


class CouponRedemption(db.Model):
    """One use of a coupon by a customer on an order."""

    __tablename__ = "coupon_redemptions"

    id = db.Column(db.Integer, primary_key=True)
    coupon_id = db.Column(
        db.Integer, db.ForeignKey("coupons.id"), nullable=False, index=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")
    order = db.relationship("Order")

    def __repr__(self):
        return f"<CouponRedemption coupon={self.coupon_id} user={self.user_id}>"
