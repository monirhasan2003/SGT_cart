"""Admin panel — Phase 1.

User management, vendor approval and "log in as user" impersonation.
Every view is admin-only.
"""
from datetime import datetime
from decimal import Decimal

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, abort,
)
from flask_login import login_user, current_user

from slugify import slugify

from app.extensions import db
from app.models.user import User, ROLE_CUSTOMER, ROLE_SELLER, ROLE_ADMIN
from app.models.vendor import (
    VendorProfile, VENDOR_PENDING, VENDOR_APPROVED, VENDOR_SUSPENDED,
)
from app.models.catalog import (
    Category, Product, PRODUCT_PUBLISHED, PRODUCT_REJECTED, PRODUCT_STATUSES,
)
from sqlalchemy import func

from app.models.order import Order, SubOrder
from app.models.wallet import (
    VendorWallet, PayoutRequest,
    PAYOUT_REQUESTED, PAYOUT_APPROVED, PAYOUT_REJECTED, PAYOUT_STATUSES,
)
from app.models.setting import AuditLog
from app.models.notification import NOTIF_PRODUCT, NOTIF_PAYOUT, NOTIF_SYSTEM
from app.models.policy import PolicyViolation, SURFACES
from app.models.marketing import (
    Coupon, COUPON_PLATFORM, FlashSale, FlashSaleItem, AbandonedCart,
)
from app.models.banner import HomepageBanner, BANNER_KINDS, BANNER_HERO
from app.services.wallet_service import refund_payout
from app.services.settings_service import all_settings, set_setting, log_action
from app.services.notification_service import notify
from app.services.coupon_service import parse_coupon_form, coupon_form_dict
from app.services import flash_sale_service, abandoned_cart_service, policy_service
from app.services.payout_service import process_due_payouts
from app.services.analytics_service import platform_metrics
from app.utils.decorators import admin_required
from app.utils.uploads import save_upload

admin = Blueprint("admin", __name__, url_prefix="/admin")


# --------------------------------------------------------------------------
# admin login  (separate from the customer/seller login)
# --------------------------------------------------------------------------
@admin.route("/login", methods=["GET", "POST"])
def login():
    """Dedicated admin sign-in. Admins log in with password only (no OTP)."""
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""
        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash("Invalid email or password.", "danger")
        elif not user.is_admin:
            flash("This is not an admin account.", "danger")
        elif not user.is_active:
            flash("This account is disabled.", "danger")
        else:
            login_user(user)
            user.last_login_at = datetime.utcnow()
            db.session.commit()
            flash("Welcome back!", "success")
            return redirect(url_for("admin.dashboard"))

    return render_template("admin/login.html")


# --------------------------------------------------------------------------
# dashboard
# --------------------------------------------------------------------------
@admin.route("/")
@admin_required
def dashboard():
    stats = {
        "total_users": User.query.count(),
        "customers": User.query.filter_by(role=ROLE_CUSTOMER).count(),
        "sellers": User.query.filter_by(role=ROLE_SELLER).count(),
        "pending_vendors": VendorProfile.query.filter_by(status=VENDOR_PENDING).count(),
        "total_products": Product.query.count(),
        "total_orders": Order.query.count(),
        "pending_payouts": PayoutRequest.query.filter_by(status=PAYOUT_REQUESTED).count(),
        "total_sales": db.session.query(
            func.coalesce(func.sum(Order.total_amount), 0)).scalar(),
        "commission_earned": db.session.query(
            func.coalesce(func.sum(SubOrder.commission_amount), 0)).scalar(),
    }
    top_sellers = (
        VendorWallet.query.filter(VendorWallet.total_earned > 0)
        .order_by(VendorWallet.total_earned.desc()).limit(5).all()
    )
    recent_orders = Order.query.order_by(Order.id.desc()).limit(8).all()
    pending = (
        VendorProfile.query.filter_by(status=VENDOR_PENDING)
        .order_by(VendorProfile.id.desc()).limit(6).all()
    )
    return render_template(
        "admin/dashboard.html", stats=stats, top_sellers=top_sellers,
        recent_orders=recent_orders, pending=pending,
    )


