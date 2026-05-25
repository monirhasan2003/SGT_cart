"""SocketIO connection & room handlers — Phase 8.

Chat-message events are added in Chunk B; this module establishes the
connection model: on connect a user joins their personal ``user:<id>`` room,
and may join/leave per-thread rooms explicitly.

Phase 15 D-7 — connect + disconnect also drive the chat presence indicator:
`presence_service.mark_user_online` stamps in-memory recency, and the DB
column `User.last_seen_at` is refreshed on disconnect for offline fallback.
"""
from datetime import datetime

from flask_login import current_user
from flask_jwt_extended import decode_token
from flask_socketio import join_room, leave_room

from app.extensions import socketio, db
from app.models.user import User
from app.models.chat import ChatThread
from app.services import presence_service
from . import user_room, thread_room


def _user_from_auth(auth):
    """Resolve the connecting user from a session or a JWT in `auth`."""
    if current_user.is_authenticated:
        return current_user
    if isinstance(auth, dict) and auth.get("token"):
        try:
            identity = decode_token(auth["token"])["sub"]
            return db.session.get(User, int(identity))
        except Exception:  # noqa: BLE001 — bad/expired token: treat as anonymous
            return None
    return None


def _can_access_thread(user, thread):
    """True when `user` is a participant of `thread`."""
    if thread is None or user is None:
        return False
    if user.is_admin:
        return True
    if thread.customer_id == user.id:
        return True
    if thread.vendor_id and user.vendor_profile:
        return thread.vendor_id == user.vendor_profile.id
    return False


@socketio.on("connect")
def on_connect(auth=None):
    """Join the user's personal room + mark them online (Phase 15 D-7)."""
    user = _user_from_auth(auth)
    if user is None:
        return  # allow anonymous connections (public pages) without a room
    join_room(user_room(user.id))
    presence_service.mark_user_online(user.id)
    user.last_seen_at = datetime.utcnow()
    db.session.commit()


@socketio.on("disconnect")
def on_disconnect():
    """Persist last-seen on disconnect for offline-fallback rendering."""
    if current_user.is_authenticated:
        current_user.last_seen_at = datetime.utcnow()
        db.session.commit()


@socketio.on("join_thread")
def on_join_thread(data):
    """Subscribe to live messages for one chat thread (after access check)."""
    user = _user_from_auth(None)
    thread = db.session.get(ChatThread, (data or {}).get("thread_id"))
    if _can_access_thread(user, thread):
        join_room(thread_room(thread.id))


@socketio.on("leave_thread")
def on_leave_thread(data):
    thread_id = (data or {}).get("thread_id")
    if thread_id:
        leave_room(thread_room(thread_id))
