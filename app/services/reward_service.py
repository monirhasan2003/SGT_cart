"""Reward-points (loyalty) service — Phase 9.

Customers earn points when a sub-order is delivered and may redeem them for a
discount at checkout. `User.reward_points` holds the running balance;
`RewardLedger` is the audit trail.
"""
from decimal import Decimal

from app.extensions import db
from app.models.marketing import RewardLedger
from app.models.notification import NOTIF_SYSTEM
from app.services.notification_service import notify

# 1 point earned per 100 Taka of delivered value; 1 point is worth 1 Taka.
TAKA_PER_POINT = Decimal("100")
POINT_VALUE = Decimal("1.00")


def balance(user):
    return user.reward_points or 0


def points_value(points):
    """Taka value of a number of points."""
    return (Decimal(points) * POINT_VALUE).quantize(Decimal("0.01"))


def _record(user, points, reason, order=None):
    """Move the balance and append a ledger row (caller commits)."""
    user.reward_points = (user.reward_points or 0) + points
    db.session.add(RewardLedger(
        user_id=user.id, points=points, reason=reason,
        order_id=order.id if order else None,
    ))


def earn_for_suborder(sub):
    """Credit reward points for a delivered sub-order. Returns points earned.

    Guards against double-credit if a sub-order is re-delivered.
    """
    order = sub.order
    if order is None:
        return 0
    reason = f"Order {order.order_number} delivered (#{sub.id})"
    already = RewardLedger.query.filter_by(
        user_id=order.customer_id, order_id=order.id, reason=reason
    ).first()
    if already is not None:
        return 0

    points = int(Decimal(sub.subtotal) / TAKA_PER_POINT)
    if points <= 0:
        return 0
    _record(order.customer, points, reason, order)
    notify(
        order.customer_id, NOTIF_SYSTEM,
        f"You earned {points} reward point(s)",
        f"From order {order.order_number} — redeem points at checkout.",
        url="/rewards/",
    )
    return points


def grant_points(user, points, reason, order=None):
    """Credit points outside the order-delivery flow (referrals, affiliate,
    admin adjustments). Caller commits."""
    if points <= 0:
        return 0
    _record(user, points, reason, order)
    return points


def redeem(user, points, order):
    """Spend points against an order. Returns the points actually used."""
    points = min(int(points), balance(user))
    if points <= 0:
        return 0
    _record(user, -points, f"Redeemed on order {order.order_number}", order)
    return points
