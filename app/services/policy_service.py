"""Policy enforcement service — Phase 15 Chunk D-0.

Wraps the phone-number guard with anti-disintermediation enforcement:

  * Customer redactions are silent — text is cleaned, nothing else happens.
  * Seller redactions log a `PolicyViolation`. Once a seller crosses
    `SELLER_VIOLATION_THRESHOLD`, their `VendorProfile` is auto-suspended
    and both admin + seller are notified. The admin can manually un-suspend
    from `/admin/vendors/<id>/`.

Marketplace rule: see `marketplace-feature-rules` memory.
"""
from app.extensions import db
from app.models.user import User, ROLE_ADMIN
from app.models.vendor import VendorProfile, VENDOR_SUSPENDED
from app.models.notification import NOTIF_SYSTEM
from app.models.policy import (
    PolicyViolation, SURFACES, SELLER_VIOLATION_THRESHOLD,
)
from app.services.notification_service import notify
from app.services.settings_service import log_action
from app.utils.phone_guard import redact_phone_numbers


def _is_seller(user):
    """True when the user account is a seller with a vendor profile."""
    return (
        user is not None
        and getattr(user, "is_seller", False)
        and getattr(user, "vendor_profile", None) is not None
    )


def seller_violation_count(user_id):
    """How many violations the given seller account has logged."""
    return PolicyViolation.query.filter_by(user_id=user_id).count()


def vendor_violation_count(vendor):
    """Convenience: violation count keyed by VendorProfile."""
    return seller_violation_count(vendor.user_id) if vendor else 0


def last_violation_at(user_id):
    row = (
        PolicyViolation.query.filter_by(user_id=user_id)
        .order_by(PolicyViolation.id.desc()).first()
    )
    return row.created_at if row else None


def redact_and_log(user, text, surface, ref_kind=None, ref_id=None):
    """Run the phone guard on `text` and, for sellers, log + maybe suspend.

    Returns ``(clean_text, was_redacted, violation_or_None)``. The caller is
    expected to commit (the violation row + any suspension are added to the
    current session and ``flush()``ed only).
    """
    if surface not in SURFACES:
        raise ValueError(f"Unknown policy surface: {surface!r}")

    clean, flagged = redact_phone_numbers(text)
    if not flagged or not _is_seller(user):
        return clean, flagged, None

    excerpt = (text or "")[:500]
    violation = PolicyViolation(
        user_id=user.id, surface=surface,
        excerpt=excerpt, ref_kind=ref_kind, ref_id=ref_id,
    )
    db.session.add(violation)
    db.session.flush()

    total = seller_violation_count(user.id)
    vendor = user.vendor_profile
    if vendor is not None and total >= SELLER_VIOLATION_THRESHOLD \
            and vendor.status != VENDOR_SUSPENDED:
        vendor.status = VENDOR_SUSPENDED
        log_action(
            "Auto-suspended vendor (policy)",
            f"{vendor.shop_name_en} — {total} phone-share violation(s)",
        )
        notify(
            vendor.user_id, NOTIF_SYSTEM, "Your shop has been suspended",
            "Your account has shared (or tried to share) a phone number "
            f"{total} times, which is against our anti-disintermediation "
            "policy. Contact SGT Support to appeal.",
            url="/messages/new",
        )
        for admin in User.query.filter_by(role=ROLE_ADMIN).all():
            notify(
                admin.id, NOTIF_SYSTEM, "Vendor auto-suspended (policy)",
                f"{vendor.shop_name_en} crossed {SELLER_VIOLATION_THRESHOLD} "
                "phone-share violations and was auto-suspended.",
                url=f"/admin/vendors/{vendor.id}/",
            )

    return clean, flagged, violation
