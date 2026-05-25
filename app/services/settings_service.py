"""Platform settings & audit logging — Phase 6.

Settings are admin-configurable key/value pairs with sensible defaults.
Callers commit the session.
"""
from decimal import Decimal

from flask import has_request_context
from flask_login import current_user

from app.extensions import db
from app.models.setting import Setting, AuditLog

DEFAULTS = {
    "site_name": "SGT Cart",
    "default_commission_rate": "10.00",
    "shipping_fee_per_vendor": "60.00",
    "currency_symbol": "Tk",
    # Phase 15 Chunk D-1 — product page trust signals.
    "return_policy_days": "7",
    "warranty_default": "No warranty",
    "free_shipping_threshold": "1000.00",
    "mall_min_rating": "4.50",
    "mall_min_reviews": "20",
    # Phase 15 Chunk D-9 — festival / Eid pricing countdown strip.
    # Active when `campaign_ends_at` is in the future. Bengali label is
    # rendered alongside English on the product page.
    "campaign_label_en": "",
    "campaign_label_bn": "",
    "campaign_ends_at": "",          # ISO yyyy-mm-dd
    # Phase 15 Chunk D-10 — App download QR. Empty until the Flutter apps
    # ship in Phase 12; then admin sets this to the store link (Play /
    # App Store / one-link). The product page renders a QR code only
    # when this is non-empty.
    "app_download_url": "",
}


def get_setting(key, default=None):
    s = db.session.get(Setting, key)
    if s is not None and s.value not in (None, ""):
        return s.value
    return DEFAULTS.get(key, "" if default is None else default)


def get_decimal(key):
    try:
        return Decimal(get_setting(key) or "0")
    except Exception:  # noqa: BLE001
        return Decimal(DEFAULTS.get(key, "0") or "0")


def set_setting(key, value):
    s = db.session.get(Setting, key)
    if s is None:
        s = Setting(key=key)
        db.session.add(s)
    s.value = str(value)


def all_settings():
    """Full settings map — DB values layered over the defaults."""
    merged = dict(DEFAULTS)
    for s in Setting.query.all():
        if s.value is not None:
            merged[s.key] = s.value
    return merged


def log_action(action, target=None):
    """Record a significant admin action in the audit log."""
    actor_id, actor_name = None, "system"
    if has_request_context() and current_user.is_authenticated:
        actor_id = current_user.id
        actor_name = current_user.name
    db.session.add(AuditLog(
        actor_id=actor_id, actor_name=actor_name, action=action, target=target,
    ))
