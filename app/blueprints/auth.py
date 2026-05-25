"""Authentication — registration, OTP login, logout, password reset (Phase 1).

Login flow:
  * Customers & sellers  ->  email + password  ->  emailed OTP  ->  verified login
  * Admins               ->  email + password  ->  straight in (no OTP)
Forgot password uses an emailed OTP as well.
"""
from datetime import datetime

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session,
    current_app,
)
from flask_login import login_user, logout_user, login_required, current_user
from slugify import slugify

from app.extensions import db, limiter
from app.models.user import User, ROLE_CUSTOMER, ROLE_SELLER
from app.models.vendor import VendorProfile, VENDOR_PENDING
from app.models.otp import OTP_PURPOSE_LOGIN, OTP_PURPOSE_RESET
from app.services.otp_service import issue_otp, verify_otp as check_otp
from app.services.email_service import send_otp_email
from app.services.settings_service import get_decimal
from app.services import referral_service

auth = Blueprint("auth", __name__)

PENDING_LOGIN = "pending_login_user_id"
PENDING_RESET = "pending_reset_user_id"
REMEMBER_FLAG = "login_remember"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _redirect_after_login(user):
    """Send the user to their role's landing page."""
    if user.is_admin:
        return redirect(url_for("admin.dashboard"))
    if user.is_seller:
        return redirect(url_for("seller.dashboard"))
    return redirect(url_for("account.dashboard"))


def _unique_vendor_slug(name):
    base = slugify(name) or "shop"
    slug, i = base, 2
    while VendorProfile.query.filter_by(slug=slug).first() is not None:
        slug = f"{base}-{i}"
        i += 1
    return slug


def _send_login_otp(user):
    """Issue + email a login OTP. Returns True on success."""
    otp = issue_otp(user, OTP_PURPOSE_LOGIN)
    try:
        send_otp_email(user, otp.code, OTP_PURPOSE_LOGIN)
        return True
    except Exception as exc:  # noqa: BLE001 - surface any SMTP failure to the user
        current_app.logger.error("Login OTP email failed: %s", exc)
        return False


# --------------------------------------------------------------------------
# login + OTP
# --------------------------------------------------------------------------
@auth.route("/login/", methods=["GET", "POST"])
@limiter.limit("20 per minute", methods=["POST"])
def login():
    if current_user.is_authenticated:
        return _redirect_after_login(current_user)

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("pages/login.html")
        if not user.is_active:
            flash("Your account is disabled. Please contact support.", "danger")
            return render_template("pages/login.html")

        # Admins sign in from their own dedicated page (/admin/login).
        if user.is_admin:
            flash("Admins sign in from the Admin login page.", "warning")
            return redirect(url_for("admin.login"))

        # The login page has a Customer/Seller toggle; guard against the wrong tab.
        account_type = request.form.get("account_type") or "customer"
        if account_type in ("customer", "seller") and user.role != account_type:
            flash(
                f"This is a {user.role} account. Please use the "
                f"{user.role.capitalize()} tab to log in.",
                "danger",
            )
            return render_template("pages/login.html")

        session[REMEMBER_FLAG] = bool(request.form.get("remember"))

        if user.requires_otp:
            if not _send_login_otp(user):
                flash("Could not send the verification code. Please try again.", "danger")
                return render_template("pages/login.html")
            session[PENDING_LOGIN] = user.id
            flash(f"A verification code was sent to {user.email}.", "info")
            return redirect(url_for("auth.verify_otp"))

        # Admin: no OTP.
        login_user(user, remember=session.pop(REMEMBER_FLAG, False))
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        flash("Welcome back!", "success")
        return _redirect_after_login(user)

    return render_template("pages/login.html")


@auth.route("/verify-otp/", methods=["GET", "POST"])
@limiter.limit("20 per minute", methods=["POST"])
def verify_otp():
    user_id = session.get(PENDING_LOGIN)
    if not user_id:
        flash("Please log in first.", "warning")
        return redirect(url_for("auth.login"))
    user = db.session.get(User, user_id)
    if user is None:
        session.pop(PENDING_LOGIN, None)
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        ok, message = check_otp(user, OTP_PURPOSE_LOGIN, request.form.get("code"))
        if not ok:
            flash(message, "danger")
            return render_template("pages/verify-otp.html", email=user.email)

        login_user(user, remember=session.pop(REMEMBER_FLAG, False))
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        session.pop(PENDING_LOGIN, None)
        flash("Logged in successfully.", "success")
        return _redirect_after_login(user)

    return render_template("pages/verify-otp.html", email=user.email)


