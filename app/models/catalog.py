"""Catalog models — Phase 2 (categories, brands, products, variants, images).

Bilingual text fields use `*_en` / `*_bn` pairs resolved by `localized()`.
"""
from datetime import datetime

from app.extensions import db
from app.utils.i18n import localized

# Product lifecycle.
PRODUCT_DRAFT = "draft"          # seller is still editing
PRODUCT_PENDING = "pending"      # submitted, awaiting admin review
PRODUCT_PUBLISHED = "published"  # live on the storefront
PRODUCT_REJECTED = "rejected"    # admin rejected
PRODUCT_STATUSES = (PRODUCT_DRAFT, PRODUCT_PENDING, PRODUCT_PUBLISHED, PRODUCT_REJECTED)


class Category(db.Model):
    """Product category — bilingual, self-referencing tree (sub-categories)."""

    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name_en = db.Column(db.String(120), nullable=False)
    name_bn = db.Column(db.String(120))
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    image = db.Column(db.String(255))
    parent_id = db.Column(db.Integer, db.ForeignKey("categories.id"))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    children = db.relationship(
        "Category",
        backref=db.backref("parent", remote_side=[id]),
        cascade="all, delete-orphan",
    )

    @property
    def localized_name(self):
        return localized(self.name_en, self.name_bn)

    def __repr__(self):
        return f"<Category {self.slug}>"


class Brand(db.Model):
    """Optional product brand."""

    __tablename__ = "brands"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(150), unique=True, nullable=False, index=True)
    logo = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Brand {self.slug}>"


class Product(db.Model):
    """A product listed by a vendor."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(
        db.Integer, db.ForeignKey("vendor_profiles.id"), nullable=False, index=True
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey("categories.id"), nullable=False, index=True
    )
    brand_id = db.Column(db.Integer, db.ForeignKey("brands.id"))

    # Bilingual content (one language mandatory, the other optional).
    title_en = db.Column(db.String(200), nullable=False)
    title_bn = db.Column(db.String(200))
    slug = db.Column(db.String(230), unique=True, nullable=False, index=True)
    description_en = db.Column(db.Text)
    description_bn = db.Column(db.Text)

    base_price = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    discount_price = db.Column(db.Numeric(12, 2))   # optional sale price
    sku = db.Column(db.String(80))
    stock = db.Column(db.Integer, nullable=False, default=0)
    thumbnail = db.Column(db.String(255))

    status = db.Column(db.String(20), nullable=False, default=PRODUCT_DRAFT, index=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False)

    # Admin-controlled paid promotion (Phase 15 v3c) — when active, the
    # product surfaces above regular ordering with a Sponsored badge.
    is_sponsored = db.Column(db.Boolean, nullable=False, default=False, index=True)
    sponsored_until = db.Column(db.DateTime)

    # Review aggregates — maintained by review_service (Phase 9).
    rating_avg = db.Column(db.Numeric(3, 2), nullable=False, default=0)
    rating_count = db.Column(db.Integer, nullable=False, default=0)

    # Phase 15 D-8 — cached AI pros/cons summary, refreshed nightly.
    # Stored as JSON-encoded lists so the heuristic and the LLM-backed
    # producer share the same shape.
    ai_pros_json = db.Column(db.Text)
    ai_cons_json = db.Column(db.Text)
    ai_summary_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vendor = db.relationship(
        "VendorProfile", backref=db.backref("products", cascade="all, delete-orphan")
    )
    category = db.relationship("Category", backref="products")
    brand = db.relationship("Brand", backref="products")
    variants = db.relationship(
        "ProductVariant", backref="product", cascade="all, delete-orphan"
    )
    images = db.relationship(
        "ProductImage", backref="product", cascade="all, delete-orphan",
        order_by="ProductImage.sort_order",
    )

    @property
    def localized_title(self):
        return localized(self.title_en, self.title_bn)

    @property
    def localized_description(self):
        return localized(self.description_en, self.description_bn)

    @property
    def is_published(self):
        return self.status == PRODUCT_PUBLISHED

    @property
    def is_sponsored_active(self):
        """True only while the paid promotion has not expired."""
        if not self.is_sponsored:
            return False
        if self.sponsored_until is None:
            return True
        return self.sponsored_until >= datetime.utcnow()

    @property
    def current_price(self):
        """Effective sale price (discount price when set)."""
        return self.discount_price if self.discount_price else self.base_price

    @property
    def primary_image(self):
        """Best image path for listings, or None."""
        for img in self.images:
            if img.is_primary:
                return img.image_path
        if self.thumbnail:
            return self.thumbnail
        return self.images[0].image_path if self.images else None

    def __repr__(self):
        return f"<Product {self.slug}>"


class ProductVariant(db.Model):
    """A size/color variant of a product with its own price and stock."""

    __tablename__ = "product_variants"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    price = db.Column(db.Numeric(12, 2))
    stock = db.Column(db.Integer, nullable=False, default=0)
    sku = db.Column(db.String(80))

    def __repr__(self):
        return f"<ProductVariant {self.id} of product {self.product_id}>"


class ProductImage(db.Model):
    """An image attached to a product."""

    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    image_path = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, nullable=False, default=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<ProductImage {self.id}>"


class ProductPriceTier(db.Model):
    """Quantity-based bulk-pricing tier — Phase 15 D-5.

    Sellers add rows like "2-pack: 5% off, 5-pack: 10% off". The cart's
    `CartItem.unit_price` looks up the highest-`min_quantity` row whose
    threshold the customer has met and applies its `discount_pct`.
    """

    __tablename__ = "product_price_tiers"
    __table_args__ = (
        db.UniqueConstraint("product_id", "min_quantity",
                            name="uq_price_tier_product_qty"),
    )

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    min_quantity = db.Column(db.Integer, nullable=False)
    discount_pct = db.Column(db.Numeric(5, 2), nullable=False)

    product = db.relationship(
        "Product", backref=db.backref(
            "price_tiers", cascade="all, delete-orphan",
            order_by="ProductPriceTier.min_quantity",
        ),
    )

    def __repr__(self):
        return f"<ProductPriceTier {self.product_id} q>={self.min_quantity} -{self.discount_pct}%>"


class ProductSpec(db.Model):
    """A structured key-value specification row — Phase 15 D-2.

    Distinct from the seller's free-form description: short label/value pairs
    rendered as a table on the product page, with a "View More" toggle once
    there are more than a few rows.
    """

    __tablename__ = "product_specs"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    label = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(500), nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    product = db.relationship(
        "Product", backref=db.backref(
            "specs", cascade="all, delete-orphan", order_by="ProductSpec.sort_order"),
    )

    def __repr__(self):
        return f"<ProductSpec {self.id} {self.label}>"