# --------------------------------------------------------------------------
# users
# --------------------------------------------------------------------------
@admin.route("/users/")
@admin_required
def users():
    role = request.args.get("role", "")
    q = (request.args.get("q") or "").strip()
    query = User.query
    if role in (ROLE_CUSTOMER, ROLE_SELLER, ROLE_ADMIN):
        query = query.filter_by(role=role)
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(User.name.ilike(like), User.email.ilike(like)))
    user_list = query.order_by(User.id.desc()).all()
    return render_template("admin/users.html", users=user_list, role=role, q=q)


@admin.route("/users/<int:user_id>/")
@admin_required
def user_detail(user_id):
    user = db.session.get(User, user_id) or abort(404)
    return render_template("admin/user_detail.html", user=user)


@admin.route("/users/<int:user_id>/toggle-active", methods=["POST"])
@admin_required
def toggle_active(user_id):
    user = db.session.get(User, user_id) or abort(404)
    if user.id == current_user.id:
        flash("You cannot disable your own account.", "danger")
    else:
        user.is_active = not user.is_active
        db.session.commit()
        state = "active" if user.is_active else "disabled"
        flash(f"{user.name} is now {state}.", "success")
    return redirect(request.referrer or url_for("admin.users"))


@admin.route("/users/<int:user_id>/login-as")
@admin_required
def login_as(user_id):
    """Impersonate a customer/seller — view the platform as that user."""
    user = db.session.get(User, user_id) or abort(404)
    if user.is_admin:
        flash("You cannot impersonate another admin.", "danger")
        return redirect(url_for("admin.user_detail", user_id=user_id))
    session["impersonator_id"] = current_user.id
    login_user(user)
    flash(f"You are now viewing the platform as {user.name}.", "info")
    return redirect(url_for("main.index"))


@admin.route("/stop-impersonating")
def stop_impersonating():
    """Return from an impersonated session back to the admin account."""
    admin_id = session.pop("impersonator_id", None)
    if not admin_id:
        return redirect(url_for("main.index"))
    admin_user = db.session.get(User, admin_id)
    if admin_user and admin_user.is_admin:
        login_user(admin_user)
        flash("Returned to your admin account.", "info")
        return redirect(url_for("admin.dashboard"))
    return redirect(url_for("main.index"))


# --------------------------------------------------------------------------
# vendors
# --------------------------------------------------------------------------
@admin.route("/vendors/")
@admin_required
def vendors():
    status = request.args.get("status", "")
    query = VendorProfile.query
    if status in (VENDOR_PENDING, VENDOR_APPROVED, VENDOR_SUSPENDED):
        query = query.filter_by(status=status)
    vendor_list = query.order_by(VendorProfile.id.desc()).all()
    return render_template("admin/vendors.html", vendors=vendor_list, status=status)


@admin.route("/vendors/<int:vendor_id>/")
@admin_required
def vendor_detail(vendor_id):
    vendor = db.session.get(VendorProfile, vendor_id) or abort(404)
    violation_count = policy_service.vendor_violation_count(vendor)
    last_violation = policy_service.last_violation_at(vendor.user_id)
    return render_template(
        "admin/vendor_detail.html", vendor=vendor,
        violation_count=violation_count, last_violation=last_violation,
    )


@admin.route("/vendors/<int:vendor_id>/approve", methods=["POST"])
@admin_required
def approve_vendor(vendor_id):
    vendor = db.session.get(VendorProfile, vendor_id) or abort(404)
    if not vendor.is_verification_submitted:
        flash(
            "Cannot approve — the seller has not submitted verification documents yet.",
            "danger",
        )
        return redirect(request.referrer or url_for("admin.vendors"))
    vendor.status = VENDOR_APPROVED
    vendor.approved_at = datetime.utcnow()
    log_action("Approved vendor", vendor.shop_name_en)
    notify(vendor.user_id, NOTIF_SYSTEM, "Your shop is approved!",
           "You can now list products and start selling on SGT Cart.",
           url="/seller/")
    db.session.commit()
    flash(f"Vendor '{vendor.shop_name_en}' approved.", "success")
    return redirect(request.referrer or url_for("admin.vendors"))


