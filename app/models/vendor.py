"""Vendor (seller) profile model — Phase 1 (Auth & Users)."""
from datetime import datetime

from app.extensions import db

VENDOR_PENDING = "pending"
VENDOR_APPROVED = "approved"
VENDOR_SUSPENDED = "suspended"
VENDOR_STATUSES = (VENDOR_PENDING, VENDOR_APPROVED, VENDOR_SUSPENDED)


class VendorProfile(db.Model):
    """Seller shop details. A seller can list products only once approved."""

    __tablename__ = "vendor_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False
    )

    # Bilingual shop identity (one language mandatory, the other optional).
    shop_name_en = db.Column(db.String(150), nullable=False)
    shop_name_bn = db.Column(db.String(150))
    slug = db.Column(db.String(180), unique=True, nullable=False, index=True)
    logo = db.Column(db.String(255))
    banner = db.Column(db.String(255))          # store cover image
    description_en = db.Column(db.Text)
    description_bn = db.Column(db.Text)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))

    status = db.Column(db.String(20), nullable=False, default=VENDOR_PENDING)
    # Platform commission this vendor pays, in percent.
    commission_rate = db.Column(db.Numeric(5, 2), nullable=False, default=10.00)

    # Seller rating — averaged across all reviews of this vendor's products
    # (Phase 9). Drives search / homepage ranking in Phase 10.
    rating_avg = db.Column(db.Numeric(3, 2), nullable=False, default=0)
    rating_count = db.Column(db.Integer, nullable=False, default=0)
    # Admin ranking override (Phase 10) — added to the seller's rating when
    # ordering search results. 0 = neutral (rating-driven); +/- nudges a shop.
    ranking_boost = db.Column(db.Numeric(4, 2), nullable=False, default=0)

    # Computed performance signals (Phase 15 v3b) — refreshed by
    # `vendor_stats_service.recompute_vendor_stats` on each delivery /
    # cancellation and via the `recompute-vendor-stats` CLI / cron.
    avg_delivery_days = db.Column(db.Numeric(5, 2), nullable=False, default=0)
    cancel_rate = db.Column(db.Numeric(5, 4), nullable=False, default=0)

    # Store promotion banner (Phase 15 Chunk C) — the seller's own marketing
    # message shown atop their store page. Auto-hidden after `promo_until`.
    promo_banner_text = db.Column(db.String(240))
    promo_banner_image = db.Column(db.String(255))
    promo_until = db.Column(db.DateTime)

    # --- Verification / KYC (submitted by the seller, reviewed by admin) ---
    # The admin should only approve a vendor after reviewing these documents.
    business_type = db.Column(db.String(50))           # individual / company
    city = db.Column(db.String(120))
    trade_license_no = db.Column(db.String(80))
    trade_license_doc = db.Column(db.String(255))      # uploaded file (static path)
    nid_number = db.Column(db.String(50))              # owner's national ID
    nid_doc = db.Column(db.String(255))                # uploaded file (static path)
    verification_submitted_at = db.Column(db.DateTime)

    # Payout details — where the seller receives money from the platform.
    # The platform collects all customer payments, deducts commission, and
    # pays the seller out to one of these (processed in Phase 4 / Phase 7).
    bank_account_name = db.Column(db.String(120))
    bank_account_number = db.Column(db.String(50))
    bank_name = db.Column(db.String(120))
    bkash_number = db.Column(db.String(20))
    nagad_number = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="vendor_profile")

    @property
    def is_approved(self):
        return self.status == VENDOR_APPROVED

    @property
    def is_verification_submitted(self):
        """True once the seller has submitted their KYC documents."""
        return self.verification_submitted_at is not None

    @property
    def is_verified_seller(self):
        """True when the seller is approved AND both KYC docs are on file.

        The product page's "Verified by SGT" badge (Phase 15 D-4) requires
        this stricter check — admin-approved + both trade license and NID
        actually uploaded, not just `verification_submitted_at` flagged.
        """
        return (
            self.status == VENDOR_APPROVED
            and bool(self.trade_license_doc)
            and bool(self.nid_doc)
        )

    @property
    def has_trade_license_verified(self):
        return self.status == VENDOR_APPROVED and bool(self.trade_license_doc)

    @property
    def has_nid_verified(self):
        return self.status == VENDOR_APPROVED and bool(self.nid_doc)

    @property
    def has_active_promo(self):
        """True while the store promotion banner should be shown."""
        if not (self.promo_banner_text or self.promo_banner_image):
            return False
        if self.promo_until is None:
            return True
        return self.promo_until >= datetime.utcnow()

    @property
    def is_mall_tier(self):
        """Premium seller tier — derived from review aggregates.

        Thresholds come from the `mall_min_rating` / `mall_min_reviews`
        platform settings so the admin can re-tune the bar over time.
        Imported lazily to avoid circular imports.
        """
        from app.services.settings_service import get_decimal
        try:
            min_rating = float(get_decimal("mall_min_rating") or 4.5)
            min_reviews = int(get_decimal("mall_min_reviews") or 20)
        except Exception:  # noqa: BLE001
            min_rating, min_reviews = 4.5, 20
        return (
            self.status == VENDOR_APPROVED
            and (self.rating_count or 0) >= min_reviews
            and float(self.rating_avg or 0) >= min_rating
        )

    def __repr__(self):
        return f"<VendorProfile {self.slug} ({self.status})>"
