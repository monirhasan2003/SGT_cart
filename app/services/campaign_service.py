"""Festival / Eid campaign strip — Phase 15 D-9 B5.

Configured through three platform settings:
  * `campaign_label_en`   — main strip text in English.
  * `campaign_label_bn`   — Bengali rendering shown alongside.
  * `campaign_ends_at`    — ISO ``YYYY-MM-DD`` end date (countdown target).

When `campaign_ends_at` is in the future *and* the English label is
non-empty, `active_campaign()` returns a dict with the timer end so the
product page can show a "Eid Special — ends in 3d 4h" badge with a
client-side countdown.
"""
from datetime import datetime

from app.services.settings_service import get_setting


def active_campaign(now=None):
    """Return the active campaign dict, or None when nothing is configured."""
    now = now or datetime.utcnow()
    label_en = (get_setting("campaign_label_en") or "").strip()
    if not label_en:
        return None
    ends_raw = (get_setting("campaign_ends_at") or "").strip()
    if not ends_raw:
        return None
    try:
        ends = datetime.strptime(ends_raw, "%Y-%m-%d")
    except ValueError:
        return None
    if ends <= now:
        return None
    return {
        "label_en": label_en,
        "label_bn": (get_setting("campaign_label_bn") or "").strip(),
        "ends_at": ends,
        "ends_iso": ends.isoformat(),
    }
