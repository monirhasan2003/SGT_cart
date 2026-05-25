"""Policy-violation log — Phase 15 Chunk D-0.

Every time the phone-number guard redacts something authored by a SELLER
account (chat message, Q&A answer, etc.), one row is written here. Once a
seller crosses `SELLER_VIOLATION_THRESHOLD` rows, `policy_service` auto-
suspends their `VendorProfile` (admin + seller both notified). The admin
panel can browse the log and manually un-suspend.

Customer-authored violations are *not* logged — their text is redacted but
they are not blocked. The marketplace rule lives in
`marketplace-feature-rules` memory.
"""
from datetime import datetime

from app.extensions import db

SURFACE_CHAT = "chat"        # ChatMessage
SURFACE_REVIEW = "review"    # Review (currently customer-only, kept for completeness)
SURFACE_QA = "qa"            # Q&A Answer (D-2)
SURFACES = (SURFACE_CHAT, SURFACE_REVIEW, SURFACE_QA)

# How many violations a seller may accumulate before being auto-suspended.
SELLER_VIOLATION_THRESHOLD = 2


class PolicyViolation(db.Model):
    """One redaction event for one user."""

    __tablename__ = "policy_violations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    surface = db.Column(db.String(20), nullable=False, index=True)
    excerpt = db.Column(db.String(500))           # offending text (already redacted)
    ref_kind = db.Column(db.String(20))           # "thread" / "review" / "answer"
    ref_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship("User")

    def __repr__(self):
        return f"<PolicyViolation {self.id} user={self.user_id} {self.surface}>"