@admin.route("/vendors/<int:vendor_id>/ranking", methods=["POST"])
@admin_required
def vendor_ranking(vendor_id):
    """Override a seller's search-ranking boost (Phase 10)."""
    vendor = db.session.get(VendorProfile, vendor_id) or abort(404)
    try:
        boost = Decimal((request.form.get("ranking_boost") or "0").strip())
    except Exception:  # noqa: BLE001
        boost = Decimal("0")
    boost = max(Decimal("-5"), min(Decimal("5"), boost))   # clamp
    vendor.ranking_boost = boost
    log_action("Set ranking boost", f"{vendor.shop_name_en} -> {boost}")
    db.session.commit()
    flash(f"Ranking boost for '{vendor.shop_name_en}' set to {boost}.", "success")
    return redirect(url_for("admin.vendor_detail", vendor_id=vendor.id))


@admin.route("/vendors/<int:vendor_id>/suspend", methods=["POST"])
@admin_required
def suspend_vendor(vendor_id):
    vendor = db.session.get(VendorProfile, vendor_id) or abort(404)
    vendor.status = VENDOR_SUSPENDED
    log_action("Suspended vendor", vendor.shop_name_en)
    notify(vendor.user_id, NOTIF_SYSTEM, "Your shop has been suspended",
           "Please contact SGT Support for details.", url="/messages/new")
    db.session.commit()
    flash(f"Vendor '{vendor.shop_name_en}' suspended.", "warning")
    return redirect(request.referrer or url_for("admin.vendors"))


@admin.route("/vendors/<int:vendor_id>/unsuspend", methods=["POST"])
@admin_required
def unsuspend_vendor(vendor_id):
    """Reinstate a suspended vendor (Phase 15 Chunk D-0 admin override)."""
    vendor = db.session.get(VendorProfile, vendor_id) or abort(404)
    if vendor.status != VENDOR_SUSPENDED:
        flash("This vendor is not suspended.", "info")
        return redirect(request.referrer or url_for("admin.vendor_detail",
                                                    vendor_id=vendor.id))
    vendor.status = VENDOR_APPROVED
    log_action("Unsuspended vendor", vendor.shop_name_en)
    notify(vendor.user_id, NOTIF_SYSTEM, "Your shop has been reinstated",
           "An admin has unsuspended your shop. You can sell again — please "
           "review our anti-disintermediation policy to avoid future issues.",
           url="/seller/")
    db.session.commit()
    flash(f"Vendor '{vendor.shop_name_en}' unsuspended.", "success")
    return redirect(request.referrer or url_for("admin.vendor_detail",
                                                vendor_id=vendor.id))


# --------------------------------------------------------------------------
# policy violations (Phase 15 Chunk D-0)
# --------------------------------------------------------------------------
@admin.route("/policy-violations/")
@admin_required
def policy_violations():
    """Browse every redaction event logged by `policy_service`."""
    surface = request.args.get("surface", "")
    query = PolicyViolation.query
    if surface in SURFACES:
        query = query.filter_by(surface=surface)
    page = request.args.get("page", 1, type=int)
    pagination = (
        query.order_by(PolicyViolation.id.desc())
        .paginate(page=page, per_page=30, error_out=False)
    )
    return render_template(
        "admin/policy_violations.html",
        pagination=pagination, violations=pagination.items,
        surface=surface, surfaces=SURFACES,
    )


# --------------------------------------------------------------------------
# categories
# --------------------------------------------------------------------------
def _unique_category_slug(name, exclude_id=None):
    base = slugify(name) or "category"
    slug, i = base, 2
    while True:
        existing = Category.query.filter_by(slug=slug).first()
        if existing is None or existing.id == exclude_id:
            return slug
        slug = f"{base}-{i}"
        i += 1


def _category_parents(exclude_id=None):
    """Top-level categories usable as a parent (sub-categories nest one level)."""
    query = Category.query.filter(Category.parent_id.is_(None))
    if exclude_id is not None:
        query = query.filter(Category.id != exclude_id)
    return query.order_by(Category.name_en).all()


@admin.route("/categories/")
@admin_required
def categories():
    roots = (
        Category.query.filter_by(parent_id=None)
        .order_by(Category.sort_order, Category.name_en).all()
    )
    return render_template("admin/categories.html", roots=roots)


@admin.route("/categories/create", methods=["GET", "POST"])
@admin_required
def category_create():
    if request.method == "POST":
        return _save_category(None)
    return render_template(
        "admin/category_form.html", category=None, parents=_category_parents(), form={}
    )


@admin.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@admin_required
def category_edit(category_id):
    category = db.session.get(Category, category_id) or abort(404)
    if request.method == "POST":
        return _save_category(category)
    return render_template(
        "admin/category_form.html", category=category,
        parents=_category_parents(exclude_id=category_id), form={},
    )


