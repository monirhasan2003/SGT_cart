"""Notification service — Phase 8.

One entry point, `notify()`, used by orders, chat, payouts and product review:
it stores an in-app `Notification`, broadcasts it live over SocketIO, and
pushes it to the user's mobile devices via FCM.
"""
from app.extensions import db
from app.models.notification import Notification
from app.sockets import emit_to_user
from app.services import push_service


def notify(user_id, kind, title, body=None, url=None):
    """Create + deliver a notification to one user.

    Adds the row and flushes it; the **caller commits** (so a notification is
    only persisted if the action that triggered it succeeds). The live socket
    event and device push are sent immediately.
    """
    note = Notification(
        user_id=user_id, kind=kind, title=title,
        body=(body or "")[:500] or None, url=url,
    )
    db.session.add(note)
    db.session.flush()

    payload = {
        "id": note.id, "kind": kind, "title": title,
        "body": note.body, "url": url,
        "created_at": note.created_at.isoformat() if note.created_at else None,
    }
    emit_to_user(user_id, "notification", payload)
    push_service.send_push(user_id, title, note.body or "",
                           {"url": url or "", "kind": kind})
    return note


def notification_json(note):
    """Serialize a notification for the REST API."""
    return {
        "id": note.id,
        "kind": note.kind,
        "title": note.title,
        "body": note.body,
        "url": note.url,
        "is_read": note.is_read,
        "created_at": note.created_at.isoformat() if note.created_at else None,
    }


def unread_count(user_id):
    return Notification.query.filter_by(user_id=user_id, is_read=False).count()


def mark_read(user_id, notification_id):
    """Mark one notification read (only if it belongs to the user)."""
    note = db.session.get(Notification, notification_id)
    if note is None or note.user_id != user_id:
        return False
    if not note.is_read:
        note.is_read = True
        db.session.commit()
    return True


def mark_all_read(user_id):
    """Mark every unread notification of a user as read. Returns the count."""
    count = (Notification.query
             .filter_by(user_id=user_id, is_read=False)
             .update({"is_read": True}))
    db.session.commit()
    return count
