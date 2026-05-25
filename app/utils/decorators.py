"""Role-based access decorators for web (session) views.

API endpoints use JWT-based role checks (see `app/blueprints/api`).
"""
from functools import wraps

from flask import abort, flash, redirect, request, url_for
from flask_login import current_user


def role_required(*roles):
    """Allow the view only for authenticated users whose role is in `roles`.

    Unauthenticated users are sent to the storefront login page.
    """
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in to continue.", "warning")
                return redirect(url_for("auth.login", next=request.path))
            if current_user.role not in roles:
                abort(403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def admin_required(view):
    """Admin-only views.

    Unauthenticated visitors are sent to the dedicated **admin** login page
    (not the customer/seller login). Authenticated non-admins get a 403.
    """
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("admin.login", next=request.path))
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def seller_required(view):
    """Restrict a view to sellers."""
    return role_required("seller")(view)


def approved_vendor_required(view):
    """Seller views that need an approved vendor profile (e.g. product management).

    Unapproved sellers are redirected to their dashboard with a notice.
    """
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        if not current_user.is_seller:
            abort(403)
        profile = current_user.vendor_profile
        if profile is None or not profile.is_approved:
            flash("Your shop must be approved by an admin before you can manage products.",
                  "warning")
            return redirect(url_for("seller.dashboard"))
        return view(*args, **kwargs)
    return wrapped
