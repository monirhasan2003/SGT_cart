"""Customer account area — Phase 1: profile view/edit + password change.

Address management is added alongside checkout in a later phase.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app.extensions import db
from app.models.user import Address
from app.models.order import Order
from app.models.marketing import RewardLedger, Referral
from app.services import referral_service
from app.services.recommendation_service import for_you

account = Blueprint("account", __name__)


@account.route("/dashboard/")
@login_required
def dashboard():
    recommended = for_you(current_user, limit=8)
    return render_template("pages/customer-dashboard.html",
                           recommended=recommended)


@account.route("/profile-info/")
@login_required
def profile():
    return render_template("pages/profile-info.html")


@account.route("/profile-info/update", methods=["POST"])
@login_required
def update_profile():
    first = (request.form.get("first_name") or "").strip()
    last = (request.form.get("last_name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    if not first:
        flash("First name is required.", "danger")
    else:
        current_user.name = (first + " " + last).strip()
        current_user.phone = phone
        db.session.commit()
        flash("Profile updated successfully.", "success")
    return redirect(url_for("account.profile"))


@account.route("/profile-info/change-password", methods=["POST"])
@login_required
def change_password():
    current = request.form.get("current_password") or ""
    new = request.form.get("new_password") or ""
    confirm = request.form.get("confirm_password") or ""

    if not current_user.check_password(current):
        flash("Your current password is incorrect.", "danger")
    elif len(new) < 6:
        flash("New password must be at least 6 characters.", "danger")
    elif new != confirm:
        flash("New passwords do not match.", "danger")
    else:
        current_user.set_password(new)
        db.session.commit()
        flash("Password changed successfully.", "success")
    return redirect(url_for("account.profile"))


# --------------------------------------------------------------------------
# delivery addresses
# --------------------------------------------------------------------------
def _own_address_or_404(address_id):
    address = db.session.get(Address, address_id)
    if address is None or address.user_id != current_user.id:
        abort(404)
    return address


def _save_address(address):
    f = request.form
    full_name = (f.get("full_name") or "").strip()
    phone = (f.get("phone") or "").strip()
    address_line = (f.get("address_line") or "").strip()
    city = (f.get("city") or "").strip()

    errors = []
    if not full_name:
        errors.append("Full name is required.")
    if not phone:
        errors.append("Phone number is required.")
    if not address_line:
        errors.append("Address is required.")
    if not city:
        errors.append("City is required.")
    if errors:
        for err in errors:
            flash(err, "danger")
        return render_template("pages/edit-account-address.html", address=address, form=f)

    creating = address is None
    # Count existing addresses BEFORE adding the new row (autoflush would
    # otherwise include it and break the "first address" check).
    existing_count = Address.query.filter_by(user_id=current_user.id).count()
    if creating:
        address = Address(user_id=current_user.id)
        db.session.add(address)

    address.label = (f.get("label") or "").strip()
    address.full_name = full_name
    address.phone = phone
    address.address_line = address_line
    address.area = (f.get("area") or "").strip()
    address.city = city
    address.district = (f.get("district") or "").strip()
    address.postal_code = (f.get("postal_code") or "").strip()
    # Phase 15 D-9 B4 — courier honours this when supported.
    address.prayer_time_delivery = bool(f.get("prayer_time_delivery"))

    make_default = bool(f.get("is_default"))
    if make_default or (creating and existing_count == 0):
        Address.query.filter_by(user_id=current_user.id).update({"is_default": False})
        address.is_default = True

    db.session.commit()
    flash(f"Address {'added' if creating else 'updated'} successfully.", "success")
    return redirect(url_for("account.addresses"))


@account.route("/addresses/")
@login_required
def addresses():
    items = (Address.query.filter_by(user_id=current_user.id)
             .order_by(Address.is_default.desc(), Address.id.desc()).all())
    return render_template("pages/addresses.html", addresses=items)


@account.route("/addresses/new", methods=["GET", "POST"])
@login_required
def address_create():
    if request.method == "POST":
        return _save_address(None)
    return render_template("pages/edit-account-address.html", address=None, form={})


@account.route("/addresses/<int:address_id>/edit", methods=["GET", "POST"])
@login_required
def address_edit(address_id):
    address = _own_address_or_404(address_id)
    if request.method == "POST":
        return _save_address(address)
    return render_template("pages/edit-account-address.html", address=address, form={})


@account.route("/addresses/<int:address_id>/delete", methods=["POST"])
@login_required
def address_delete(address_id):
    address = _own_address_or_404(address_id)
    db.session.delete(address)
    db.session.commit()
    flash("Address deleted.", "info")
    return redirect(url_for("account.addresses"))


@account.route("/addresses/<int:address_id>/default", methods=["POST"])
@login_required
def address_default(address_id):
    address = _own_address_or_404(address_id)
    Address.query.filter_by(user_id=current_user.id).update({"is_default": False})
    address.is_default = True
    db.session.commit()
    flash("Default address updated.", "success")
    return redirect(url_for("account.addresses"))


# --------------------------------------------------------------------------
# orders
# --------------------------------------------------------------------------
@account.route("/my-orders/")
@login_required
def orders():
    items = (Order.query.filter_by(customer_id=current_user.id)
             .order_by(Order.id.desc()).all())
    return render_template("pages/my-orders.html", orders=items)


@account.route("/rewards/")
@login_required
def rewards():
    """Reward-points balance + history."""
    ledger = (
        RewardLedger.query.filter_by(user_id=current_user.id)
        .order_by(RewardLedger.id.desc()).limit(100).all()
    )
    return render_template("pages/rewards.html", ledger=ledger)


@account.route("/refer/")
@login_required
def refer():
    """Refer & Earn — the user's referral code, share link and earnings."""
    stats = referral_service.stats(current_user)
    referrals = (
        Referral.query.filter_by(referrer_id=current_user.id)
        .order_by(Referral.id.desc()).all()
    )
    return render_template("pages/refer.html", stats=stats, referrals=referrals)


@account.route("/my-orders/<order_number>/")
@login_required
def order_detail(order_number):
    order = Order.query.filter_by(
        order_number=order_number, customer_id=current_user.id
    ).first()
    if order is None:
        abort(404)
    return render_template("pages/order-detail.html", order=order)