def _save_category(category):
    name_en = (request.form.get("name_en") or "").strip()
    name_bn = (request.form.get("name_bn") or "").strip()
    parent_raw = request.form.get("parent_id") or ""
    sort_raw = request.form.get("sort_order") or "0"
    is_active = bool(request.form.get("is_active"))

    if not name_en:
        flash("English name is required.", "danger")
        exclude = category.id if category else None
        return render_template(
            "admin/category_form.html", category=category,
            parents=_category_parents(exclude_id=exclude), form=request.form,
        )

    parent_id = int(parent_raw) if parent_raw.isdigit() else None
    sort_order = int(sort_raw) if sort_raw.lstrip("-").isdigit() else 0

    creating = category is None
    if creating:
        category = Category(slug=_unique_category_slug(name_en))
        db.session.add(category)

    category.name_en = name_en
    category.name_bn = name_bn
    category.parent_id = parent_id
    category.sort_order = sort_order
    category.is_active = is_active

    image_path = save_upload(request.files.get("image"), "categories")
    if image_path:
        category.image = image_path

    db.session.commit()
    flash(f"Category '{name_en}' {'created' if creating else 'updated'}.", "success")
    return redirect(url_for("admin.categories"))


@admin.route("/categories/<int:category_id>/delete", methods=["POST"])
@admin_required
def category_delete(category_id):
    category = db.session.get(Category, category_id) or abort(404)
    if category.children:
        flash("Cannot delete — this category has sub-categories.", "danger")
    elif category.products:
        flash("Cannot delete — products are assigned to this category.", "danger")
    else:
        db.session.delete(category)
        db.session.commit()
        flash("Category deleted.", "success")
    return redirect(url_for("admin.categories"))


# --------------------------------------------------------------------------
# product review
# --------------------------------------------------------------------------
@admin.route("/products/")
@admin_required
def products():
    status = request.args.get("status", "")
    query = Product.query
    if status in PRODUCT_STATUSES:
        query = query.filter_by(status=status)
    items = query.order_by(Product.id.desc()).all()
    pending_count = Product.query.filter_by(status="pending").count()
    return render_template("admin/products.html", products=items, status=status,
                           pending_count=pending_count)


@admin.route("/products/<int:product_id>/approve", methods=["POST"])
@admin_required
def approve_product(product_id):
    product = db.session.get(Product, product_id) or abort(404)
    product.status = PRODUCT_PUBLISHED
    log_action("Published product", product.title_en)
    if product.vendor:
        notify(product.vendor.user_id, NOTIF_PRODUCT, "Product published",
               f"'{product.title_en}' is now live on the storefront.",
               url=f"/product/{product.slug}/")
    db.session.commit()
    flash(f"Product '{product.title_en}' published.", "success")
    return redirect(request.referrer or url_for("admin.products"))


@admin.route("/products/<int:product_id>/reject", methods=["POST"])
@admin_required
def reject_product(product_id):
    product = db.session.get(Product, product_id) or abort(404)
    product.status = PRODUCT_REJECTED
    log_action("Rejected product", product.title_en)
    if product.vendor:
        notify(product.vendor.user_id, NOTIF_PRODUCT, "Product needs changes",
               f"'{product.title_en}' was not approved. Please review and resubmit.",
               url=f"/seller/products/{product.id}/edit")
    db.session.commit()
    flash(f"Product '{product.title_en}' rejected.", "warning")
    return redirect(request.referrer or url_for("admin.products"))


# --------------------------------------------------------------------------
# sponsored / paid promotion (Phase 15 v3c)
# --------------------------------------------------------------------------
@admin.route("/sponsored/")
@admin_required
def sponsored():
    """List published products with their Sponsored status + active window."""
    q = (request.args.get("q") or "").strip()
    query = Product.query.filter_by(status=PRODUCT_PUBLISHED)
    if q:
        like = f"%{q}%"
        query = query.filter(Product.title_en.ilike(like))
    items = (query.order_by(Product.is_sponsored.desc(),
                            Product.id.desc()).limit(200).all())
    active_count = Product.query.filter(
        Product.is_sponsored.is_(True),
        db.or_(Product.sponsored_until.is_(None),
               Product.sponsored_until >= datetime.utcnow()),
    ).count()
    return render_template("admin/sponsored.html", products=items, q=q,
                           active_count=active_count, now=datetime.utcnow())


