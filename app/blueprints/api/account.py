"""API v1 — customer account: profile, addresses, order history."""
from flask import request, jsonify

from app.extensions import db
from app.models.user import Address
from app.models.order import Order
from app.models.marketing import RewardLedger
from app.services import referral_service
from app.services.recommendation_service import for_you
from .helpers import err, current_api_user, customer_required
from .serializers import address_json, order_json, product_card_json
from . import api_v1


# --------------------------------------------------------------------------
# profile
# --------------------------------------------------------------------------
@api_v1.route("/account/profile", methods=["PATCH"])
@customer_required
def update_profile():
    """Update name / phone / preferred locale."""
    user = current_api_user()
    data = request.get_json(silent=True) or {}
    if "name" in data:
        name = (data.get("name") or "").strip()
        if not name:
            return err("name cannot be empty.")
        user.name = name
    if "phone" in data:
        user.phone = (data.get("phone") or "").strip()
    if "locale" in data:
        if data.get("locale") not in ("en", "bn"):
            return err("locale must be 'en' or 'bn'.")
        user.locale = data["locale"]
    db.session.commit()
    return jsonify({"message": "Profile updated."})


# --------------------------------------------------------------------------
# addresses
# --------------------------------------------------------------------------
def _read_address(data):
    """Validate an address payload → (fields, errors)."""
    fields = {
        "label": (data.get("label") or "").strip(),
        "full_name": (data.get("full_name") or "").strip(),
        "phone": (data.get("phone") or "").strip(),
        "address_line": (data.get("address_line") or "").strip(),
        "area": (data.get("area") or "").strip(),
        "city": (data.get("city") or "").strip(),
        "district": (data.get("district") or "").strip(),
        "postal_code": (data.get("postal_code") or "").strip(),
    }
    errors = []
    if not fields["full_name"]:
        errors.append("full_name is required.")
    if not fields["phone"]:
        errors.append("phone is required.")
    if not fields["address_line"]:
        errors.append("address_line is required.")
    if not fields["city"]:
        errors.append("city is required.")
    return fields, errors


@api_v1.route("/addresses", methods=["GET"])
@customer_required
def list_addresses():
    user = current_api_user()
    items = (
        Address.query.filter_by(user_id=user.id)
        .order_by(Address.is_default.desc(), Address.id.desc()).all()
    )
    return jsonify({"addresses": [address_json(a) for a in items]})


@api_v1.route("/addresses", methods=["POST"])
@customer_required
def create_address():
    user = current_api_user()
    fields, errors = _read_address(request.get_json(silent=True) or {})
    if errors:
        return err(" ".join(errors))

    # The first saved address always becomes the default.
    existing_count = Address.query.filter_by(user_id=user.id).count()
    address = Address(user_id=user.id, **fields)
    db.session.add(address)
    if (request.get_json(silent=True) or {}).get("is_default") or existing_count == 0:
        Address.query.filter_by(user_id=user.id).update({"is_default": False})
        address.is_default = True
    db.session.commit()
    return jsonify({"address": address_json(address)}), 201


@api_v1.route("/addresses/<int:address_id>", methods=["PATCH", "PUT"])
@customer_required
def update_address(address_id):
    user = current_api_user()
    address = db.session.get(Address, address_id)
    if address is None or address.user_id != user.id:
        return err("Address not found.", 404)

    data = request.get_json(silent=True) or {}
    fields, errors = _read_address(data)
    if errors:
        return err(" ".join(errors))
    for key, value in fields.items():
        setattr(address, key, value)
    if data.get("is_default"):
        Address.query.filter_by(user_id=user.id).update({"is_default": False})
        address.is_default = True
    db.session.commit()
    return jsonify({"address": address_json(address)})


@api_v1.route("/addresses/<int:address_id>", methods=["DELETE"])
@customer_required
def delete_address(address_id):
    user = current_api_user()
    address = db.session.get(Address, address_id)
    if address is None or address.user_id != user.id:
        return err("Address not found.", 404)
    db.session.delete(address)
    db.session.commit()
    return jsonify({"message": "Address deleted."})


@api_v1.route("/addresses/<int:address_id>/default", methods=["POST"])
@customer_required
def set_default_address(address_id):
    user = current_api_user()
    address = db.session.get(Address, address_id)
    if address is None or address.user_id != user.id:
        return err("Address not found.", 404)
    Address.query.filter_by(user_id=user.id).update({"is_default": False})
    address.is_default = True
    db.session.commit()
    return jsonify({"address": address_json(address)})


# --------------------------------------------------------------------------
# orders
# --------------------------------------------------------------------------
@api_v1.route("/orders", methods=["GET"])
@customer_required
def list_orders():
    user = current_api_user()
    items = (
        Order.query.filter_by(customer_id=user.id)
        .order_by(Order.id.desc()).all()
    )
    return jsonify({"orders": [order_json(o) for o in items]})


@api_v1.route("/rewards", methods=["GET"])
@customer_required
def rewards():
    """Reward-points balance and recent history."""
    user = current_api_user()
    ledger = (
        RewardLedger.query.filter_by(user_id=user.id)
        .order_by(RewardLedger.id.desc()).limit(100).all()
    )
    return jsonify({
        "balance": user.reward_points or 0,
        "history": [
            {
                "points": e.points, "reason": e.reason,
                "at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in ledger
        ],
    })


@api_v1.route("/referral", methods=["GET"])
@customer_required
def referral():
    """The user's referral code, share stats and affiliate earnings."""
    return jsonify(referral_service.stats(current_api_user()))


@api_v1.route("/recommendations", methods=["GET"])
@customer_required
def recommendations():
    """Personalised product recommendations for the customer."""
    products = for_you(current_api_user(), limit=12)
    return jsonify({"products": [product_card_json(p) for p in products]})


@api_v1.route("/orders/<order_number>", methods=["GET"])
@customer_required
def order_detail(order_number):
    user = current_api_user()
    order = Order.query.filter_by(
        order_number=order_number, customer_id=user.id
    ).first()
    if order is None:
        return err("Order not found.", 404)
    return jsonify({"order": order_json(order, detail=True)})
