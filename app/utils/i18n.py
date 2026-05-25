"""Bilingual content helper.

Product/category text is stored in `*_en` / `*_bn` column pairs (one mandatory,
the other optional). `localized()` returns the value for the active request
locale, falling back to whichever language is filled in.
"""
from flask import has_request_context
from flask_babel import get_locale


def localized(en, bn):
    """Return `bn` when the active locale is Bengali and `bn` is set, else `en`."""
    if has_request_context():
        try:
            if str(get_locale()) == "bn" and bn:
                return bn
        except Exception:  # noqa: BLE001 - never let locale lookup break rendering
            pass
    return en if en else bn


def tr(obj, field):
    """Locale-aware field picker for any model that follows the
    `<field>` / `<field>_bn` naming convention.

    Templates can use it as a filter:

        {{ category|tr('name') }}        -> name_bn (when bn) else name
        {{ product|tr('title') }}        -> title_bn else title_en
        {{ page|tr('body_html') }}       -> body_html_bn else body_html

    The fallback handles both naming styles — `<field>_en` (Category,
    Product, VendorProfile) and bare `<field>` (Brand, HomepageBanner,
    StaticPage, FlashSale, Coupon, Notification, ProductSpec).
    """
    if obj is None:
        return None
    # Try `<field>_en` first; if absent, fall back to `<field>` (some
    # models use the bare name for the English/canonical value).
    en = getattr(obj, f"{field}_en", None)
    if en is None:
        en = getattr(obj, field, None)
    bn = getattr(obj, f"{field}_bn", None)
    return localized(en, bn)