@admin.route("/sponsored/<int:product_id>", methods=["POST"])
@admin_required
def sponsored_update(product_id):
    product = db.session.get(Product, product_id) or abort(404)
    action = request.form.get("action", "")
    if action == "disable":
        product.is_sponsored = False
        product.sponsored_until = None
        log_action("Disabled sponsored promo", product.title_en)
        flash(f"'{product.title_en}' is no longer sponsored.", "info")
    else:
        until_raw = (request.form.get("sponsored_until") or "").strip()
        until = None
        if until_raw:
            try:
                until = datetime.strptime(until_raw, "%Y-%m-%d")
            except ValueError:
                flash("Invalid end date — leave blank for no expiry.", "danger")
                return redirect(url_for("admin.sponsored"))
        product.is_sponsored = True
        product.sponsored_until = until
        log_action("Marked product sponsored", product.title_en)
        if product.vendor:
            notify(product.vendor.user_id, NOTIF_PRODUCT,
                   "Your product is now Sponsored",
                   f"Admin promoted '{product.title_en}' — it surfaces above "
                   "regular results in search and the homepage.",
                   url=f"/product/{product.slug}/")
        flash(f"'{product.title_en}' marked sponsored.", "success")
    db.session.commit()
    return redirect(url_for("admin.sponsored", q=request.args.get("q", "")))


# --------------------------------------------------------------------------
# orders
# --------------------------------------------------------------------------
@admin.route("/orders/")
@admin_required
def orders():
    page = request.args.get("page", 1, type=int)
    pagination = (
        Order.query.order_by(Order.id.desc())
        .paginate(page=page, per_page=20, error_out=False)
    )
    return render_template("admin/orders.html",
                           pagination=pagination, orders=pagination.items)


@admin.route("/orders/<order_number>/")
@admin_required
def order_detail(order_number):
    order = Order.query.filter_by(order_number=order_number).first() or abort(404)
    return render_template("admin/order_detail.html", order=order)


# --------------------------------------------------------------------------
# payouts
# --------------------------------------------------------------------------
@admin.route("/payouts/")
@admin_required
def payouts():
    status = request.args.get("status", "")
    query = PayoutRequest.query
    if status in PAYOUT_STATUSES:
        query = query.filter_by(status=status)
    items = query.order_by(PayoutRequest.id.desc()).all()
    pending_count = PayoutRequest.query.filter_by(status=PAYOUT_REQUESTED).count()
    return render_template("admin/payouts.html", payouts=items, status=status,
                           pending_count=pending_count)


@admin.route("/payouts/run-scheduled", methods=["POST"])
@admin_required
def run_scheduled_payouts():
    """Auto-approve every payout request older than the configured grace period."""
    approved = process_due_payouts()
    flash(f"Scheduled payouts run — {approved} payout(s) auto-approved.", "info")
    return redirect(url_for("admin.payouts"))


@admin.route("/reports/")
@admin_required
def reports():
    """Marketplace-wide sales reports (Phase 11)."""
    days = max(7, min(365, request.args.get("days", 30, type=int) or 30))
    metrics = platform_metrics(days=days)
    return render_template("admin/reports.html", metrics=metrics, days=days)


@admin.route("/payouts/<int:payout_id>/approve", methods=["POST"])
@admin_required
def approve_payout(payout_id):
    p = db.session.get(PayoutRequest, payout_id) or abort(404)
    if p.status == PAYOUT_REQUESTED:
        p.status = PAYOUT_APPROVED
        p.processed_at = datetime.utcnow()
        log_action("Approved payout",
                   f"{p.vendor.shop_name_en if p.vendor else '?'} — Tk {p.amount}")
        if p.vendor:
            notify(p.vendor.user_id, NOTIF_PAYOUT, "Payout approved",
                   f"Your payout of Tk {p.amount} has been approved.",
                   url="/seller/earnings/")
        db.session.commit()
        flash(f"Payout of Tk {p.amount} approved.", "success")
    return redirect(request.referrer or url_for("admin.payouts"))


