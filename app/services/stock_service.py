"""Stock-notification service — Phase 15 D-6.

Subscribers register an email against an out-of-stock product. When the
seller raises stock from 0 → positive, every pending subscriber gets an
email + (when their user is known) an in-app notification.

A subscription with a stamped `notified_at` is left in the table for
audit. A re-subscription on the same email after the stock drops again
re-opens the same row (sets `notified_at` back to NULL) so we never spam
twice for the same incident.
"""
from datetime import datetime
from sqlalchemy import func

from app.extensions import db
from app.models.notification import NOTIF_PRODUCT
from app.models.order import OrderItem, SubOrder, SUBORDER_CANCELLED
from app.models.stock import StockNotification
from app.services.email_service import send_email
from app.services.notification_service import notify


def _norm_email(raw):
    return (raw or "").strip().lower()


def subscribe(product, user, email):
    """Register a back-in-stock subscription. Returns (row, error_str)."""
    email = _norm_email(email) or (user.email if user else None)
    if not email:
        return None, "Please provide an email address."

    if product.stock > 0:
        return None, "This product is in stock — no notification needed."

    existing = StockNotification.query.filter_by(
        product_id=product.id, email=email
    ).first()
    if existing is not None:
        if existing.notified_at is None:
            return existing, None        # idempotent re-subscribe
        existing.notified_at = None      # re-open after a previous notify
        existing.created_at = datetime.utcnow()
        existing.user_id = user.id if user else existing.user_id
        db.session.commit()
        return existing, None

    row = StockNotification(
        product_id=product.id, email=email,
        user_id=user.id if user else None,
    )
    db.session.add(row)
    db.session.commit()
    return row, None


def pending_for_product(product):
    """Subscribers waiting for a back-in-stock email."""
    return (
        StockNotification.query
        .filter_by(product_id=product.id, notified_at=None)
        .order_by(StockNotification.id).all()
    )


def pending_count_for_product(product):
    return (
        StockNotification.query
        .filter_by(product_id=product.id, notified_at=None).count()
    )


def notify_back_in_stock(product):
    """Email + in-app-notify every pending subscriber. Returns count sent."""
    pending = pending_for_product(product)
    if not pending:
        return 0
    sent = 0
    for row in pending:
        title = "Back in stock"
        body_line = f"'{product.title_en}' is available again."
        try:
            send_email(
                subject=title,
                recipients=[row.email],
                html=(
                    f"<p>Good news — <strong>{product.title_en}</strong> "
                    "is back in stock on SGT Cart.</p>"
                    f"<p><a href=\"/product/{product.slug}/\">View product</a></p>"
                ),
                text=body_line + f" /product/{product.slug}/",
            )
        except Exception:  # noqa: BLE001
            # Email outage shouldn't block the loop — leave notified_at
            # blank so a retry next time can pick it up.
            continue
        row.notified_at = datetime.utcnow()
        if row.user_id:
            notify(row.user_id, NOTIF_PRODUCT, title, body_line,
                   url=f"/product/{product.slug}/")
        sent += 1
    db.session.commit()
    return sent


def units_sold_recent(product, hours=24):
    """Total units sold of a product in the last `hours`, excluding
    cancelled sub-orders. Used for the "X sold in last 24h" urgency badge."""
    from datetime import timedelta
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    row = (
        db.session.query(func.coalesce(func.sum(OrderItem.quantity), 0))
        .join(SubOrder, OrderItem.sub_order_id == SubOrder.id)
        .filter(
            OrderItem.product_id == product.id,
            SubOrder.created_at >= cutoff,
            SubOrder.status != SUBORDER_CANCELLED,
        ).scalar()
    )
    return int(row or 0)
