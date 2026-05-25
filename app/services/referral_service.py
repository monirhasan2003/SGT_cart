"""Referral & affiliate service — Phase 9.

One referral code per user powers two earning paths:
  * referral  — a new user signs up with the code; the referrer earns points
                when that new user places their first order.
  * affiliate — anyone buys through a product/store link carrying the code;
                the code owner earns a commission (as reward points).
"""
import secrets
import string
from decimal import Decimal

from app.extensions import db
from app.models.user import User
from app.models.order import Order
from app.models.marketing import Referral, AffiliateCommission
from app.models.notification import NOTIF_SYSTEM
from app.services import reward_service
from app.services.notification_service import notify

# Points the referrer earns when their referee places a first order.
REFERRAL_REWARD_POINTS = 50
# Affiliate commission as a fraction of order subtotal, paid in points.
AFFILIATE_COMMISSION_RATE = Decimal("0.02")

_ALPHABET = string.ascii_uppercase + string.digits


def _generate_code():
    return "".join(secrets.choice(_ALPHABET) for _ in range(8))


def ensure_code(user):
    """Return the user's referral code, generating a unique one if needed."""
    if not user.referral_code:
        code = _generate_code()
        while User.query.filter_by(referral_code=code).first() is not None:
            code = _generate_code()
        user.referral_code = code
        db.session.commit()
    return user.referral_code


def find_by_code(code):
    code = (code or "").strip().upper()
    return User.query.filter_by(referral_code=code).first() if code else None


def record_referral(referrer, referee):
    """Register a signup referral (skips self-referral / duplicates)."""
    if referrer is None or referee is None or referrer.id == referee.id:
        return None
    if Referral.query.filter_by(referee_id=referee.id).first() is not None:
        return None
    referral = Referral(referrer_id=referrer.id, referee_id=referee.id)
    db.session.add(referral)
    return referral


def reward_referral_on_first_order(user):
    """Reward the referrer when `user` places their first order. Caller commits."""
    referral = Referral.query.filter_by(referee_id=user.id, is_rewarded=False).first()
    if referral is None:
        return 0
    referrer = db.session.get(User, referral.referrer_id)
    if referrer is None:
        return 0
    referral.is_rewarded = True
    referral.reward_points = REFERRAL_REWARD_POINTS
    reward_service.grant_points(
        referrer, REFERRAL_REWARD_POINTS,
        f"Referral reward — {user.name} placed their first order",
    )
    notify(
        referrer.id, NOTIF_SYSTEM, "Referral reward earned!",
        f"You earned {REFERRAL_REWARD_POINTS} points — {user.name} just "
        "placed their first order.", url="/refer/",
    )
    return REFERRAL_REWARD_POINTS


def record_affiliate_commission(affiliate_code, order):
    """Credit an affiliate commission for a sale made via a share link.

    Caller commits.
    """
    affiliate = find_by_code(affiliate_code)
    if affiliate is None or affiliate.id == order.customer_id:
        return 0
    points = int(Decimal(order.subtotal) * AFFILIATE_COMMISSION_RATE)
    if points <= 0:
        return 0
    db.session.add(AffiliateCommission(
        affiliate_id=affiliate.id, order_id=order.id, points=points,
    ))
    reward_service.grant_points(
        affiliate, points,
        f"Affiliate commission — order {order.order_number}", order,
    )
    notify(
        affiliate.id, NOTIF_SYSTEM, "Affiliate commission earned",
        f"You earned {points} points from a sale through your share link.",
        url="/refer/",
    )
    return points


def stats(user):
    """Referral + affiliate summary for the Refer & Earn page / API."""
    referrals = Referral.query.filter_by(referrer_id=user.id).all()
    commissions = AffiliateCommission.query.filter_by(affiliate_id=user.id).all()
    return {
        "code": ensure_code(user),
        "referral_count": len(referrals),
        "referrals_rewarded": sum(1 for r in referrals if r.is_rewarded),
        "referral_points": sum(r.reward_points for r in referrals),
        "affiliate_sales": len(commissions),
        "affiliate_points": sum(c.points for c in commissions),
    }
