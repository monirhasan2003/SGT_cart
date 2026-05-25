"""Notification & device-token models — Phase 8.

`Notification` is the in-app notification feed (web + apps). `DeviceToken`
stores Firebase Cloud Messaging tokens so the backend can push to the apps.
"""
from datetime import datetime

from app.extensions import db
from app.utils.i18n import localized

# Notification categories — used to pick an icon and a destination.
NOTIF_ORDER = "order"        # order placed / status changed
NOTIF_CHAT = "chat"          # new chat message
NOTIF_PAYOUT = "payout"      # payout request approved / rejected
NOTIF_PRODUCT = "product"    # product approved / rejected
NOTIF_SYSTEM = "system"      # generic platform notice
NOTIF_KINDS = (NOTIF_ORDER, NOTIF_CHAT, NOTIF_PAYOUT, NOTIF_PRODUCT, NOTIF_SYSTEM)

# Mobile platforms a device token can belong to.
DEVICE_ANDROID = "android"
DEVICE_IOS = "ios"
DEVICE_WEB = "web"


class Notification(db.Model):
    """An in-app notification addressed to one user."""

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    kind = db.Column(db.String(20), nullable=False, default=NOTIF_SYSTEM)
    title = db.Column(db.String(160), nullable=False)
    title_bn = db.Column(db.String(160))
    body = db.Column(db.String(500))
    body_bn = db.Column(db.String(500))
    url = db.Column(db.String(255))            # in-app link to open
    is_read = db.Column(db.Boolean, nullable=False, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship(
        "User", backref=db.backref("notifications", cascade="all, delete-orphan")
    )

    @property
    def localized_title(self):
        return localized(self.title, self.title_bn)

    @property
    def localized_body(self):
        return localized(self.body, self.body_bn)

    def __repr__(self):
        return f"<Notification {self.id} user={self.user_id} {self.kind}>"


class DeviceToken(db.Model):
    """A Firebase Cloud Messaging token for one of a user's devices."""

    __tablename__ = "device_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    platform = db.Column(db.String(10), nullable=False, default=DEVICE_ANDROID)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        "User", backref=db.backref("device_tokens", cascade="all, delete-orphan")
    )

    def __repr__(self):
        return f"<DeviceToken {self.id} user={self.user_id} {self.platform}>"
