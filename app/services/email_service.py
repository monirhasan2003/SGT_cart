"""Email sending — Phase 1.

Sent synchronously for now; Phase 8 moves delivery to a Celery task so login
requests are not blocked on SMTP.
"""
from flask import current_app, render_template

from flask_mail import Message

from app.extensions import mail
from app.models.otp import OTP_PURPOSE_RESET


def send_email(subject, recipients, html, text=None):
    """Send an HTML email."""
    msg = Message(
        subject=subject,
        recipients=recipients,
        html=html,
        body=text or "",
        sender=current_app.config.get("MAIL_DEFAULT_SENDER"),
    )
    mail.send(msg)


def send_otp_email(user, code, purpose):
    """Email a login or password-reset OTP to the user."""
    app_name = current_app.config["APP_NAME"]
    minutes = current_app.config["OTP_EXPIRY_MINUTES"]

    if purpose == OTP_PURPOSE_RESET:
        subject = f"{app_name} — Password Reset Code"
        heading = "Password Reset"
        intro = "Use the code below to reset your password."
    else:
        subject = f"{app_name} — Login Verification Code"
        heading = "Login Verification"
        intro = "Use the code below to complete your login."

    html = render_template(
        "emails/otp_email.html",
        user=user, code=code, heading=heading, intro=intro,
        minutes=minutes, app_name=app_name,
    )
    text = f"Your {app_name} verification code is {code} (valid for {minutes} minutes)."
    send_email(subject, [user.email], html, text=text)


def send_abandoned_cart_email(user, item_count, cart_value):
    """Remind a customer about items left in their cart (Phase 9)."""
    app_name = current_app.config["APP_NAME"]
    subject = f"{app_name} — You left {item_count} item(s) in your cart"
    html = render_template(
        "emails/abandoned_cart.html",
        user=user, item_count=item_count, cart_value=cart_value, app_name=app_name,
    )
    text = (f"Hi {user.name}, you still have {item_count} item(s) worth "
            f"Tk {cart_value} in your {app_name} cart. Complete your order today!")
    send_email(subject, [user.email], html, text=text)
