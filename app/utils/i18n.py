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
