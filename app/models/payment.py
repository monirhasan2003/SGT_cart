"""Payment transaction model — Phase 4.

One Transaction per payment attempt on an Order. COD orders get a single
`pending` transaction; SSLCommerz orders move initiated -> success/failed.
"""
from datetime import datetime

from app.extensions import db

# Gateways
GATEWAY_COD = "cod"
GATEWAY_SSLCOMMERZ = "sslcommerz"

# Transaction status
TXN_INITIATED = "initiated"   # SSLCommerz session started, awaiting gateway
TXN_PENDING = "pending"       # COD — collected on delivery
TXN_SUCCESS = "success"
TXN_FAILED = "failed"
TXN_CANCELLED = "cancelled"


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True)

    gateway = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=TXN_INITIATED)

    # SSLCommerz references
    gateway_txn_id = db.Column(db.String(120))   # val_id
    bank_txn_id = db.Column(db.String(120))
    card_type = db.Column(db.String(60))
    raw_response = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    order = db.relationship("Order", backref=db.backref("transactions", cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<Transaction {self.id} order={self.order_id} {self.gateway}:{self.status}>"
