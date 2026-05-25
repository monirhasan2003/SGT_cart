"""Firebase Cloud Messaging push — Phase 8.

Push is OPTIONAL: when no Firebase service-account file is configured (or the
`firebase-admin` package is not installed) the service degrades gracefully —
in-app notifications and live SocketIO events still work, only the device
push is skipped. Add `FCM_CREDENTIALS_FILE` to `.env` to enable it.
"""
import logging
import os

from flask import current_app

from app.models.notification import DeviceToken

logger = logging.getLogger(__name__)

# Lazily-initialised Firebase app; `_init_attempted` avoids retrying every call.
_firebase_app = None
_init_attempted = False


def _get_firebase():
    """Return the initialised Firebase app, or None when push is disabled."""
    global _firebase_app, _init_attempted
    if _init_attempted:
        return _firebase_app
    _init_attempted = True

    cred_file = current_app.config.get("FCM_CREDENTIALS_FILE")
    if not cred_file or not os.path.exists(cred_file):
        logger.info("FCM not configured — device push disabled.")
        return None
    try:
        import firebase_admin
        from firebase_admin import credentials
        _firebase_app = firebase_admin.initialize_app(
            credentials.Certificate(cred_file)
        )
        logger.info("Firebase Cloud Messaging initialised.")
    except Exception as exc:  # noqa: BLE001 — missing package or bad creds
        logger.warning("Firebase init failed (%s) — push disabled.", exc)
        _firebase_app = None
    return _firebase_app


def is_configured():
    """True when device push is available."""
    return _get_firebase() is not None


def send_push(user_id, title, body, data=None):
    """Push a notification to every registered device of a user.

    Returns the number of devices reached (0 when push is disabled).
    """
    if _get_firebase() is None:
        return 0

    from firebase_admin import messaging

    tokens = [d.token for d in DeviceToken.query.filter_by(user_id=user_id).all()]
    if not tokens:
        return 0

    payload = {k: str(v) for k, v in (data or {}).items()}
    sent = 0
    for token in tokens:
        try:
            messaging.send(messaging.Message(
                token=token,
                notification=messaging.Notification(title=title, body=body or ""),
                data=payload,
            ))
            sent += 1
        except Exception as exc:  # noqa: BLE001 — a stale token shouldn't break others
            logger.warning("Push to device %s… failed: %s", token[:12], exc)
    return sent