@admin.route("/payouts/<int:payout_id>/reject", methods=["POST"])
@admin_required
def reject_payout(payout_id):
    p = db.session.get(PayoutRequest, payout_id) or abort(404)
    if p.status == PAYOUT_REQUESTED:
        p.status = PAYOUT_REJECTED
        p.processed_at = datetime.utcnow()
        p.admin_note = (request.form.get("note") or "").strip() or None
        refund_payout(p.vendor_id, p.amount)
        log_action("Rejected payout",
                   f"{p.vendor.shop_name_en if p.vendor else '?'} — Tk {p.amount}")
        if p.vendor:
            notify(p.vendor.user_id, NOTIF_PAYOUT, "Payout rejected",
                   f"Your payout of Tk {p.amount} was rejected — the amount is "
                   "back in your available balance.", url="/seller/earnings/")
        db.session.commit()
        flash("Payout rejected — amount returned to the vendor's balance.", "warning")
    return redirect(request.referrer or url_for("admin.payouts"))


# --------------------------------------------------------------------------
# coupons (platform-wide)
# --------------------------------------------------------------------------
@admin.route("/coupons/")
@admin_required
def coupons():
    items = (Coupon.query.filter_by(scope=COUPON_PLATFORM)
             .order_by(Coupon.id.desc()).all())
    return render_template("admin/coupons.html", coupons=items)


@admin.route("/coupons/new", methods=["GET", "POST"])
@admin_required
def coupon_create():
    if request.method == "POST":
        data, errors = parse_coupon_form(request.form)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("admin/coupon_form.html",
                                   form=request.form, coupon=None)
        coupon = Coupon(scope=COUPON_PLATFORM, **data)
        db.session.add(coupon)
        log_action("Created coupon", coupon.code)
        db.session.commit()
        flash(f"Coupon '{coupon.code}' created.", "success")
        return redirect(url_for("admin.coupons"))
    return render_template("admin/coupon_form.html", form={}, coupon=None)


@admin.route("/coupons/<int:coupon_id>/edit", methods=["GET", "POST"])
@admin_required
def coupon_edit(coupon_id):
    coupon = db.session.get(Coupon, coupon_id) or abort(404)
    if coupon.scope != COUPON_PLATFORM:
        abort(404)
    if request.method == "POST":
        data, errors = parse_coupon_form(request.form, existing=coupon)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("admin/coupon_form.html",
                                   form=request.form, coupon=coupon)
        for key, value in data.items():
            setattr(coupon, key, value)
        log_action("Updated coupon", coupon.code)
        db.session.commit()
        flash("Coupon updated.", "success")
        return redirect(url_for("admin.coupons"))
    return render_template("admin/coupon_form.html",
                           form=coupon_form_dict(coupon), coupon=coupon)


@admin.route("/coupons/<int:coupon_id>/delete", methods=["POST"])
@admin_required
def coupon_delete(coupon_id):
    coupon = db.session.get(Coupon, coupon_id) or abort(404)
    if coupon.scope != COUPON_PLATFORM:
        abort(404)
    log_action("Deleted coupon", coupon.code)
    db.session.delete(coupon)
    db.session.commit()
    flash("Coupon deleted.", "info")
    return redirect(url_for("admin.coupons"))


# --------------------------------------------------------------------------
# flash sales
# --------------------------------------------------------------------------
def _unique_flash_slug(title):
    base = slugify(title) or "flash-sale"
    slug, i = base, 2
    while FlashSale.query.filter_by(slug=slug).first() is not None:
        slug = f"{base}-{i}"
        i += 1
    return slug


