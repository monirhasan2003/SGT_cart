"""OTP issuing and verification — Phase 1.

Customers and sellers verify an emailed one-time code on every login; the same
mechanism backs password reset. Admins are exempt from login OTP.
"""
import secrets
from datetime import datetime, timedelta

from flask import current_app

from app.extensions import db
from app.models.otp import OtpCode


def _generate_code(length):
    return "".join(secrets.choice("0123456789") for _ in range(length))


def issue_otp(user, purpose):
    """Invalidate any prior unused codes for this purpose, then create a new one.

    Returns the new :class:`OtpCode`.
    """
    OtpCode.query.filter_by(
        user_id=user.id, purpose=purpose, is_used=False
    ).update({"is_used": True})

    length = current_app.config["OTP_LENGTH"]
    minutes = current_app.config["OTP_EXPIRY_MINUTES"]
    otp = OtpCode(
        user_id=user.id,
        code=_generate_code(length),
        purpose=purpose,
        expires_at=datetime.utcnow() + timedelta(minutes=minutes),
    )
    db.session.add(otp)
    db.session.commit()
    return otp


def verify_otp(user, purpose, code):
    """Validate a submitted code.

    Returns ``(ok: bool, message: str)``. On success the code is consumed.
    """
    otp = (
        OtpCode.query
        .filter_by(user_id=user.id, purpose=purpose, is_used=False)
        .order_by(OtpCode.id.desc())
        .first()
    )
    if otp is None:
        return False, "No active code. Please request a new one."
    if otp.is_expired:
        return False, "Code has expired. Please request a new one."

    max_attempts = current_app.config["OTP_MAX_ATTEMPTS"]
    if otp.attempts >= max_attempts:
        otp.is_used = True
        db.session.commit()
        return False, "Too many incorrect attempts. Please request a new code."

    if otp.code != (code or "").strip():
        otp.attempts += 1
        db.session.commit()
        return False, "Incorrect code. Please try again."

    otp.is_used = True
    db.session.commit()
    return True, "OK"
