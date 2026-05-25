"""API v1 — chat (the two messaging systems).

Customers and sellers both use these endpoints; admins handle support chat
from the web admin panel. New messages arrive live over SocketIO; the app
opens a socket and emits `join_thread` to receive them.
"""
from flask import request, jsonify

from app.extensions import db
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Product
from app.models.order import Order
from app.models.chat import ChatThread, SUPPORT_TOPICS, SUPPORT_TOPIC_LABELS
from app.services.chat_service import (
    get_or_create_vendor_thread, get_or_create_support_thread,
    can_access, threads_for, post_message, mark_thread_read,
    thread_json, message_json,
)
from .helpers import err, current_api_user, role_required
from . import api_v1

# Both customers and sellers chat; admins are not served by the app API.
chat_user_required = role_required("customer", "seller")


@api_v1.route("/chat/threads", methods=["GET"])
@chat_user_required
def list_threads():
    user = current_api_user()
    return jsonify({"threads": [thread_json(t, user) for t in threads_for(user)]})


@api_v1.route("/chat/threads/vendor", methods=["POST"])
@chat_user_required
def start_vendor_thread():
    """Open (or fetch) the customer<->seller thread. Body: {vendor_slug, product_slug?}."""
    user = current_api_user()
    data = request.get_json(silent=True) or {}

    vendor = None
    if data.get("vendor_slug"):
        vendor = VendorProfile.query.filter_by(
            slug=data["vendor_slug"], status=VENDOR_APPROVED
        ).first()
    elif data.get("vendor_id"):
        vendor = db.session.get(VendorProfile, data["vendor_id"])
    if vendor is None or vendor.status != VENDOR_APPROVED:
        return err("Store not found.", 404)
    if user.is_seller and user.vendor_profile and user.vendor_profile.id == vendor.id:
        return err("You cannot start a chat with your own store.", 400)

    product = None
    if data.get("product_slug"):
        product = Product.query.filter_by(slug=data["product_slug"]).first()

    thread = get_or_create_vendor_thread(user, vendor, product)
    return jsonify({"thread": thread_json(thread, user, with_messages=True)}), 201


@api_v1.route("/chat/support/topics", methods=["GET"])
@chat_user_required
def support_topics():
    """The triage choices shown before a support chat opens."""
    return jsonify({"topics": [
        {"topic": t, "label": SUPPORT_TOPIC_LABELS[t]} for t in SUPPORT_TOPICS
    ]})


@api_v1.route("/chat/threads/support", methods=["POST"])
@chat_user_required
def start_support_thread():
    """Open (or fetch) a triaged customer<->platform support thread.

    Body: {topic: purchase|delivery|refund|other, order_number?}.
    """
    user = current_api_user()
    data = request.get_json(silent=True) or {}

    topic = (data.get("topic") or "").strip()
    if topic not in SUPPORT_TOPICS:
        return err("topic must be one of: " + ", ".join(SUPPORT_TOPICS) + ".")

    order = None
    if data.get("order_number"):
        order = Order.query.filter_by(
            order_number=data["order_number"], customer_id=user.id
        ).first()
        if order is None:
            return err("Order not found.", 404)

    thread = get_or_create_support_thread(user, topic, order)
    return jsonify({"thread": thread_json(thread, user, with_messages=True)}), 201


@api_v1.route("/chat/threads/<int:thread_id>", methods=["GET"])
@chat_user_required
def get_thread(thread_id):
    user = current_api_user()
    thread = db.session.get(ChatThread, thread_id)
    if not can_access(user, thread):
        return err("Thread not found.", 404)
    mark_thread_read(thread, user)
    return jsonify({"thread": thread_json(thread, user, with_messages=True)})


@api_v1.route("/chat/threads/<int:thread_id>/messages", methods=["POST"])
@chat_user_required
def send_message(thread_id):
    user = current_api_user()
    thread = db.session.get(ChatThread, thread_id)
    if not can_access(user, thread):
        return err("Thread not found.", 404)

    body = (request.get_json(silent=True) or {}).get("body")
    msg, error = post_message(thread, user, body)
    if error:
        return err(error)
    return jsonify({"message": message_json(msg)}), 201


@api_v1.route("/chat/threads/<int:thread_id>/read", methods=["POST"])
@chat_user_required
def mark_read(thread_id):
    user = current_api_user()
    thread = db.session.get(ChatThread, thread_id)
    if not can_access(user, thread):
        return err("Thread not found.", 404)
    count = mark_thread_read(thread, user)
    return jsonify({"marked_read": count})
