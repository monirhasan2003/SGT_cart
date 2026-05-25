"""In-app notifications — Phase 8 web views.

A `Notification` feed shared by customers, sellers and admins. The unread
count is injected into every page (navbar bell); live updates arrive over
SocketIO (see Base/base.html).
"""
from flask import (
    Blueprint, render_template, redirect, url_for, abort, has_request_context,
)
from flask_login import login_required, current_user

from app.extensions import db
from app.models.notification import Notification
from app.services.notification_service import mark_all_read, unread_count

notification = Blueprint("notification", __name__)


@notification.app_context_processor
def inject_notifications():
    """Unread count for the navbar bell, on every page."""
    if has_request_context() and current_user.is_authenticated:
        return {"nav_unread_notifications": unread_count(current_user.id)}
    return {"nav_unread_notifications": 0}


@notification.route("/notifications/")
@login_required
def inbox():
    items = (
        Notification.query.filter_by(user_id=current_user.id)
        .order_by(Notification.id.desc()).limit(100).all()
    )
    return render_template("pages/notifications.html", notifications=items)


@notification.route("/notifications/read-all", methods=["POST"])
@login_required
def read_all():
    mark_all_read(current_user.id)
    return redirect(url_for("notification.inbox"))


@notification.route("/notifications/<int:notification_id>/go")
@login_required
def go(notification_id):
    """Mark a notification read, then jump to whatever it points at."""
    note = db.session.get(Notification, notification_id)
    if note is None or note.user_id != current_user.id:
        abort(404)
    if not note.is_read:
        note.is_read = True
        db.session.commit()
    return redirect(note.url or url_for("notification.inbox"))
