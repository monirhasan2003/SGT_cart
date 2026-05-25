"""Order placement — multi-vendor split & commission (Phase 3).

When a customer checks out, their cart is split by vendor: one Order with one
SubOrder per vendor. Platform commission is computed per SubOrder using the
vendor's commission rate (snapshotted onto the SubOrder).
"""
import random
from datetime import datetime
from decimal import Decimal

from app.extensions import db
from app.models.cart import CartItem
from app.models.order import (
    Order, SubOrder, OrderItem, SubOrderEvent,
    PAYMENT_PENDING, SUBORDER_PENDING, SUBORDER_DELIVERED,
)
from app.models.notification import NOTIF_ORDER, NOTIF_PRODUCT
from app.services.wallet_service import (
    credit_pending, settle_delivered, unsettle_delivered,
)
from app.services.settings_service import get_decimal
from app.services.notification_service import notify
from app.services.coupon_service import validate_coupon, redeem_coupon
from app.services import reward_service, referral_service, abandoned_cart_service
from app.services.analytics_service import LOW_STOCK_THRESHOLD
from app.services.vendor_stats_service import recompute_vendor_stats
from app.sockets import emit_to_user

_ORDER_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def shipping_fee_per_vendor():
    """Per-vendor shipping fee, from admin platform settings."""
    return get_decimal("shipping_fee_per_vendor")


def _unique_order_number():
    prefix = "SGT" + datetime.utcnow().strftime("%y%m%d")
    while True:
        number = prefix + "-" + "".join(random.choices(_ORDER_CHARS, k=5))
        if Order.query.filter_by(order_number=number).first() is None:
            return number


def group_cart_by_vendor(items):
    """Group cart items by their product's vendor → {VendorProfile: [items]}."""
    groups = {}
    for item in items:
        groups.setdefault(item.product.vendor, []).append(item)
    return groups


