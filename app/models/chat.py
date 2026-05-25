"""Chat models — Phase 8 (real-time messaging).

The marketplace runs TWO separate chat systems:

  * CHAT_SUPPORT  — customer  <-> platform (admin): delivery, refunds, disputes.
  * CHAT_VENDOR   — customer  <-> seller: product questions before/after buying.

Phone numbers are never allowed in chat (sellers must not move deals off the
platform); `app/utils/phone_guard.py` redacts them before a message is stored.
"""
from datetime import datetime

from app.extensions import db

CHAT_SUPPORT = "support"   # customer <-> platform
CHAT_VENDOR = "vendor"     # customer <-> seller
CHAT_KINDS = (CHAT_SUPPORT, CHAT_VENDOR)

# Support threads are triaged: before the chat opens the user picks WHAT the
# issue is about, so it reaches the right desk (and the seller never sees
# delivery/refund/payment matters — those stay with the platform).
SUPPORT_PURCHASE = "purchase"   # placing/changing an order, payment
SUPPORT_DELIVERY = "delivery"   # shipping / tracking / late delivery
SUPPORT_REFUND = "refund"       # returns, refunds, cancellations
SUPPORT_OTHER = "other"         # anything else
SUPPORT_TOPICS = (SUPPORT_PURCHASE, SUPPORT_DELIVERY, SUPPORT_REFUND, SUPPORT_OTHER)

# Human labels for the triage screen.
SUPPORT_TOPIC_LABELS = {
    SUPPORT_PURCHASE: "Purchase & payment",
    SUPPORT_DELIVERY: "Delivery & tracking",
    SUPPORT_REFUND: "Refund & return",
    SUPPORT_OTHER: "Other issue",
}


class ChatThread(db.Model):
    """One conversation. `kind` decides who the customer is talking to."""

    __tablename__ = "chat_threads"

    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(20), nullable=False, index=True)

    # The customer is always one side of the thread.
    customer_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    # The seller side — set only for vendor threads.
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor_profiles.id"), index=True)

    # Support triage topic — purchase / delivery / refund / other.
    # Set only for support threads; vendor threads are always about a product.
    topic = db.Column(db.String(20))

    # Optional context the thread is "about".
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))

    subject = db.Column(db.String(160))
    is_closed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship("User", foreign_keys=[customer_id])
    vendor = db.relationship("VendorProfile")
    product = db.relationship("Product")
    order = db.relationship("Order")
    messages = db.relationship(
        "ChatMessage", back_populates="thread",
        cascade="all, delete-orphan", order_by="ChatMessage.id",
    )

    def unread_count(self, user_id):
        """Messages in this thread not sent by `user_id` and still unread."""
        return sum(
            1 for m in self.messages
            if m.sender_id != user_id and not m.is_read
        )

    def __repr__(self):
        return f"<ChatThread {self.id} {self.kind}>"


class ChatMessage(db.Model):
    """A single message inside a thread."""

    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    thread_id = db.Column(
        db.Integer, db.ForeignKey("chat_threads.id"), nullable=False, index=True
    )
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    sender_role = db.Column(db.String(20), nullable=False)  # snapshot for display

    body = db.Column(db.Text, nullable=False)
    # Phase 15 D-7 — optional voice-message attachment (static path).
    audio_path = db.Column(db.String(255))
    # True when the phone-number guard redacted something from the message.
    is_flagged = db.Column(db.Boolean, nullable=False, default=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    thread = db.relationship("ChatThread", back_populates="messages")
    sender = db.relationship("User")

    def __repr__(self):
        return f"<ChatMessage {self.id} thread={self.thread_id}>"
