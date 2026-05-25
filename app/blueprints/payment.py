"""Payment callbacks — SSLCommerz redirect URLs & IPN (Phase 4).

SSLCommerz posts to /payment/success|fail|cancel after the customer pays, and
to /payment/ipn server-to-server. This blueprint is CSRF-exempt (external POST).
"""
import json

from flask import Blueprint, request, redirect, url_for, flash

from app.extensions import db
from app.models.order import Order, PAYMENT_PAID, PAYMENT_FAILED
from app.models.payment import (
    Transaction, GATEWAY_SSLCOMMERZ, TXN_SUCCESS, TXN_FAILED, TXN_CANCELLED,
)
from app.services import sslcommerz

payment = Blueprint("payment", __name__, url_prefix="/payment")


def _order_from_request():
    tran_id = request.form.get("tran_id") or request.args.get("tran_id")
    if not tran_id:
        return None
    return Order.query.filter_by(order_number=tran_id).first()


def _latest_txn(order):
    return (
        Transaction.query
        .filter_by(order_id=order.id, gateway=GATEWAY_SSLCOMMERZ)
        .order_by(Transaction.id.desc()).first()
    )


def _is_valid(result, order):
    """A validation response is trusted only if VALID and the amount matches."""
    if not result or result.get("status") not in ("VALID", "VALIDATED"):
        return False
    try:
        return abs(float(result.get("amount", 0)) - float(order.total_amount)) < 1.0
    except (TypeError, ValueError):
        return False


@payment.route("/success", methods=["POST", "GET"])
def success():
    order = _order_from_request()
    if order is None:
        flash("Payment reference not found.", "danger")
        return redirect(url_for("main.index"))

    val_id = request.form.get("val_id") or request.args.get("val_id")
    result = sslcommerz.validate_payment(val_id)
    txn = _latest_txn(order)

    if _is_valid(result, order):
        order.payment_status = PAYMENT_PAID
        if txn:
            txn.status = TXN_SUCCESS
            txn.gateway_txn_id = val_id
            txn.bank_txn_id = result.get("bank_tran_id")
            txn.card_type = result.get("card_type")
            txn.raw_response = json.dumps(result)
        db.session.commit()
        flash(f"Payment successful — order {order.order_number} is confirmed.", "success")
    else:
        if txn:
            txn.status = TXN_FAILED
            txn.raw_response = json.dumps(result) if result else None
        db.session.commit()
        flash("Payment could not be verified. Please contact support.", "danger")

    return redirect(url_for("account.order_detail", order_number=order.order_number))


@payment.route("/fail", methods=["POST", "GET"])
def fail():
    order = _order_from_request()
    if order is None:
        return redirect(url_for("main.index"))
    txn = _latest_txn(order)
    if txn:
        txn.status = TXN_FAILED
    order.payment_status = PAYMENT_FAILED
    db.session.commit()
    flash("Payment failed. Your order is saved as unpaid.", "danger")
    return redirect(url_for("account.order_detail", order_number=order.order_number))


@payment.route("/cancel", methods=["POST", "GET"])
def cancel():
    order = _order_from_request()
    if order is None:
        return redirect(url_for("main.index"))
    txn = _latest_txn(order)
    if txn:
        txn.status = TXN_CANCELLED
    db.session.commit()
    flash("Payment cancelled. Your order is saved as unpaid.", "warning")
    return redirect(url_for("account.order_detail", order_number=order.order_number))


@payment.route("/ipn", methods=["POST"])
def ipn():
    """Server-to-server payment notification from SSLCommerz (idempotent)."""
    order = _order_from_request()
    if order is None:
        return "order not found", 404
    result = sslcommerz.validate_payment(request.form.get("val_id"))
    if _is_valid(result, order) and order.payment_status != PAYMENT_PAID:
        order.payment_status = PAYMENT_PAID
        txn = _latest_txn(order)
        if txn:
            txn.status = TXN_SUCCESS
            txn.gateway_txn_id = request.form.get("val_id")
            txn.raw_response = json.dumps(result)
        db.session.commit()
    return "OK", 200
