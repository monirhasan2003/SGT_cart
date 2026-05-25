"""Scheduled / automated payouts — Phase 11.

`process_due_payouts` auto-approves payout requests that have been pending
longer than the configured grace period. Intended to run from a scheduler
(cron / Celery beat / the admin "Run now" button / the `process-payouts`
CLI command). Safe to call repeatedly — already-approved payouts are skipped.
"""
import logging
from datetime import datetime, timedelta

from app.extensions import db
from app.models.wallet import PayoutRequest, PAYOUT_REQUESTED, PAYOUT_APPROVED
from app.models.notification import NOTIF_PAYOUT
from app.services.notification_service import notify
from app.services.settings_service import get_setting, log_action

logger = logging.getLogger(__name__)

# Default grace period — overridden by the `auto_payout_min_hours` setting.
DEFAULT_MIN_HOURS = 24


def _min_hours():
    raw = get_setting("auto_payout_min_hours")
    try:
        return int(raw) if raw else DEFAULT_MIN_HOURS
    except (TypeError, ValueError):
        return DEFAULT_MIN_HOURS


def process_due_payouts(min_hours=None):
    """Approve every payout that has been waiting longer than `min_hours`.

    Returns the number of payouts approved.
    """
    if min_hours is None:
        min_hours = _min_hours()
    cutoff = datetime.utcnow() - timedelta(hours=int(min_hours))

    due = (
        PayoutRequest.query
        .filter(PayoutRequest.status == PAYOUT_REQUESTED,
                PayoutRequest.requested_at <= cutoff).all()
    )
    approved = 0
    now = datetime.utcnow()
    for payout in due:
        payout.status = PAYOUT_APPROVED
        payout.processed_at = now
        if payout.vendor is not None:
            notify(
                payout.vendor.user_id, NOTIF_PAYOUT,
                "Payout approved",
                f"Your payout of Tk {payout.amount} has been approved.",
                url="/seller/earnings/",
            )
        log_action("Auto-approved payout",
                   f"{payout.vendor.shop_name_en if payout.vendor else '?'}"
                   f" — Tk {payout.amount}")
        approved += 1
    if approved:
        db.session.commit()
    logger.info("Auto-payout run: %s approved (cutoff %sh).", approved, min_hours)
    return approved
