"""Chat service — Phase 8.

Single source of truth for the two chat systems, shared by the web views,
the REST API and the socket layer:

  * support thread — customer <-> platform (admins)
  * vendor thread  — customer <-> seller

Every outgoing message passes through the phone-number guard, raises an
in-app notification for the recipient(s), and is broadcast live over SocketIO.
"""
from datetime import datetime

from app.extensions import db, socketio
from app.models.user import User, ROLE_ADMIN
from app.models.chat import (
    ChatThread, ChatMessage, CHAT_SUPPORT, CHAT_VENDOR,
    SUPPORT_TOPICS, SUPPORT_OTHER, SUPPORT_TOPIC_LABELS,
)
from app.models.notification import Notification, NOTIF_CHAT
from app.models.policy import SURFACE_CHAT
from app.services import policy_service
from app.sockets import thread_room, emit_to_user


# --------------------------------------------------------------------------
# thread creation / lookup
# --------------------------------------------------------------------------
def get_or_create_vendor_thread(customer, vendor, product=None):
    """The customer <-> seller thread for this pair (one per pair)."""
    thread = ChatThread.query.filter_by(
        kind=CHAT_VENDOR, customer_id=customer.id, vendor_id=vendor.id
    ).first()
    if thread is None:
        thread = ChatThread(
            kind=CHAT_VENDOR, customer_id=customer.id, vendor_id=vendor.id,
            product_id=product.id if product else None,
            subject=vendor.shop_name_en,
        )
        db.session.add(thread)
        db.session.commit()
    return thread


def get_or_create_support_thread(user, topic, order=None):
    """A customer <-> platform thread for one triaged issue.

    Threads are keyed on (user, topic, order): each distinct issue is its own
    conversation, so the support desk never mixes a refund with a delivery
    query. `topic` is one of chat.SUPPORT_TOPICS.
    """
    if topic not in SUPPORT_TOPICS:
        topic = SUPPORT_OTHER

    thread = ChatThread.query.filter_by(
        kind=CHAT_SUPPORT, customer_id=user.id, topic=topic,
        order_id=order.id if order else None, is_closed=False,
    ).first()
    if thread is None:
        label = SUPPORT_TOPIC_LABELS[topic]
        thread = ChatThread(
            kind=CHAT_SUPPORT, customer_id=user.id, topic=topic,
            order_id=order.id if order else None,
            subject=(f"{label} — order {order.order_number}" if order else label),
        )
        db.session.add(thread)
        db.session.commit()
    return thread


# --------------------------------------------------------------------------
# access control
# --------------------------------------------------------------------------
def can_access(user, thread):
    """True when `user` is a participant of `thread`."""
    if user is None or thread is None:
        return False
    # Direct participation wins — covers the case where an admin user
    # personally started a vendor chat (the admin is the thread's customer)
    # and would otherwise be locked out by the `is_admin` short-circuit below.
    if thread.customer_id == user.id:
        return True
    if (thread.kind == CHAT_VENDOR and thread.vendor_id
            and user.vendor_profile is not None
            and thread.vendor_id == user.vendor_profile.id):
        return True
    # Admins staff the support desk — but only for support threads they
    # didn't personally start (already covered above).
    if user.is_admin:
        return thread.kind == CHAT_SUPPORT
    return False


def threads_for(user):
    """Every thread `user` participates in, newest activity first."""
    if user.is_admin:
        threads = ChatThread.query.filter_by(kind=CHAT_SUPPORT).all()
    elif user.is_seller and user.vendor_profile is not None:
        threads = ChatThread.query.filter(
            db.or_(
                db.and_(ChatThread.kind == CHAT_VENDOR,
                        ChatThread.vendor_id == user.vendor_profile.id),
                ChatThread.customer_id == user.id,
            )
        ).all()
    else:
        threads = ChatThread.query.filter_by(customer_id=user.id).all()
    return sorted(
        threads,
        key=lambda t: t.last_message_at or t.created_at,
        reverse=True,
    )


# --------------------------------------------------------------------------
# messaging
# --------------------------------------------------------------------------
def _recipient_ids(thread, sender):
    """User ids to notify of a new message — everyone but the sender."""
    ids = set()
    if thread.kind == CHAT_SUPPORT:
        if sender.is_admin:
            ids.add(thread.customer_id)
        else:
            ids.update(a.id for a in User.query.filter_by(role=ROLE_ADMIN).all())
    else:  # vendor thread
        if sender.id == thread.customer_id:
            if thread.vendor is not None:
                ids.add(thread.vendor.user_id)
        else:
            ids.add(thread.customer_id)
    ids.discard(sender.id)
    return ids


