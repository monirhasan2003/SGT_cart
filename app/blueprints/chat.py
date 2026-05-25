"""Chat — Phase 8 web views (the two messaging systems).

Triage first: a user picks WHAT they need before a conversation opens, so it
reaches the right side.

  * SGT Support  — purchase / delivery / refund / other  -> the platform
  * Ask a Seller — product questions                     -> that seller

Admins staff the support desk from /admin/messages/.
"""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, abort,
)
from flask_login import login_required, current_user

from app.extensions import db
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Product
from app.models.order import Order, SubOrder
from app.models.chat import (
    ChatThread, CHAT_SUPPORT, SUPPORT_TOPICS, SUPPORT_TOPIC_LABELS,
)
from app.services.chat_service import (
    get_or_create_vendor_thread, get_or_create_support_thread,
    can_access, threads_for, post_message, mark_thread_read,
)
from app.utils.decorators import admin_required

chat = Blueprint("chat", __name__)


def _own_thread_or_404(thread_id):
    thread = db.session.get(ChatThread, thread_id)
    if thread is None or not can_access(current_user, thread):
        abort(404)
    return thread


def _support_thread_or_404(thread_id):
    thread = db.session.get(ChatThread, thread_id)
    if thread is None or thread.kind != CHAT_SUPPORT:
        abort(404)
    return thread


# --------------------------------------------------------------------------
# customer / seller inbox + triage
# --------------------------------------------------------------------------
@chat.route("/messages/")
@login_required
def inbox():
    return render_template("pages/messages.html", threads=threads_for(current_user))


@chat.route("/messages/new")
@login_required
def new_chat():
    """Triage screen — choose the support desk or a seller to talk to."""
    # Sellers the user has ordered from — one-tap "ask a seller" shortcuts.
    seller_ids = [
        row[0] for row in db.session.query(SubOrder.vendor_id)
        .join(Order, SubOrder.order_id == Order.id)
        .filter(Order.customer_id == current_user.id).distinct()
    ]
    vendors = (
        VendorProfile.query.filter(
            VendorProfile.id.in_(seller_ids),
            VendorProfile.status == VENDOR_APPROVED,
        ).all() if seller_ids else []
    )
    orders = (
        Order.query.filter_by(customer_id=current_user.id)
        .order_by(Order.id.desc()).limit(20).all()
    )
    return render_template(
        "pages/chat-new.html", topics=SUPPORT_TOPICS,
        topic_labels=SUPPORT_TOPIC_LABELS, vendors=vendors, orders=orders,
    )


@chat.route("/messages/start/support", methods=["POST"])
@login_required
def start_support():
    topic = (request.form.get("topic") or "").strip()
    if topic not in SUPPORT_TOPICS:
        flash("Please choose what your issue is about.", "danger")
        return redirect(url_for("chat.new_chat"))

    order = None
    order_number = (request.form.get("order_number") or "").strip()
    if order_number:
        order = Order.query.filter_by(
            order_number=order_number, customer_id=current_user.id
        ).first()

    thread = get_or_create_support_thread(current_user, topic, order)
    return redirect(url_for("chat.thread", thread_id=thread.id))


@chat.route("/messages/start/vendor", methods=["POST"])
@login_required
def start_vendor():
    vendor = db.session.get(VendorProfile, request.form.get("vendor_id", type=int))
    if vendor is None or vendor.status != VENDOR_APPROVED:
        flash("Store not found.", "danger")
        return redirect(url_for("chat.new_chat"))
    if (current_user.is_seller and current_user.vendor_profile
            and current_user.vendor_profile.id == vendor.id):
        flash("You cannot start a chat with your own store.", "warning")
        return redirect(url_for("chat.inbox"))

    product = None
    product_id = request.form.get("product_id", type=int)
    if product_id:
        product = db.session.get(Product, product_id)

    thread = get_or_create_vendor_thread(current_user, vendor, product)
    return redirect(url_for("chat.thread", thread_id=thread.id))


