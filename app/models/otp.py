"""One-time-code model for login & password-reset OTPs — Phase 1.

OTPs are stored in the database (Redis is not yet provisioned). Each code is
short-lived and single-use, with an attempt counter to block brute force.
"""
from datetime import datetime

from app.extensions import db

OTP_PURPOSE_LOGIN = "login"
OTP_PURPOSE_RESET = "reset"


class OtpCode(db.Model):
    __tablename__ = "otp_codes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    code = db.Column(db.String(10), nullable=False)
    purpose = db.Column(db.String(20), nullable=False)  # login / reset
    expires_at = db.Column(db.DateTime, nullable=False)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    is_used = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User")

    @property
    def is_expired(self):
        return datetime.utcnow() >= self.expires_at

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired

    def __repr__(self):
        return f"<OtpCode {self.purpose} user={self.user_id}>"
