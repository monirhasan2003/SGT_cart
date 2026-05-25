"""API v1 — authentication endpoints (JWT).

Login flow for the apps (customers & sellers):
    POST /auth/login        -> emails an OTP, returns {otp_required: true}
    POST /auth/verify-otp   -> returns {access_token, refresh_token, user}
Admins are not served by the app API.
"""
from datetime import datetime

from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity,
)
from slugify import slugify

from app.extensions import db, limiter
from app.models.user import User, ROLE_CUSTOMER, ROLE_SELLER
from app.models.vendor import VendorProfile, VENDOR_PENDING
from app.models.otp import OTP_PURPOSE_LOGIN, OTP_PURPOSE_RESET
from app.services.otp_service import issue_otp, verify_otp
from app.services.email_service import send_otp_email
from . import api_v1


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def err(message, status=400):
    return jsonify({"error": message}), status


def user_json(user):
    data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "role": user.role,
        "locale": user.locale,
        "is_email_verified": user.is_email_verified,
    }
    if user.is_seller and user.vendor_profile:
        vp = user.vendor_profile
        data["vendor"] = {
            "shop_name": vp.shop_name_en,
            "slug": vp.slug,
            "status": vp.status,
            "verification_submitted": vp.is_verification_submitted,
        }
    return data


def _issue_tokens(user):
    claims = {"role": user.role}
    return (
        create_access_token(identity=str(user.id), additional_claims=claims),
        create_refresh_token(identity=str(user.id)),
    )


def _unique_vendor_slug(name):
    base = slugify(name) or "shop"
    slug, i = base, 2
    while VendorProfile.query.filter_by(slug=slug).first() is not None:
        slug = f"{base}-{i}"
        i += 1
    return slug


# --------------------------------------------------------------------------
# registration
# --------------------------------------------------------------------------
@api_v1.route("/auth/register", methods=["POST"])
@limiter.limit("10 per hour")
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    phone = (data.get("phone") or "").strip()
    password = data.get("password") or ""
    role = data.get("role") or ROLE_CUSTOMER
    shop_name = (data.get("shop_name") or "").strip()

    if role not in (ROLE_CUSTOMER, ROLE_SELLER):
        return err("role must be 'customer' or 'seller'.")
    if not name:
        return err("name is required.")
    if not email or "@" not in email:
        return err("A valid email is required.")
    if len(password) < 6:
        return err("password must be at least 6 characters.")
    if role == ROLE_SELLER and not shop_name:
        return err("shop_name is required for a seller account.")
    if User.query.filter_by(email=email).first():
        return err("An account with this email already exists.", 409)

    user = User(name=name, email=email, phone=phone, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()
    if role == ROLE_SELLER:
        from app.services.settings_service import get_decimal
        db.session.add(VendorProfile(
            user_id=user.id, shop_name_en=shop_name,
            slug=_unique_vendor_slug(shop_name), phone=phone, status=VENDOR_PENDING,
            commission_rate=get_decimal("default_commission_rate"),
        ))
    db.session.commit()

    # Referral program: give the new user a code, credit a valid referrer.
    from app.services import referral_service
    referral_service.ensure_code(user)
    ref_code = (data.get("referral_code") or "").strip()
    if ref_code:
        referrer = referral_service.find_by_code(ref_code)
        if referrer is not None:
            referral_service.record_referral(referrer, user)
            db.session.commit()
    return jsonify({"message": "Account created. Please log in.",
                    "user": user_json(user)}), 201


# --------------------------------------------------------------------------
# login + OTP
# --------------------------------------------------------------------------
@api_v1.route("/auth/login", methods=["POST"])
@limiter.limit("15 per minute")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        return err("Invalid email or password.", 401)
    if not user.is_active:
        return err("Your account is disabled.", 403)
    if user.is_admin:
        return err("Admin login is not available in the app.", 403)

    otp = issue_otp(user, OTP_PURPOSE_LOGIN)
    try:
        send_otp_email(user, otp.code, OTP_PURPOSE_LOGIN)
    except Exception:  # noqa: BLE001
        return err("Could not send the verification code. Please try again.", 502)
    return jsonify({"otp_required": True, "email": user.email,
                    "message": "A verification code was sent to your email."})


@api_v1.route("/auth/verify-otp", methods=["POST"])
@limiter.limit("15 per minute")
def verify_login_otp():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    code = data.get("code") or ""

    user = User.query.filter_by(email=email).first()
    if user is None:
        return err("Account not found.", 404)

    ok, message = verify_otp(user, OTP_PURPOSE_LOGIN, code)
    if not ok:
        return err(message, 400)

    user.last_login_at = datetime.utcnow()
    db.session.commit()
    access, refresh = _issue_tokens(user)
    return jsonify({"access_token": access, "refresh_token": refresh,
                    "user": user_json(user)})


@api_v1.route("/auth/resend-otp", methods=["POST"])
@limiter.limit("5 per minute")
def resend_otp():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if user is None:
        return err("Account not found.", 404)
    otp = issue_otp(user, OTP_PURPOSE_LOGIN)
    try:
        send_otp_email(user, otp.code, OTP_PURPOSE_LOGIN)
    except Exception:  # noqa: BLE001
        return err("Could not send the code.", 502)
    return jsonify({"message": "A new verification code was sent."})


@api_v1.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user = db.session.get(User, int(get_jwt_identity()))
    if user is None or not user.is_active:
        return err("Account not available.", 401)
    access, _ = _issue_tokens(user)
    return jsonify({"access_token": access})


# --------------------------------------------------------------------------
# forgot / reset password
# --------------------------------------------------------------------------
@api_v1.route("/auth/forgot-password", methods=["POST"])
@limiter.limit("5 per minute")
def forgot_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    user = User.query.filter_by(email=email).first()
    if user is None:
        return err("No account found with that email.", 404)
    otp = issue_otp(user, OTP_PURPOSE_RESET)
    try:
        send_otp_email(user, otp.code, OTP_PURPOSE_RESET)
    except Exception:  # noqa: BLE001
        return err("Could not send the reset code.", 502)
    return jsonify({"message": "A password reset code was sent to your email."})


@api_v1.route("/auth/reset-password", methods=["POST"])
@limiter.limit("10 per minute")
def reset_password():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    code = data.get("code") or ""
    password = data.get("password") or ""

    if len(password) < 6:
        return err("password must be at least 6 characters.")
    user = User.query.filter_by(email=email).first()
    if user is None:
        return err("Account not found.", 404)

    ok, message = verify_otp(user, OTP_PURPOSE_RESET, code)
    if not ok:
        return err(message, 400)
    user.set_password(password)
    db.session.commit()
    return jsonify({"message": "Password reset successfully. Please log in."})


# --------------------------------------------------------------------------
# current user
# --------------------------------------------------------------------------
@api_v1.route("/auth/me", methods=["GET"])
@jwt_required()
def me():
    user = db.session.get(User, int(get_jwt_identity()))
    if user is None:
        return err("Account not found.", 404)
    return jsonify({"user": user_json(user)})