def place_order(user, address, payment_method, coupon_code=None,
                points_to_redeem=0, affiliate_code=None):
    """Create an Order + per-vendor SubOrders from the user's cart.

    Computes commission per SubOrder, applies a coupon discount and/or
    redeemed reward points, settles referral / affiliate rewards, clears the
    cart, and returns the Order (or None when the cart is empty).
    """
    items = CartItem.query.filter_by(user_id=user.id).all()
    if not items:
        return None

    groups = group_cart_by_vendor(items)

    order = Order(
        customer_id=user.id,
        order_number=_unique_order_number(),
        payment_method=payment_method,
        payment_status=PAYMENT_PENDING,
        ship_name=address.full_name,
        ship_phone=address.phone,
        ship_address_line=address.address_line,
        ship_area=address.area,
        ship_city=address.city,
        ship_district=address.district,
        ship_postal_code=address.postal_code,
    )
    db.session.add(order)
    db.session.flush()

    grand_subtotal = Decimal("0.00")
    for vendor, vendor_items in groups.items():
        sub_total = Decimal("0.00")
        for item in vendor_items:
            sub_total += Decimal(item.unit_price) * item.quantity

        rate = Decimal(vendor.commission_rate or 0)
        commission = (sub_total * rate / Decimal("100")).quantize(Decimal("0.01"))

        sub = SubOrder(
            order_id=order.id, vendor_id=vendor.id,
            subtotal=sub_total, commission_rate=rate,
            commission_amount=commission, vendor_earning=sub_total - commission,
            status=SUBORDER_PENDING,
        )
        db.session.add(sub)
        db.session.flush()

        # Start the tracking timeline + alert the vendor of the new order.
        db.session.add(SubOrderEvent(
            sub_order_id=sub.id, status=SUBORDER_PENDING, note="Order placed",
        ))
        notify(
            vendor.user_id, NOTIF_ORDER,
            "New order received",
            f"Order {order.order_number} — {len(vendor_items)} item(s) to fulfil.",
            url=f"/seller/orders/{sub.id}/",
        )

        # Vendor earning enters their wallet's pending balance.
        credit_pending(vendor.id, sub.vendor_earning)

        for item in vendor_items:
            unit = Decimal(item.unit_price)
            label = None
            if item.variant is not None:
                label = " / ".join(p for p in (item.variant.size, item.variant.color) if p)
            db.session.add(OrderItem(
                sub_order_id=sub.id, product_id=item.product_id, variant_id=item.variant_id,
                title=item.product.title_en, variant_label=label or None,
                unit_price=unit, quantity=item.quantity, line_total=unit * item.quantity,
            ))

            # Decrement stock and alert the seller when it falls below the
            # low-stock threshold (Phase 11). Variant stock wins when set.
            stock_target = item.variant if item.variant is not None else item.product
            before = stock_target.stock or 0
            stock_target.stock = max(0, before - item.quantity)
            after = stock_target.stock
            if before > LOW_STOCK_THRESHOLD >= after:
                notify(
                    vendor.user_id, NOTIF_PRODUCT,
                    f"Low stock: {item.product.title_en}",
                    f"Only {after} left in stock — restock soon.",
                    url=f"/seller/products/{item.product_id}/edit",
                )
        grand_subtotal += sub_total

    order.subtotal = grand_subtotal
    order.shipping_fee = shipping_fee_per_vendor() * len(groups)

    # Apply a coupon discount when one is supplied and still valid.
    discount = Decimal("0.00")
    coupon = None
    if coupon_code:
        coupon, discount, error = validate_coupon(coupon_code, user, items)
        if error:
            coupon, discount = None, Decimal("0.00")
    order.discount_amount = discount
    order.coupon_code = coupon.code if coupon else None
    if coupon is not None and discount > 0:
        redeem_coupon(coupon, user, order, discount)

    # Redeem reward points — capped to the balance and the remaining payable.
    points_used = 0
    points_discount = Decimal("0.00")
    if points_to_redeem:
        payable = order.subtotal + order.shipping_fee - discount
        cap = min(int(points_to_redeem), reward_service.balance(user),
                  int(payable / reward_service.POINT_VALUE))
        if cap > 0:
            points_used = reward_service.redeem(user, cap, order)
            points_discount = reward_service.points_value(points_used)
    order.points_redeemed = points_used
    order.points_discount = points_discount

    order.total_amount = (order.subtotal + order.shipping_fee
                          - discount - points_discount)

    notify(
        user.id, NOTIF_ORDER,
        f"Order {order.order_number} placed",
        f"Your order across {len(groups)} seller(s) has been placed.",
        url=f"/my-orders/{order.order_number}/",
    )

    # Referral reward (referee's first order), affiliate commission, and
    # abandoned-cart recovery.
    if Order.query.filter_by(customer_id=user.id).count() == 1:
        referral_service.reward_referral_on_first_order(user)
    if affiliate_code:
        referral_service.record_affiliate_commission(affiliate_code, order)
    abandoned_cart_service.mark_recovered(user)

    for item in items:
        db.session.delete(item)
    db.session.commit()
    return order


def update_suborder_status(sub, new_status, note=None):
    """Change a sub-order's fulfilment status — the single code path for it.

    Records the tracking event, settles/unsettles the vendor wallet on
    delivery, and notifies the customer with a live tracking update. The
    caller commits.
    """
    old_status = sub.status
    if new_status == old_status:
        return False

    sub.status = new_status
    db.session.add(SubOrderEvent(
        sub_order_id=sub.id, status=new_status, note=note,
    ))

    # Delivery settles the vendor's earning (reverses if undone) and credits
    # the customer's reward points.
    if new_status == SUBORDER_DELIVERED and old_status != SUBORDER_DELIVERED:
        settle_delivered(sub.vendor_id, sub.vendor_earning)
        reward_service.earn_for_suborder(sub)
    elif old_status == SUBORDER_DELIVERED and new_status != SUBORDER_DELIVERED:
        unsettle_delivered(sub.vendor_id, sub.vendor_earning)

    # Refresh the vendor's delivery / cancel signals after any status change
    # — keeps the ranking score current.
    if sub.vendor is not None:
        recompute_vendor_stats(sub.vendor)

    order = sub.order
    shop = sub.vendor.shop_name_en if sub.vendor else "A seller"
    notify(
        order.customer_id, NOTIF_ORDER,
        f"Order {order.order_number}: {new_status}",
        f"{shop} marked your items as {new_status}.",
        url=f"/my-orders/{order.order_number}/",
    )
    # Live order tracking — the customer's open order page updates instantly.
    emit_to_user(order.customer_id, "order_update", {
        "order_number": order.order_number,
        "sub_order_id": sub.id,
        "vendor": shop,
        "status": new_status,
    })
    return True