@chat.route("/messages/<int:thread_id>/")
@login_required
def thread(thread_id):
    t = _own_thread_or_404(thread_id)
    mark_thread_read(t, current_user)
    return render_template("pages/chat-thread.html", thread=t)


@chat.route("/messages/<int:thread_id>/send", methods=["POST"])
@login_required
def send(thread_id):
    t = _own_thread_or_404(thread_id)
    msg, error = post_message(t, current_user, request.form.get("body"))
    if error:
        flash(error, "danger")
    elif msg.is_flagged:
        flash("Message sent — a phone number was removed. Please keep all "
              "contact and payment on SGT Cart.", "warning")
    return redirect(url_for("chat.thread", thread_id=t.id))


@chat.route("/messages/<int:thread_id>/send-audio", methods=["POST"])
@login_required
def send_audio(thread_id):
    """Upload + post a voice message (Phase 15 D-7 C5)."""
    from app.utils.uploads import save_audio_upload
    t = _own_thread_or_404(thread_id)
    file = request.files.get("audio")
    audio_path = save_audio_upload(file, "chat_audio")
    if audio_path is None:
        flash("Could not save audio — accepted formats: mp3, ogg, wav, "
              "webm, m4a, up to 5 MB.", "danger")
        return redirect(url_for("chat.thread", thread_id=t.id))
    # Body can be left blank — `post_message` substitutes a placeholder
    # whenever audio_path is present.
    msg, error = post_message(t, current_user, "", audio_path=audio_path)
    if error:
        flash(error, "danger")
    return redirect(url_for("chat.thread", thread_id=t.id))


@chat.route("/messages/quick-question", methods=["POST"])
@login_required
def quick_question():
    """One-tap pre-set question from the product page (Phase 15 D-7 C4)."""
    from app.services.quick_questions import question_body
    vendor = db.session.get(VendorProfile, request.form.get("vendor_id", type=int))
    if vendor is None or vendor.status != VENDOR_APPROVED:
        flash("Store not found.", "danger")
        return redirect(request.referrer or url_for("chat.new_chat"))
    if (current_user.is_seller and current_user.vendor_profile
            and current_user.vendor_profile.id == vendor.id):
        flash("You cannot chat with your own store.", "warning")
        return redirect(url_for("chat.inbox"))

    body = question_body((request.form.get("question_key") or "").strip())
    if body is None:
        flash("Unknown quick question.", "danger")
        return redirect(request.referrer or url_for("chat.new_chat"))

    product = None
    product_id = request.form.get("product_id", type=int)
    if product_id:
        product = db.session.get(Product, product_id)

    thread = get_or_create_vendor_thread(current_user, vendor, product)
    _, error = post_message(thread, current_user, body)
    if error:
        flash(error, "danger")
    return redirect(url_for("chat.thread", thread_id=thread.id))


# --------------------------------------------------------------------------
# admin support desk
# --------------------------------------------------------------------------
@chat.route("/admin/messages/")
@admin_required
def admin_inbox():
    threads = (
        ChatThread.query.filter_by(kind=CHAT_SUPPORT)
        .order_by(ChatThread.last_message_at.desc()).all()
    )
    return render_template("admin/messages.html", threads=threads)


@chat.route("/admin/messages/<int:thread_id>/")
@admin_required
def admin_thread(thread_id):
    t = _support_thread_or_404(thread_id)
    mark_thread_read(t, current_user)
    return render_template("admin/chat_thread.html", thread=t)


@chat.route("/admin/messages/<int:thread_id>/send", methods=["POST"])
@admin_required
def admin_send(thread_id):
    t = _support_thread_or_404(thread_id)
    _, error = post_message(t, current_user, request.form.get("body"))
    if error:
        flash(error, "danger")
    return redirect(url_for("chat.admin_thread", thread_id=t.id))
