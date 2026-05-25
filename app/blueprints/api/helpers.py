"""Shared helpers for the REST API.

Web views authenticate with Flask-Login sessions; the API uses JWT. These
helpers give API endpoints a consistent error envelope and JWT role checks.
"""
from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from app.extensions import db
from app.models.user import User


def err(message, status=400):
    """Consistent JSON error response."""
    return jsonify({"error": message}), status


def current_api_user():
    """Return the User for the current JWT identity, or None."""
    identity = get_jwt_identity()
    if identity is None:
        return None
    try:
        return db.session.get(User, int(identity))
    except (TypeError, ValueError):
        return None


def role_required(*roles):
    """JWT-protect an endpoint and require the token's role to be in `roles`.

    A missing/invalid token yields 401 (via Flask-JWT-Extended); a valid token
    with the wrong role yields a 403 JSON error.
    """
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            verify_jwt_in_request()
            if get_jwt().get("role") not in roles:
                return err("You do not have access to this resource.", 403)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def customer_required(view):
    """Restrict an API endpoint to customer tokens."""
    return role_required("customer")(view)


def seller_required(view):
    """Restrict an API endpoint to seller tokens."""
    return role_required("seller")(view)
