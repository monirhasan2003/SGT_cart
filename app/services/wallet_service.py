"""Vendor wallet operations — Phase 5.

Callers are responsible for committing the session.
"""
from decimal import Decimal

from app.extensions import db
from app.models.wallet import VendorWallet


def _d(value):
    return Decimal(str(value or 0))


def get_or_create_wallet(vendor_id):
    wallet = VendorWallet.query.filter_by(vendor_id=vendor_id).first()
    if wallet is None:
        wallet = VendorWallet(vendor_id=vendor_id)
        db.session.add(wallet)
        db.session.flush()
    return wallet


def credit_pending(vendor_id, amount):
    """Order placed — vendor earning enters the pending balance."""
    wallet = get_or_create_wallet(vendor_id)
    wallet.pending_balance = _d(wallet.pending_balance) + _d(amount)


def settle_delivered(vendor_id, amount):
    """Sub-order delivered — move the earning from pending to available."""
    wallet = get_or_create_wallet(vendor_id)
    amt = _d(amount)
    wallet.pending_balance = max(Decimal("0"), _d(wallet.pending_balance) - amt)
    wallet.available_balance = _d(wallet.available_balance) + amt
    wallet.total_earned = _d(wallet.total_earned) + amt


def unsettle_delivered(vendor_id, amount):
    """Reverse a settlement (sub-order status moved away from delivered)."""
    wallet = get_or_create_wallet(vendor_id)
    amt = _d(amount)
    wallet.available_balance = max(Decimal("0"), _d(wallet.available_balance) - amt)
    wallet.pending_balance = _d(wallet.pending_balance) + amt
    wallet.total_earned = max(Decimal("0"), _d(wallet.total_earned) - amt)


def hold_for_payout(vendor_id, amount):
    """Deduct a requested payout amount from available balance.

    Returns True on success, False if the balance is insufficient.
    """
    wallet = get_or_create_wallet(vendor_id)
    amt = _d(amount)
    if amt <= 0 or _d(wallet.available_balance) < amt:
        return False
    wallet.available_balance = _d(wallet.available_balance) - amt
    return True


def refund_payout(vendor_id, amount):
    """Return a rejected payout amount to the available balance."""
    wallet = get_or_create_wallet(vendor_id)
    wallet.available_balance = _d(wallet.available_balance) + _d(amount)