def _parse_dt(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


@admin.route("/flash-sales/")
@admin_required
def flash_sales():
    sales = FlashSale.query.order_by(FlashSale.id.desc()).all()
    return render_template("admin/flash_sales.html", sales=sales)


@admin.route("/flash-sales/new", methods=["POST"])
@admin_required
def flash_sale_create():
    title = (request.form.get("title") or "").strip()
    if not title:
        flash("A flash sale title is required.", "danger")
        return redirect(url_for("admin.flash_sales"))
    sale = FlashSale(
        title=title, slug=_unique_flash_slug(title),
        description=(request.form.get("description") or "").strip() or None,
        starts_at=_parse_dt(request.form.get("starts_at")),
        ends_at=_parse_dt(request.form.get("ends_at")),
    )
    db.session.add(sale)
    log_action("Created flash sale", title)
    db.session.commit()
    flash("Flash sale created — add products to it.", "success")
    return redirect(url_for("admin.flash_sale_detail", sale_id=sale.id))


@admin.route("/flash-sales/<int:sale_id>/")
@admin_required
def flash_sale_detail(sale_id):
    sale = db.session.get(FlashSale, sale_id) or abort(404)
    products = (Product.query.filter_by(status=PRODUCT_PUBLISHED)
                .order_by(Product.title_en).all())
    return render_template("admin/flash_sale_detail.html",
                           sale=sale, products=products)


@admin.route("/flash-sales/<int:sale_id>/items", methods=["POST"])
@admin_required
def flash_sale_add_item(sale_id):
    sale = db.session.get(FlashSale, sale_id) or abort(404)
    product = db.session.get(Product, request.form.get("product_id", type=int))
    try:
        price = Decimal((request.form.get("flash_price") or "0").strip())
    except Exception:  # noqa: BLE001
        price = Decimal("0")

    if product is None:
        flash("Please choose a product.", "danger")
    elif price <= 0:
        flash("Enter a valid flash price.", "danger")
    elif any(it.product_id == product.id for it in sale.items):
        flash("That product is already in this sale.", "warning")
    elif flash_sale_service.product_on_active_sale(product.id, exclude_sale_id=sale.id):
        flash("That product is already on another active flash sale.", "danger")
    else:
        flash_sale_service.add_item(sale, product, price)
        db.session.commit()
        flash("Product added to the flash sale.", "success")
    return redirect(url_for("admin.flash_sale_detail", sale_id=sale.id))


@admin.route("/flash-sales/items/<int:item_id>/delete", methods=["POST"])
@admin_required
def flash_sale_remove_item(item_id):
    item = db.session.get(FlashSaleItem, item_id) or abort(404)
    sale_id = item.flash_sale_id
    flash_sale_service.remove_item(item)
    db.session.commit()
    flash("Product removed from the flash sale.", "info")
    return redirect(url_for("admin.flash_sale_detail", sale_id=sale_id))


@admin.route("/flash-sales/<int:sale_id>/activate", methods=["POST"])
@admin_required
def flash_sale_activate(sale_id):
    sale = db.session.get(FlashSale, sale_id) or abort(404)
    clash = [it for it in sale.items
             if flash_sale_service.product_on_active_sale(it.product_id,
                                                          exclude_sale_id=sale.id)]
    if clash:
        flash("Some products are already on another active flash sale.", "danger")
    else:
        flash_sale_service.activate(sale)
        log_action("Activated flash sale", sale.title)
        db.session.commit()
        flash("Flash sale is live — discounted prices applied.", "success")
    return redirect(url_for("admin.flash_sale_detail", sale_id=sale.id))


@admin.route("/flash-sales/<int:sale_id>/deactivate", methods=["POST"])
@admin_required
def flash_sale_deactivate(sale_id):
    sale = db.session.get(FlashSale, sale_id) or abort(404)
    flash_sale_service.deactivate(sale)
    log_action("Ended flash sale", sale.title)
    db.session.commit()
    flash("Flash sale ended — original prices restored.", "info")
    return redirect(url_for("admin.flash_sale_detail", sale_id=sale.id))


@admin.route("/flash-sales/<int:sale_id>/delete", methods=["POST"])
@admin_required
def flash_sale_delete(sale_id):
    sale = db.session.get(FlashSale, sale_id) or abort(404)
    if sale.is_active:
        flash_sale_service.deactivate(sale)   # restore prices before removal
    log_action("Deleted flash sale", sale.title)
    db.session.delete(sale)
    db.session.commit()
    flash("Flash sale deleted.", "info")
    return redirect(url_for("admin.flash_sales"))


# --------------------------------------------------------------------------
# abandoned carts
# --------------------------------------------------------------------------
@admin.route("/abandoned-carts/")
@admin_required
def abandoned_carts():
    carts = (AbandonedCart.query
             .order_by(AbandonedCart.detected_at.desc()).all())
    return render_template("admin/abandoned_carts.html", carts=carts)


@admin.route("/abandoned-carts/scan", methods=["POST"])
@admin_required
def abandoned_carts_scan():
    detected, sent = abandoned_cart_service.scan()
    log_action("Ran abandoned-cart scan", f"{detected} found, {sent} emailed")
    flash(f"Scan complete — {detected} abandoned cart(s), "
          f"{sent} reminder email(s) sent.", "info")
    return redirect(url_for("admin.abandoned_carts"))


# --------------------------------------------------------------------------
# homepage banners — Phase 15 Chunk B polish
# --------------------------------------------------------------------------
def _read_banner_form(form, files, existing=None):
    """Parse + validate the banner create/edit form. Returns (data, errors)."""
    errors = []
    kind = (form.get("kind") or "").strip()
    if kind not in BANNER_KINDS:
        kind = BANNER_HERO

    image_file = files.get("image")
    if existing is None and (image_file is None or not getattr(image_file, "filename", "")):
        errors.append("An image is required for a new banner.")
    image_path = existing.image_path if existing else None
    if image_file and getattr(image_file, "filename", ""):
        saved = save_upload(image_file, "banners")
        if saved:
            image_path = saved
        else:
            errors.append("Image upload failed — try PNG / JPG under 16 MB.")

    sort_raw = (form.get("sort_order") or "0").strip()
    try:
        sort_order = int(sort_raw)
    except ValueError:
        sort_order = 0

    data = {
        "kind": kind,
        "image_path": image_path,
        "headline": (form.get("headline") or "").strip() or None,
        "subheadline": (form.get("subheadline") or "").strip() or None,
        "button_text": (form.get("button_text") or "").strip() or None,
        "button_url": (form.get("button_url") or "").strip() or None,
        "sort_order": sort_order,
        "is_active": bool(form.get("is_active")),
    }
    return data, errors


@admin.route("/banners/")
@admin_required
def banners():
    items = (HomepageBanner.query
             .order_by(HomepageBanner.kind, HomepageBanner.sort_order,
                       HomepageBanner.id).all())
    return render_template("admin/banners.html", banners=items)


@admin.route("/banners/new", methods=["GET", "POST"])
@admin_required
def banner_create():
    if request.method == "POST":
        data, errors = _read_banner_form(request.form, request.files)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("admin/banner_form.html",
                                   form=request.form, banner=None)
        banner = HomepageBanner(**data)
        db.session.add(banner)
        log_action("Created homepage banner", f"{banner.kind} #{banner.sort_order}")
        db.session.commit()
        flash("Banner created.", "success")
        return redirect(url_for("admin.banners"))
    return render_template("admin/banner_form.html", form={}, banner=None)


@admin.route("/banners/<int:banner_id>/edit", methods=["GET", "POST"])
@admin_required
def banner_edit(banner_id):
    banner = db.session.get(HomepageBanner, banner_id) or abort(404)
    if request.method == "POST":
        data, errors = _read_banner_form(request.form, request.files, existing=banner)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("admin/banner_form.html",
                                   form=request.form, banner=banner)
        for key, value in data.items():
            setattr(banner, key, value)
        log_action("Updated homepage banner", f"#{banner.id}")
        db.session.commit()
        flash("Banner updated.", "success")
        return redirect(url_for("admin.banners"))
    return render_template("admin/banner_form.html", form={}, banner=banner)


@admin.route("/banners/<int:banner_id>/delete", methods=["POST"])
@admin_required
def banner_delete(banner_id):
    banner = db.session.get(HomepageBanner, banner_id) or abort(404)
    log_action("Deleted homepage banner", f"#{banner.id}")
    db.session.delete(banner)
    db.session.commit()
    flash("Banner deleted.", "info")
    return redirect(url_for("admin.banners"))


# --------------------------------------------------------------------------
# platform settings & audit log
# --------------------------------------------------------------------------
SETTING_KEYS = (
    "site_name", "default_commission_rate", "shipping_fee_per_vendor", "currency_symbol",
)


@admin.route("/settings/", methods=["GET", "POST"])
@admin_required
def settings():
    if request.method == "POST":
        for key in SETTING_KEYS:
            if key in request.form:
                set_setting(key, (request.form.get(key) or "").strip())
        log_action("Updated platform settings")
        db.session.commit()
        flash("Platform settings saved.", "success")
        return redirect(url_for("admin.settings"))
    return render_template("admin/settings.html", settings=all_settings())


@admin.route("/audit-log/")
@admin_required
def audit_log():
    page = request.args.get("page", 1, type=int)
    pagination = (
        AuditLog.query.order_by(AuditLog.id.desc())
        .paginate(page=page, per_page=30, error_out=False)
    )
    return render_template("admin/audit_log.html",
                           pagination=pagination, logs=pagination.items)
