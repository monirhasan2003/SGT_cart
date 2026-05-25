"""Flask-SocketIO real-time layer — Phase 8.

Rooms:
  * ``user:<id>``    — every device/tab of one user; carries notifications,
                        order-tracking updates and chat alerts.
  * ``thread:<id>``  — the participants of one chat thread; carries live
                        messages.

Web clients authenticate the socket with their Flask-Login session cookie;
the mobile apps pass a JWT access token in the connection ``auth`` payload.
"""
from app.extensions import socketio


def user_room(user_id):
    return f"user:{user_id}"


def thread_room(thread_id):
    return f"thread:{thread_id}"


def emit_to_user(user_id, event, data):
    """Push an event to every connection a user has open."""
    socketio.emit(event, data, room=user_room(user_id))


def register_socket_handlers():
    """Import handler modules so their ``@socketio.on`` routes register."""
    from . import events  # noqa: F401
