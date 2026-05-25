"""API v1 — in-app notifications & device (FCM) token registration.

The apps poll `/notifications` and also receive them live over SocketIO;
`/devices` registers a Firebase token so the backend can push while the app
is closed.
"""
from datetime import datetime

from flask import request, jsonify

from app.extensions import db
from app.models.notification import Notification, DeviceToken, DEVICE_ANDROID
from app.services.notification_service import (
    notification_json, unread_count, mark_read, mark_all_read,
)
from .helpers import err, current_api_user, role_required
from . import api_v1

# Customers and sellers both have a notification feed.
app_user_required = role_required("customer", "seller")
_PLATFORMS = ("android", "ios", "web")


@api_v1.route("/notifications", methods=["GET"])
@app_user_required
def list_notifications():
    user = current_api_user()
    items = (
        Notification.query.filter_by(user_id=user.id)
        .order_by(Notification.id.desc()).limit(100).all()
    )
    return jsonify({
        "notifications": [notification_json(n) for n in items],
        "unread": unread_count(user.id),
    })


@api_v1.route("/notifications/unread-count", methods=["GET"])
@app_user_required
def notifications_unread_count():
    return jsonify({"unread": unread_count(current_api_user().id)})


@api_v1.route("/notifications/<int:notification_id>/read", methods=["POST"])
@app_user_required
def read_notification(notification_id):
    if not mark_read(current_api_user().id, notification_id):
        return err("Notification not found.", 404)
    return jsonify({"message": "Notification marked read."})


@api_v1.route("/notifications/read-all", methods=["POST"])
@app_user_required
def read_all_notifications():
    count = mark_all_read(current_api_user().id)
    return jsonify({"marked_read": count})


# --------------------------------------------------------------------------
# device (FCM) tokens
# --------------------------------------------------------------------------
@api_v1.route("/devices", methods=["POST"])
@app_user_required
def register_device():
    """Register (or refresh) this device's FCM token for push notifications."""
    user = current_api_user()
    data = request.get_json(silent=True) or {}
    token = (data.get("token") or "").strip()
    if not token:
        return err("token is required.")
    platform = (data.get("platform") or DEVICE_ANDROID).strip().lower()
    if platform not in _PLATFORMS:
        platform = DEVICE_ANDROID

    device = DeviceToken.query.filter_by(token=token).first()
    if device is None:
        device = DeviceToken(token=token)
        db.session.add(device)
    # A token can move between accounts (shared device) — keep it current.
    device.user_id = user.id
    device.platform = platform
    device.last_used_at = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Device registered for push notifications."}), 201


@api_v1.route("/devices", methods=["DELETE"])
@app_user_required
def unregister_device():
    """Remove a device token (on logout / push opt-out)."""
    user = current_api_user()
    token = ((request.get_json(silent=True) or {}).get("token") or "").strip()
    device = DeviceToken.query.filter_by(token=token, user_id=user.id).first()
    if device is None:
        return err("Device token not found.", 404)
    db.session.delete(device)
    db.session.commit()
    return jsonify({"message": "Device unregistered."})
