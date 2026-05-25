"""Shopping cart — Phase 3 (DB-backed, per logged-in customer)."""
from decimal import Decimal

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session,
)
from flask_login import login_required, current_user

from app.extensions import db, limiter
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
from app.services.coupon_service import validate_coupon
from app.services import sslcommerz

cart = Blueprint("cart", __name__)

# Session key holding the coupon code the customer applied at checkout.
COUPON_SESSION = "checkout_coupon"


def _items():
    """Current user's cart items (newest first)."""
    if not current_user.is_authenticated:
        return []
    return (
        CartItem.query.filter_by(user_id=current_user.id)
        .order_by(CartItem.id.desc()).all()
    )


def _subtotal(items):
    return sum((it.line_total for it in items), Decimal("0"))


@cart.app_context_processor
def inject_cart():
    """Expose the cart to every template (navbar badge, offcanvas)."""
    from flask import has_request_context
    if not has_request_context():
        # Background template rendering (e.g. emails) has no cart.
        return {"cart": [], "cart_count": 0,
                "cart_subtotal": Decimal("0"), "wishlist": []}
    items = _items()
    return {
        "cart": items,
        "cart_count": sum(it.quantity for it in items),
        "cart_subtotal": _subtotal(items),
        "wishlist": [],  # DB wishlist arrives in a later phase
    }


@cart.route("/cart/")
@login_required
def view():
    items = _items()
    return render_template("pages/shoping-cart.html",
                           items=items, subtotal=_subtotal(items))


@cart.route("/cart/checkout/", methods=["GET", "POST"])
@login_required
def checkout():
    items = _items()
    if not items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart.view"))

    addresses = (
        Address.query.filter_by(user_id=current_user.id)
        .order_by(Address.is_default.desc(), Address.id.desc()).all()
    )

    if request.method == "POST":
        if not addresses:
            flash("Please add a delivery address first.", "danger")
            return redirect(url_for("account.address_create"))
        address = next(
            (a for a in addresses if a.id == request.form.get("address_id", type=int)),
            None,
        )
        if address is None:
            flash("Please select a delivery address.", "danger")
            return redirect(url_for("cart.checkout"))

        method = request.form.get("payment_method", PAYMENT_COD)
        if method not in (PAYMENT_COD, PAYMENT_SSLCOMMERZ):
            method = PAYMENT_COD

        # "Use my points" redeems the whole balance (place_order caps it).
        points = current_user.reward_points if request.form.get("use_points") else 0
        order = place_order(current_user, address, method,
                            coupon_code=session.get(COUPON_SESSION),
                            points_to_redeem=points,
                            affiliate_code=session.get("affiliate_ref"))
        if order is None:
            flash("Your cart is empty.", "warning")
            return redirect(url_for("cart.view"))
        session.pop(COUPON_SESSION, None)   # coupon consumed by this order
        session.pop("affiliate_ref", None)  # affiliate credited (if any)

        if method == PAYMENT_SSLCOMMERZ:
            db.session.add(Transaction(
                order_id=order.id, gateway=GATEWAY_SSLCOMMERZ,
                amount=order.total_amount, status=TXN_INITIATED,
            ))
            db.session.commit()
            if not sslcommerz.is_configured():
                flash("Online payment is not available yet — your order is saved as "
                      "unpaid. You can pay later or contact support.", "warning")
                return redirect(url_for("account.order_detail", order_number=order.order_number))
            ok, result = sslcommerz.init_payment(
                order, current_user.email,
                success_url=url_for("payment.success", _external=True),
                fail_url=url_for("payment.fail", _external=True),
                cancel_url=url_for("payment.cancel", _external=True),
                ipn_url=url_for("payment.ipn", _external=True),
            )
            if ok:
                return redirect(result)
            flash(f"Could not start online payment: {result} "
                  f"Order {order.order_number} is saved as unpaid.", "warning")
            return redirect(url_for("account.order_detail", order_number=order.order_number))

        # Cash on Delivery
        db.session.add(Transaction(
            order_id=order.id, gateway=GATEWAY_COD,
            amount=order.total_amount, status=TXN_PENDING,
        ))
        db.session.commit()
        flash(f"Order {order.order_number} placed successfully!", "success")
        return redirect(url_for("account.order_detail", order_number=order.order_number))

    groups = group_cart_by_vendor(items)
    subtotal = _subtotal(items)
    shipping = shipping_fee_per_vendor() * len(groups)

    # A coupon held in the session — re-validated against the current cart.
    coupon_code = session.get(COUPON_SESSION)
    discount = Decimal("0")
    if coupon_code:
        _, discount, error = validate_coupon(coupon_code, current_user, items)
        if error:
            session.pop(COUPON_SESSION, None)
            coupon_code, discount = None, Decimal("0")

    return render_template(
        "pages/checkout.html", groups=groups, addresses=addresses,
        subtotal=subtotal, shipping=shipping, discount=discount,
        coupon_code=coupon_code, total=subtotal + shipping - discount,
    )


