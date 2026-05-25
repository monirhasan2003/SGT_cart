"""API v1 — cart & checkout (customer-only).

The cart is DB-backed (one set of CartItem rows per customer), shared with the
web cart. Checkout reuses `order_service.place_order` so the multi-vendor split
and commission logic stay identical across web and API.
"""
from decimal import Decimal

from flask import request, jsonify, url_for

from app.extensions import db
from app.models.cart import CartItem
from app.models.catalog import Product, ProductVariant, PRODUCT_PUBLISHED
from app.models.user import Address
from app.models.order import PAYMENT_COD, PAYMENT_SSLCOMMERZ
from app.models.payment import (
    Transaction, GATEWAY_COD, GATEWAY_SSLCOMMERZ, TXN_PENDING, TXN_INITIATED,
)
from app.services.order_service import (
    place_order, group_cart_by_vendor, shipping_fee_per_vendor,
)
from app.services import sslcommerz
from .helpers import err, current_api_user, customer_required
from .serializers import cart_item_json, order_json
from . import api_v1


def _cart_payload(user):
    """The full cart state — items plus computed totals."""
    items = (
        CartItem.query.filter_by(user_id=user.id)
        .order_by(CartItem.id.desc()).all()
    )
    subtotal = sum((it.line_total for it in items), Decimal("0"))
    shipping = shipping_fee_per_vendor() * len(group_cart_by_vendor(items)) if items else Decimal("0")
    return {
        "items": [cart_item_json(it) for it in items],
        "count": sum(it.quantity for it in items),
        "subtotal": float(subtotal),
        "shipping_fee": float(shipping),
        "total": float(subtotal + shipping),
    }


@api_v1.route("/cart", methods=["GET"])
@customer_required
def get_cart():
    return jsonify(_cart_payload(current_api_user()))


@api_v1.route("/cart/items", methods=["POST"])
@customer_required
def add_to_cart():
    """Add a product (optionally a variant) to the cart, or bump its quantity."""
    user = current_api_user()
    data = request.get_json(silent=True) or {}

    product = db.session.get(Product, data.get("product_id")) if data.get("product_id") else None
    if product is None or product.status != PRODUCT_PUBLISHED:
        return err("That product is not available.", 404)

    try:
        quantity = max(1, int(data.get("quantity", 1)))
    except (TypeError, ValueError):
        return err("quantity must be an integer.")

    variant = None
    if data.get("variant_id"):
        variant = db.session.get(ProductVariant, data["variant_id"])
        if variant is None or variant.product_id != product.id:
            return err("Invalid product variant.", 400)

    existing = CartItem.query.filter_by(
        user_id=user.id, product_id=product.id,
        variant_id=variant.id if variant else None,
    ).first()
    if existing:
        existing.quantity += quantity
    else:
        db.session.add(CartItem(
            user_id=user.id, product_id=product.id,
            variant_id=variant.id if variant else None, quantity=quantity,
        ))
    db.session.commit()
    return jsonify(_cart_payload(user)), 201


@api_v1.route("/cart/items/<int:item_id>", methods=["PATCH", "PUT"])
@customer_required
def update_cart_item(item_id):
    """Set a cart line's quantity; a quantity below 1 removes the line."""
    user = current_api_user()
    item = db.session.get(CartItem, item_id)
    if item is None or item.user_id != user.id:
        return err("Cart item not found.", 404)

    data = request.get_json(silent=True) or {}
    try:
        quantity = int(data.get("quantity", 1))
    except (TypeError, ValueError):
        return err("quantity must be an integer.")

    if quantity < 1:
        db.session.delete(item)
    else:
        item.quantity = quantity
    db.session.commit()
    return jsonify(_cart_payload(user))


@api_v1.route("/cart/items/<int:item_id>", methods=["DELETE"])
@customer_required
def remove_cart_item(item_id):
    user = current_api_user()
    item = db.session.get(CartItem, item_id)
    if item is None or item.user_id != user.id:
        return err("Cart item not found.", 404)
    db.session.delete(item)
    db.session.commit()
    return jsonify(_cart_payload(user))


@api_v1.route("/checkout", methods=["POST"])
@customer_required
def checkout():
    """Place an order from the cart. Body: {address_id, payment_method}.

    For SSLCommerz, the response carries a `payment.gateway_url` the app opens
    in a webview; COD orders are confirmed immediately.
    """
    user = current_api_user()
    if not CartItem.query.filter_by(user_id=user.id).first():
        return err("Your cart is empty.", 400)

    data = request.get_json(silent=True) or {}
    address = db.session.get(Address, data.get("address_id")) if data.get("address_id") else None
    if address is None or address.user_id != user.id:
        return err("Please provide a valid delivery address.", 400)

    method = data.get("payment_method") or PAYMENT_COD
    if method not in (PAYMENT_COD, PAYMENT_SSLCOMMERZ):
        return err("payment_method must be 'cod' or 'sslcommerz'.")

    try:
        points = max(0, int(data.get("points_to_redeem", 0) or 0))
    except (TypeError, ValueError):
        return err("points_to_redeem must be an integer.")

    order = place_order(user, address, method,
                        coupon_code=data.get("coupon_code"),
                        points_to_redeem=points,
                        affiliate_code=data.get("affiliate_code"))
    if order is None:
        return err("Your cart is empty.", 400)

    if method == PAYMENT_SSLCOMMERZ:
        db.session.add(Transaction(
            order_id=order.id, gateway=GATEWAY_SSLCOMMERZ,
            amount=order.total_amount, status=TXN_INITIATED,
        ))
        db.session.commit()
        if not sslcommerz.is_configured():
            return jsonify({
                "order": order_json(order, detail=True),
                "payment": {
                    "status": "unconfigured",
                    "message": "Online payment is not available yet. "
                               "The order is saved as unpaid.",
                },
            }), 201
        ok, result = sslcommerz.init_payment(
            order, user.email,
            success_url=url_for("payment.success", _external=True),
            fail_url=url_for("payment.fail", _external=True),
            cancel_url=url_for("payment.cancel", _external=True),
            ipn_url=url_for("payment.ipn", _external=True),
        )
        return jsonify({
            "order": order_json(order, detail=True),
            "payment": (
                {"status": "redirect", "gateway_url": result} if ok
                else {"status": "error", "message": result}
            ),
        }), 201

    # Cash on Delivery
    db.session.add(Transaction(
        order_id=order.id, gateway=GATEWAY_COD,
        amount=order.total_amount, status=TXN_PENDING,
    ))
    db.session.commit()
    return jsonify({
        "order": order_json(order, detail=True),
        "payment": {"status": "cod"},
    }), 201
