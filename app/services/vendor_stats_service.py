"""Vendor performance signals — Phase 15 Chunk B v3b.

Two computed signals influence search ranking on top of the seller rating:

  * `avg_delivery_days` — mean time from sub-order placement to the first
    "delivered" status change. Lower is better.
  * `cancel_rate` — fraction of this vendor's sub-orders cancelled. Higher
    is worse.

`apply_ranking` (see `search_service.py`) uses both. Stats are refreshed in
real time by `order_service.update_suborder_status` on each delivery /
cancellation, and in bulk by the `recompute-vendor-stats` CLI command (or a
nightly cron — see `deploy/sgt-cron.example`).
"""
from datetime import datetime, timedelta

from sqlalchemy import func

from app.extensions import db
from app.models.vendor import VendorProfile
from app.models.order import SubOrder, SUBORDER_DELIVERED, SUBORDER_CANCELLED
from app.models.catalog import Product
from app.models.review import Review
from app.models.chat import ChatThread, ChatMessage, CHAT_VENDOR


def recompute_vendor_stats(vendor):
    """Refresh avg_delivery_days + cancel_rate for one vendor (no commit)."""
    if vendor is None:
        return

    # Average delivery time across all delivered sub-orders.
    deltas = []
    delivered = SubOrder.query.filter_by(
        vendor_id=vendor.id, status=SUBORDER_DELIVERED
    ).all()
    for sub in delivered:
        if not sub.created_at:
            continue
        # The first "delivered" event tells us when the seller marked it shipped/done.
        delivered_event = next(
            (e for e in sorted(sub.events, key=lambda e: e.id)
             if e.status == SUBORDER_DELIVERED),
            None,
        )
        if delivered_event is None:
            continue
        delta_days = (delivered_event.created_at - sub.created_at).total_seconds() / 86400.0
        if delta_days >= 0:
            deltas.append(delta_days)
    vendor.avg_delivery_days = round(sum(deltas) / len(deltas), 2) if deltas else 0

    # Cancellation rate across all sub-orders.
    total = SubOrder.query.filter_by(vendor_id=vendor.id).count()
    cancelled = SubOrder.query.filter_by(
        vendor_id=vendor.id, status=SUBORDER_CANCELLED
    ).count()
    vendor.cancel_rate = round(cancelled / total, 4) if total > 0 else 0


def recompute_all():
    """Refresh stats for every vendor. Returns the number updated."""
    n = 0
    for vendor in VendorProfile.query.all():
        recompute_vendor_stats(vendor)
        n += 1
    db.session.commit()
    return n


# --------------------------------------------------------------------------
# trust_stats — Phase 15 D-4 "Why buy from this seller?" card.
# --------------------------------------------------------------------------
# Limit chat-reply scan to the recent window so the product page stays fast
# (the median reply latency drifts very little once a seller has a baseline).
_REPLY_LOOKBACK_DAYS = 60
_REPLY_THREAD_LIMIT = 50


def _positive_review_rate(vendor):
    """Share of this vendor's reviews rated 4★ or above (0..100)."""
    total = (
        db.session.query(func.count(Review.id))
        .join(Product, Review.product_id == Product.id)
        .filter(Product.vendor_id == vendor.id).scalar() or 0
    )
    if total == 0:
        return None, 0
    positives = (
        db.session.query(func.count(Review.id))
        .join(Product, Review.product_id == Product.id)
        .filter(Product.vendor_id == vendor.id, Review.rating >= 4).scalar() or 0
    )
    return round(positives * 100.0 / total, 1), total


def _median(values):
    if not values:
        return None
    s = sorted(values)
    n = len(s)
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2.0


def _avg_reply_minutes(vendor):
    """Median minutes between a customer message and the seller's reply.

    Scans the most-recent vendor chat threads in the last `_REPLY_LOOKBACK_DAYS`
    days, capped at `_REPLY_THREAD_LIMIT`. For each thread we pair customer
    messages with the next message from the seller and record that delta.
    Returns None when there's not enough signal yet.
    """
    cutoff = datetime.utcnow() - timedelta(days=_REPLY_LOOKBACK_DAYS)
    threads = (
        ChatThread.query.filter_by(kind=CHAT_VENDOR, vendor_id=vendor.id)
        .filter(ChatThread.last_message_at >= cutoff)
        .order_by(ChatThread.last_message_at.desc())
        .limit(_REPLY_THREAD_LIMIT).all()
    )
    seller_user_id = vendor.user_id
    deltas = []
    for thread in threads:
        # ChatMessage rows are ordered by id (chronological) by the model.
        pending_customer_ts = None
        for m in thread.messages:
            if m.sender_id == seller_user_id:
                if pending_customer_ts is not None and m.created_at:
                    deltas.append(
                        (m.created_at - pending_customer_ts).total_seconds() / 60.0
                    )
                    pending_customer_ts = None
            else:
                if pending_customer_ts is None and m.created_at:
                    pending_customer_ts = m.created_at
    return _median(deltas)


def trust_stats(vendor):
    """Return the dict used by the "Why buy from this seller?" card.

    Keys (any of which may be None when the seller has no signal yet):
      * positive_rate   — % of reviews >= 4★
      * review_count    — total reviews
      * avg_delivery_days
      * cancel_rate_pct — already-stored cancel_rate as a percentage
      * avg_reply_minutes
      * is_verified_seller, has_trade_license_verified, has_nid_verified
    """
    if vendor is None:
        return {}
    positive_rate, review_count = _positive_review_rate(vendor)
    return {
        "positive_rate": positive_rate,
        "review_count": review_count,
        "avg_delivery_days": float(vendor.avg_delivery_days or 0) or None,
        "cancel_rate_pct": round(float(vendor.cancel_rate or 0) * 100, 1) or None,
        "avg_reply_minutes": _avg_reply_minutes(vendor),
        "is_verified_seller": vendor.is_verified_seller,
        "has_trade_license_verified": vendor.has_trade_license_verified,
        "has_nid_verified": vendor.has_nid_verified,
    }