@cart.route("/cart/checkout/apply-coupon", methods=["POST"])
@login_required
@limiter.limit("10 per minute")
def apply_coupon():
    """Validate a coupon against the cart and remember it for checkout."""
    code = (request.form.get("coupon_code") or "").strip()
    coupon, discount, error = validate_coupon(code, current_user, _items())
    if error:
        session.pop(COUPON_SESSION, None)
        flash(error, "danger")
    else:
        session[COUPON_SESSION] = coupon.code
        flash(f"Coupon '{coupon.code}' applied — you save ৳{discount}.", "success")
    return redirect(url_for("cart.checkout"))


@cart.route("/cart/checkout/remove-coupon", methods=["POST"])
@login_required
def remove_coupon():
    session.pop(COUPON_SESSION, None)
    flash("Coupon removed.", "info")
    return redirect(url_for("cart.checkout"))


@cart.route("/cart/add", methods=["POST"])
@login_required
def add():
    product_id = request.form.get("product_id", type=int)
    variant_id = request.form.get("variant_id", type=int)
    quantity = request.form.get("quantity", default=1, type=int) or 1
    quantity = max(1, quantity)
    # Phase 15 D-1: "Buy Now" skips the cart view and jumps to checkout.
    buy_now = bool(request.form.get("buy_now"))

    product = db.session.get(Product, product_id) if product_id else None
    if product is None or product.status != PRODUCT_PUBLISHED:
        flash("That product is not available.", "danger")
        return redirect(request.referrer or url_for("storefront.shop"))

    variant = None
    if variant_id:
        variant = db.session.get(ProductVariant, variant_id)
        if variant is None or variant.product_id != product.id:
            variant = None

    existing = CartItem.query.filter_by(
        user_id=current_user.id, product_id=product.id,
        variant_id=variant.id if variant else None,
    ).first()
    if existing:
        existing.quantity += quantity
    else:
        db.session.add(CartItem(
            user_id=current_user.id, product_id=product.id,
            variant_id=variant.id if variant else None, quantity=quantity,
        ))
    db.session.commit()
    if buy_now:
        return redirect(url_for("cart.checkout"))
    flash(f"{product.localized_title} added to your cart.", "success")
    return redirect(url_for("cart.view"))


@cart.route("/cart/update", methods=["POST"])
@login_required
def update():
    item = db.session.get(CartItem, request.form.get("item_id", type=int))
    if item is not None and item.user_id == current_user.id:
        quantity = request.form.get("quantity", default=1, type=int) or 1
        if quantity < 1:
            db.session.delete(item)
        else:
            item.quantity = quantity
        db.session.commit()
    return redirect(url_for("cart.view"))


@cart.route("/cart/remove", methods=["POST"])
@login_required
def remove():
    item = db.session.get(CartItem, request.form.get("item_id", type=int))
    if item is not None and item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
        flash("Item removed from your cart.", "info")
    return redirect(url_for("cart.view"))
