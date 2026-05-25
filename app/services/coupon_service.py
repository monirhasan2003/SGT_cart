"""Coupon service — Phase 9.

Validates a coupon against a cart and computes the discount. Shared by the
web checkout, the REST API and order placement.
"""
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from app.extensions import db
from app.models.marketing import (
    Coupon, CouponRedemption, COUPON_VENDOR, DISCOUNT_PERCENT, DISCOUNT_TYPES,
)

_CENT = Decimal("0.01")
ZERO = Decimal("0.00")


def normalize_code(code):
    return (code or "").strip().upper()


def find_coupon(code):
    code = normalize_code(code)
    return Coupon.query.filter_by(code=code).first() if code else None


def _eligible_amount(coupon, cart_items):
    """Cart total the coupon applies to (vendor coupons: that store only)."""
    total = ZERO
    for item in cart_items:
        if (coupon.scope == COUPON_VENDOR
                and (item.product is None
                     or item.product.vendor_id != coupon.vendor_id)):
            continue
        total += Decimal(item.line_total)
    return total


def validate_coupon(code, user, cart_items):
    """Check a coupon for this user + cart.

    Returns ``(coupon, discount, error)``: on success ``error`` is None and
    ``discount`` is a positive Decimal; on failure ``coupon`` is None.
    """
    coupon = find_coupon(code)
    if coupon is None or not coupon.is_active:
        return None, ZERO, "Invalid coupon code."

    now = datetime.utcnow()
    if coupon.starts_at and now < coupon.starts_at:
        return None, ZERO, "This coupon is not active yet."
    if coupon.ends_at and now > coupon.ends_at:
        return None, ZERO, "This coupon has expired."
    if coupon.usage_limit is not None and coupon.used_count >= coupon.usage_limit:
        return None, ZERO, "This coupon has reached its usage limit."

    if coupon.per_user_limit and user is not None:
        used = CouponRedemption.query.filter_by(
            coupon_id=coupon.id, user_id=user.id
        ).count()
        if used >= coupon.per_user_limit:
            return None, ZERO, "You have already used this coupon."

    eligible = _eligible_amount(coupon, cart_items)
    if eligible <= ZERO:
        return None, ZERO, ("This coupon applies only to a specific store's "
                            "items, which are not in your cart.")
    if eligible < Decimal(coupon.min_order_amount or 0):
        return None, ZERO, (f"A minimum order of Tk {coupon.min_order_amount} "
                            "is required for this coupon.")

    if coupon.discount_type == DISCOUNT_PERCENT:
        discount = eligible * Decimal(coupon.discount_value) / Decimal("100")
        if coupon.max_discount:
            discount = min(discount, Decimal(coupon.max_discount))
    else:
        discount = Decimal(coupon.discount_value)
    # Never discount more than the eligible amount.
    discount = min(discount, eligible).quantize(_CENT, rounding=ROUND_HALF_UP)

    if discount <= ZERO:
        return None, ZERO, "This coupon gives no discount on your cart."
    return coupon, discount, None


def redeem_coupon(coupon, user, order, amount):
    """Record a coupon use against an order (caller commits)."""
    coupon.used_count = (coupon.used_count or 0) + 1
    db.session.add(CouponRedemption(
        coupon_id=coupon.id, user_id=user.id,
        order_id=order.id, amount=amount,
    ))


def parse_coupon_form(form, existing=None):
    """Parse + validate the coupon create/edit form.

    Returns ``(data, errors)`` — `data` is a dict of column values (scope and
    vendor_id are set by the caller).
    """
    errors = []
    code = normalize_code(form.get("code"))
    if not code:
        errors.append("Coupon code is required.")
    else:
        clash = Coupon.query.filter(
            Coupon.code == code,
            Coupon.id != (existing.id if existing else 0),
        ).first()
        if clash is not None:
            errors.append("That coupon code is already in use.")

    discount_type = form.get("discount_type")
    if discount_type not in DISCOUNT_TYPES:
        errors.append("Choose a valid discount type.")

    def _decimal(name, default="0"):
        raw = (form.get(name) or "").strip() or default
        try:
            return Decimal(raw)
        except Exception:  # noqa: BLE001
            return None

    discount_value = _decimal("discount_value")
    if discount_value is None or discount_value <= ZERO:
        errors.append("Discount value must be a positive number.")
    elif discount_type == DISCOUNT_PERCENT and discount_value > Decimal("100"):
        errors.append("A percentage discount cannot exceed 100.")

    min_order_amount = _decimal("min_order_amount") or ZERO
    max_discount = _decimal("max_discount") if (form.get("max_discount") or "").strip() else None

    def _int(name):
        raw = (form.get(name) or "").strip()
        return int(raw) if raw.isdigit() else None

    def _date(name):
        raw = (form.get(name) or "").strip()
        if not raw:
            return None
        try:
            return datetime.strptime(raw, "%Y-%m-%d")
        except ValueError:
            errors.append(f"'{name.replace('_', ' ')}' must be a valid date.")
            return None

    data = {
        "code": code,
        "description": (form.get("description") or "").strip() or None,
        "discount_type": discount_type,
        "discount_value": discount_value if discount_value is not None else ZERO,
        "min_order_amount": min_order_amount,
        "max_discount": max_discount,
        "usage_limit": _int("usage_limit"),
        "per_user_limit": _int("per_user_limit") or 1,
        "starts_at": _date("starts_at"),
        "ends_at": _date("ends_at"),
        "is_active": bool(form.get("is_active")),
    }
    return data, errors


def coupon_form_dict(coupon):
    """Pre-fill values for the coupon edit form."""
    return {
        "code": coupon.code,
        "description": coupon.description or "",
        "discount_type": coupon.discount_type,
        "discount_value": coupon.discount_value,
        "min_order_amount": coupon.min_order_amount,
        "max_discount": coupon.max_discount if coupon.max_discount is not None else "",
        "usage_limit": coupon.usage_limit if coupon.usage_limit is not None else "",
        "per_user_limit": coupon.per_user_limit,
        "starts_at": coupon.starts_at.strftime("%Y-%m-%d") if coupon.starts_at else "",
        "ends_at": coupon.ends_at.strftime("%Y-%m-%d") if coupon.ends_at else "",
        "is_active": coupon.is_active,
    }


def coupon_json(coupon):
    """Serialize a coupon for the REST API."""
    return {
        "code": coupon.code,
        "description": coupon.description,
        "scope": coupon.scope,
        "discount_type": coupon.discount_type,
        "discount_value": float(coupon.discount_value),
        "min_order_amount": float(coupon.min_order_amount or 0),
        "max_discount": float(coupon.max_discount) if coupon.max_discount else None,
    }
