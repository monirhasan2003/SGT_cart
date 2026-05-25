"""API v1 — coupons (validate a code against the customer's cart)."""
from datetime import datetime

from flask import request, jsonify

from app.models.cart import CartItem
from app.models.marketing import Coupon, COUPON_PLATFORM
from app.services.coupon_service import validate_coupon, coupon_json
from .helpers import err, current_api_user, customer_required
from . import api_v1


@api_v1.route("/coupons", methods=["GET"])
@customer_required
def list_coupons():
    """Active, currently-running platform coupons."""
    now = datetime.utcnow()
    items = Coupon.query.filter_by(scope=COUPON_PLATFORM, is_active=True).all()
    live = [
        c for c in items
        if (c.starts_at is None or c.starts_at <= now)
        and (c.ends_at is None or c.ends_at >= now)
        and (c.usage_limit is None or c.used_count < c.usage_limit)
    ]
    return jsonify({"coupons": [coupon_json(c) for c in live]})


@api_v1.route("/coupons/validate", methods=["POST"])
@customer_required
def validate():
    """Check a coupon against the customer's current cart. Body: {code}."""
    user = current_api_user()
    code = (request.get_json(silent=True) or {}).get("code")
    items = CartItem.query.filter_by(user_id=user.id).all()
    if not items:
        return err("Your cart is empty.")

    coupon, discount, error = validate_coupon(code, user, items)
    if error:
        return jsonify({"valid": False, "error": error})
    return jsonify({
        "valid": True,
        "discount": float(discount),
        "coupon": coupon_json(coupon),
    })