def _thread_url_for(user_id, thread):
    """Where this recipient opens the thread (admins have their own panel)."""
    u = db.session.get(User, user_id)
    if u is not None and u.is_admin:
        return f"/admin/messages/{thread.id}"
    return f"/messages/{thread.id}"


def message_json(msg):
    """Serialize a message for the API and live socket events."""
    return {
        "id": msg.id,
        "thread_id": msg.thread_id,
        "sender_id": msg.sender_id,
        "sender_role": msg.sender_role,
        "sender_name": msg.sender.name if msg.sender else "",
        "body": msg.body,
        "audio_path": msg.audio_path,
        "is_flagged": msg.is_flagged,
        "is_read": msg.is_read,
        "created_at": msg.created_at.isoformat() if msg.created_at else None,
    }


def thread_json(thread, user, with_messages=False):
    """Serialize a thread for the API."""
    data = {
        "id": thread.id,
        "kind": thread.kind,
        "topic": thread.topic,
        "topic_label": SUPPORT_TOPIC_LABELS.get(thread.topic),
        "subject": thread.subject,
        "is_closed": thread.is_closed,
        "unread": thread.unread_count(user.id),
        "last_message_at": (thread.last_message_at.isoformat()
                            if thread.last_message_at else None),
        "vendor": ({"slug": thread.vendor.slug, "name": thread.vendor.shop_name_en}
                   if thread.vendor else None),
        "product": ({"slug": thread.product.slug, "title": thread.product.title_en}
                    if thread.product else None),
        "last_message": thread.messages[-1].body if thread.messages else None,
    }
    if with_messages:
        data["messages"] = [message_json(m) for m in thread.messages]
    return data


def post_message(thread, sender, body, audio_path=None):
    """Store a message (phone-guarded), notify + broadcast it.

    `audio_path` (Phase 15 D-7 C5) is an optional voice-message attachment
    saved as a static path. When supplied the message body may be a short
    placeholder ("[voice message]").

    Returns ``(ChatMessage, None)`` on success or ``(None, error_str)``.
    """
    raw = (body or "").strip()
    clean, flagged, _ = policy_service.redact_and_log(
        sender, raw, SURFACE_CHAT, ref_kind="thread", ref_id=thread.id,
    )
    if not clean.strip() and not audio_path:
        return None, "Message cannot be empty."

    msg = ChatMessage(
        thread_id=thread.id, sender_id=sender.id, sender_role=sender.role,
        body=clean or "[voice message]", audio_path=audio_path,
        is_flagged=flagged,
    )
    db.session.add(msg)
    thread.last_message_at = datetime.utcnow()
    thread.is_closed = False
    # Stamp presence so the "Last seen X ago" indicator stays fresh even
    # when the user posts via the plain HTML form (no socket).
    try:
        sender.last_seen_at = datetime.utcnow()
        from app.services import presence_service
        presence_service.mark_user_online(sender.id)
    except Exception:  # noqa: BLE001 — never block message storage
        pass
    db.session.flush()

    recipients = _recipient_ids(thread, sender)
    preview = clean[:160]
    for uid in recipients:
        db.session.add(Notification(
            user_id=uid, kind=NOTIF_CHAT,
            title=f"New message from {sender.name}",
            body=preview, url=_thread_url_for(uid, thread),
        ))
    db.session.commit()

    # Live delivery: the message to the open thread, a ping to each recipient.
    payload = message_json(msg)
    socketio.emit("chat_message", payload, room=thread_room(thread.id))
    for uid in recipients:
        emit_to_user(uid, "notification", {
            "kind": NOTIF_CHAT, "title": payload["sender_name"],
            "body": preview, "thread_id": thread.id,
        })
    return msg, None


def mark_thread_read(thread, user):
    """Mark every message not sent by `user` as read. Returns the count."""
    changed = 0
    for m in thread.messages:
        if m.sender_id != user.id and not m.is_read:
            m.is_read = True
            changed += 1
    if changed:
        db.session.commit()
    return changed
