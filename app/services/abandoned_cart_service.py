"""Abandoned-cart recovery — Phase 9.

`scan()` finds carts left untouched for a while, records them and emails a
one-time reminder. It is safe to run repeatedly (idempotent per cart) and is
meant to be driven by a scheduler — for now the `scan-abandoned-carts` CLI
command or the admin "Run scan" button (Celery beat arrives with the
production infra).
"""
import logging
from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import func

from app.extensions import db
from app.models.user import User
from app.models.cart import CartItem
from app.models.marketing import AbandonedCart
from app.services.email_service import send_abandoned_cart_email

logger = logging.getLogger(__name__)

# A cart is "abandoned" once nothing has been added for this many hours.
IDLE_HOURS = 6


def scan(idle_hours=IDLE_HOURS):
    """Detect stale carts, record them and send a reminder once.

    Returns ``(detected, reminders_sent)``.
    """
    cutoff = datetime.utcnow() - timedelta(hours=idle_hours)
    rows = (
        db.session.query(
            CartItem.user_id,
            func.max(CartItem.created_at),
            func.count(CartItem.id),
        )
        .group_by(CartItem.user_id)
        .all()
    )

    detected, sent = 0, 0
    for user_id, last_added, count in rows:
        if last_added is None or last_added > cutoff:
            continue  # cart still fresh

        items = CartItem.query.filter_by(user_id=user_id).all()
        value = sum((it.line_total for it in items), Decimal("0.00"))

        record = AbandonedCart.query.filter_by(user_id=user_id).first()
        if record is None:
            record = AbandonedCart(user_id=user_id)
            db.session.add(record)
        record.item_count = count
        record.cart_value = value
        record.detected_at = datetime.utcnow()
        record.is_recovered = False
        detected += 1

        if record.reminder_sent_at is None:
            user = db.session.get(User, user_id)
            try:
                send_abandoned_cart_email(user, count, value)
                record.reminder_sent_at = datetime.utcnow()
                sent += 1
            except Exception as exc:  # noqa: BLE001 — SMTP failure shouldn't abort the scan
                logger.warning("Abandoned-cart email to %s failed: %s",
                               getattr(user, "email", user_id), exc)

    db.session.commit()
    return detected, sent


def mark_recovered(user):
    """Flag a customer's abandoned cart as recovered once they order again.

    Resets the reminder so a future abandonment is reminded afresh. Caller
    commits.
    """
    record = AbandonedCart.query.filter_by(user_id=user.id).first()
    if record is not None and not record.is_recovered:
        record.is_recovered = True
        record.reminder_sent_at = None
