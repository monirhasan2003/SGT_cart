"""Vendor wallet & payout models — Phase 5.

Earnings flow:
  order placed       -> vendor_earning added to wallet.pending_balance
  sub-order delivered-> earning moved pending_balance -> available_balance
  payout requested   -> amount held (removed from available_balance)
  payout approved    -> done (money paid out off-platform)
  payout rejected    -> amount returned to available_balance
"""
from datetime import datetime

from app.extensions import db

PAYOUT_REQUESTED = "requested"
PAYOUT_APPROVED = "approved"
PAYOUT_REJECTED = "rejected"
PAYOUT_STATUSES = (PAYOUT_REQUESTED, PAYOUT_APPROVED, PAYOUT_REJECTED)


class VendorWallet(db.Model):
    """One wallet per vendor — tracks withdrawable and pending earnings."""

    __tablename__ = "vendor_wallets"

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(
        db.Integer, db.ForeignKey("vendor_profiles.id"), unique=True, nullable=False
    )
    available_balance = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    pending_balance = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total_earned = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    vendor = db.relationship(
        "VendorProfile", backref=db.backref("wallet", uselist=False,
                                            cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<VendorWallet vendor={self.vendor_id} avail={self.available_balance}>"


class PayoutRequest(db.Model):
    """A seller's request to withdraw money from their available balance."""

    __tablename__ = "payout_requests"

    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(
        db.Integer, db.ForeignKey("vendor_profiles.id"), nullable=False, index=True
    )
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    method = db.Column(db.String(40))           # bkash / nagad / bank (snapshot)
    account_detail = db.Column(db.String(255))  # snapshot of payout destination
    status = db.Column(db.String(20), nullable=False, default=PAYOUT_REQUESTED, index=True)
    admin_note = db.Column(db.String(255))
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)

    vendor = db.relationship("VendorProfile", backref="payout_requests")

    def __repr__(self):
        return f"<PayoutRequest {self.id} vendor={self.vendor_id} {self.status}>"