@auth.route("/resend-otp/", methods=["POST"])
def resend_otp():
    user_id = session.get(PENDING_LOGIN)
    if not user_id:
        return redirect(url_for("auth.login"))
    user = db.session.get(User, user_id)
    if user and _send_login_otp(user):
        flash("A new verification code was sent.", "info")
    else:
        flash("Could not send the code. Please try again.", "danger")
    return redirect(url_for("auth.verify_otp"))


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    session.pop("impersonator_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


# --------------------------------------------------------------------------
# registration
# --------------------------------------------------------------------------
@auth.route("/signup/", methods=["GET", "POST"])
@limiter.limit("10 per hour", methods=["POST"])
def register():
    if current_user.is_authenticated:
        return _redirect_after_login(current_user)

    if request.method == "POST":
        first = (request.form.get("first_name") or "").strip()
        last = (request.form.get("last_name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        phone = (request.form.get("phone") or "").strip()
        password = request.form.get("password") or ""
        confirm = request.form.get("confirm_password") or ""
        role = request.form.get("role") or ROLE_CUSTOMER
        shop_name = (request.form.get("shop_name") or "").strip()

        if role not in (ROLE_CUSTOMER, ROLE_SELLER):
            role = ROLE_CUSTOMER

        errors = []
        if not first:
            errors.append("First name is required.")
        if not email or "@" not in email:
            errors.append("A valid email address is required.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if role == ROLE_SELLER and not shop_name:
            errors.append("Shop name is required for a seller account.")
        if email and User.query.filter_by(email=email).first():
            errors.append("An account with this email already exists.")

        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("pages/signup.html", form=request.form)

        user = User(
            name=(first + " " + last).strip(),
            email=email,
            phone=phone,
            role=role,
            locale=session.get("lang", "en"),
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()  # assign user.id

        if role == ROLE_SELLER:
            db.session.add(VendorProfile(
                user_id=user.id,
                shop_name_en=shop_name,
                slug=_unique_vendor_slug(shop_name),
                phone=phone,
                status=VENDOR_PENDING,
                commission_rate=get_decimal("default_commission_rate"),
            ))
        db.session.commit()

        # Give the new user their own referral code; credit a referrer if a
        # valid referral code was entered.
        referral_service.ensure_code(user)
        ref_code = (request.form.get("referral_code") or "").strip()
        if ref_code:
            referrer = referral_service.find_by_code(ref_code)
            if referrer is not None:
                referral_service.record_referral(referrer, user)
                db.session.commit()

        if role == ROLE_SELLER:
            flash("Seller account created — pending admin approval. You can log in now.", "success")
        else:
            flash("Account created successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    # `?role=seller` on the Sell on SGT landing pre-selects the seller tab.
    initial = {"role": request.args.get("role")} if request.args.get("role") else {}
    return render_template("pages/signup.html", form=initial)


# --------------------------------------------------------------------------
# forgot / reset password (OTP based)
# --------------------------------------------------------------------------
@auth.route("/forgot-password/", methods=["GET", "POST"])
@limiter.limit("5 per minute", methods=["POST"])
def forgot_password():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        user = User.query.filter_by(email=email).first()
        if user is None:
            flash("No account found with that email address.", "danger")
            return render_template("pages/forgot-password.html")

        otp = issue_otp(user, OTP_PURPOSE_RESET)
        try:
            send_otp_email(user, otp.code, OTP_PURPOSE_RESET)
        except Exception as exc:  # noqa: BLE001
            current_app.logger.error("Reset OTP email failed: %s", exc)
            flash("Could not send the reset code. Please try again.", "danger")
            return render_template("pages/forgot-password.html")

        session[PENDING_RESET] = user.id
        flash(f"A password reset code was sent to {user.email}.", "info")
        return redirect(url_for("auth.reset_password"))

    return render_template("pages/forgot-password.html")


@auth.route("/reset-password/", methods=["GET", "POST"])
def reset_password():
    user_id = session.get(PENDING_RESET)
    if not user_id:
        flash("Please request a password reset first.", "warning")
        return redirect(url_for("auth.forgot_password"))
    user = db.session.get(User, user_id)
    if user is None:
        session.pop(PENDING_RESET, None)
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password") or ""
        confirm = request.form.get("confirm_password") or ""

        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("pages/reset-password.html", email=user.email)
        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("pages/reset-password.html", email=user.email)

        ok, message = check_otp(user, OTP_PURPOSE_RESET, request.form.get("code"))
        if not ok:
            flash(message, "danger")
            return render_template("pages/reset-password.html", email=user.email)

        user.set_password(password)
        db.session.commit()
        session.pop(PENDING_RESET, None)
        flash("Password reset successfully. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("pages/reset-password.html", email=user.email)
