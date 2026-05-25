"""SGT Cart — Flask application factory.

Serves the web storefront (KUMO/Jinja templates), the REST API (added per phase)
and WebSocket events (Phase 8) from one backend, all sharing models + services.
"""
import os

from flask import Flask, render_template, request, session, has_request_context
from slugify import slugify

from config import config
from .extensions import (
    db, migrate, csrf, login_manager, jwt, babel, cors, cache, limiter, mail,
    socketio,
)

SUPPORTED_LANGUAGES = ["en", "bn"]


def get_locale():
    """Choose the UI language: ?lang= override > session > browser > default."""
    if not has_request_context():
        return "en"  # background jobs (e.g. email rendering) have no request
    requested = request.args.get("lang")
    if requested in SUPPORTED_LANGUAGES:
        session["lang"] = requested
    return (
        session.get("lang")
        or request.accept_languages.best_match(SUPPORTED_LANGUAGES)
        or "en"
    )


_INSECURE_KEYS = {None, "", "dev-insecure-change-me"}


def create_app(config_name=None):
    """Build and configure a Flask app instance."""
    app = Flask(__name__)
    config_name = config_name or os.environ.get("FLASK_CONFIG", "default")
    app.config.from_object(config[config_name])

    # Production refuses to boot with the development secret in place.
    if config_name == "production" and app.config["SECRET_KEY"] in _INSECURE_KEYS:
        raise RuntimeError(
            "Refusing to start: SECRET_KEY must be set to a real value in "
            "the production .env (use a 32+ byte random hex string)."
        )

    # Ensure the upload folder exists.
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # --- Bind extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    cache.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    # Real-time: a Redis message queue is used when configured, otherwise
    # SocketIO runs in-process (fine for single-worker development).
    socketio.init_app(app, message_queue=app.config.get("SOCKETIO_MESSAGE_QUEUE"))

    # --- Register models so Flask-Migrate autogenerate sees every table ---
    from . import models  # noqa: F401

    # --- Legacy KUMO context processors (hardcoded demo data) ---
    # Auto-register every `global_*` function. These are replaced by real DB
    # queries in Phase 2; kept for now so the existing templates still render.
    from . import context_processors as cp
    for name in dir(cp):
        if name.startswith("global_"):
            func = getattr(cp, name)
            if callable(func):
                app.context_processor(func)

    # Expose the active locale + language list to all templates.
    @app.context_processor
    def inject_i18n():
        return {"current_locale": get_locale(), "languages": SUPPORTED_LANGUAGES}

    # Tell templates whether an admin is impersonating another user.
    @app.context_processor
    def inject_impersonation():
        if not has_request_context():
            return {"is_impersonating": False}
        return {"is_impersonating": bool(session.get("impersonator_id"))}

    # Category-icon helper (Phase 15) — maps a category slug to a Bootstrap
    # Icons class + accent colour. Used by the homepage Categories grid so
    # every tile has a recognisable visual without needing uploaded images.
    @app.context_processor
    def inject_category_icon():
        # Bootstrap Icons + soft-tint backgrounds. Keys are matched as a
        # prefix, so `electronics-mobiles` falls back through `electronics`
        # if there's no specific entry, then to a neutral default.
        MAP = {
            "electronics-mobiles":       ("bi-phone",         "#e0f2fe", "#0284c7"),
            "electronics-laptops":       ("bi-laptop",        "#e0f2fe", "#0284c7"),
            "electronics-headphones":    ("bi-headphones",    "#e0f2fe", "#0284c7"),
            "electronics-cameras":       ("bi-camera",        "#e0f2fe", "#0284c7"),
            "electronics-televisions":   ("bi-tv",            "#e0f2fe", "#0284c7"),
            "electronics":               ("bi-display",       "#e0f2fe", "#0284c7"),
            "fashion-men-s-wear":        ("bi-person",        "#fce7f3", "#db2777"),
            "fashion-women-s-wear":      ("bi-person-heart",  "#fce7f3", "#db2777"),
            "fashion-kids-wear":         ("bi-balloon-heart", "#fce7f3", "#db2777"),
            "fashion-shoes":             ("bi-bag",           "#fce7f3", "#db2777"),
            "fashion-watches":           ("bi-watch",         "#fce7f3", "#db2777"),
            "fashion":                   ("bi-bag-heart",     "#fce7f3", "#db2777"),
            "home-living-furniture":     ("bi-lamp",          "#dcfce7", "#16a34a"),
            "home-living-kitchen":       ("bi-cup-hot",       "#dcfce7", "#16a34a"),
            "home-living-home-decor":    ("bi-flower1",       "#dcfce7", "#16a34a"),
            "home-living":               ("bi-house-heart",   "#dcfce7", "#16a34a"),
            "grocery-vegetables":        ("bi-tree",          "#fef3c7", "#ca8a04"),
            "grocery-fruits":            ("bi-apple",         "#fef3c7", "#ca8a04"),
            "grocery-beverages":         ("bi-cup-straw",     "#fef3c7", "#ca8a04"),
            "grocery":                   ("bi-basket",        "#fef3c7", "#ca8a04"),
            "health-beauty-skincare":    ("bi-droplet-half",  "#f3e8ff", "#9333ea"),
            "health-beauty-makeup":      ("bi-palette",       "#f3e8ff", "#9333ea"),
            "health-beauty-personal-care": ("bi-heart-pulse", "#f3e8ff", "#9333ea"),
            "health-beauty":             ("bi-heart-pulse",   "#f3e8ff", "#9333ea"),
        }
        DEFAULT = ("bi-tag", "#f1f5f9", "#475569")

        def category_icon(slug):
            slug = (slug or "").lower()
            if slug in MAP:
                icon, bg, fg = MAP[slug]
            else:
                # Try the first segment of the slug (e.g. "electronics-foo" → "electronics").
                root = slug.split("-")[0] if "-" in slug else slug
                icon, bg, fg = MAP.get(root, DEFAULT)
            return {"icon": icon, "bg": bg, "fg": fg}

        return {"category_icon": category_icon}

    # Active root categories for the navbar dropdown + footer (Phase 15).
    @app.context_processor
    def inject_nav():
        if not has_request_context():
            return {"nav_categories": []}
        try:
            from .models.catalog import Category
            cats = (Category.query.filter_by(parent_id=None, is_active=True)
                    .order_by(Category.sort_order, Category.name_en).limit(10).all())
        except Exception:  # noqa: BLE001 — never let nav lookup break a page
            cats = []
        return {"nav_categories": cats}

    # --- Blueprints ---
    # The monolithic `routes.py` is split into proper blueprints across
    # Phases 1-2; for now it is registered as-is so the storefront works.
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .blueprints.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .blueprints.account import account as account_blueprint
    app.register_blueprint(account_blueprint)

    from .blueprints.seller import seller as seller_blueprint
    app.register_blueprint(seller_blueprint)

    from .blueprints.storefront import storefront as storefront_blueprint
    app.register_blueprint(storefront_blueprint)

    from .blueprints.cart import cart as cart_blueprint
    app.register_blueprint(cart_blueprint)

    from .blueprints.payment import payment as payment_blueprint
    app.register_blueprint(payment_blueprint)
    csrf.exempt(payment_blueprint)  # SSLCommerz posts callbacks without our token

    from .blueprints.chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)

    from .blueprints.notification import notification as notification_blueprint
    app.register_blueprint(notification_blueprint)

    from .blueprints.review import review as review_blueprint
    app.register_blueprint(review_blueprint)

    from .blueprints.pages import pages as pages_blueprint
    app.register_blueprint(pages_blueprint)

    from .blueprints.legal import legal as legal_blueprint
    app.register_blueprint(legal_blueprint)

    # REST API (JSON, JWT) — CSRF does not apply to token-authenticated APIs.
    from .blueprints.api import api_v1 as api_blueprint
    app.register_blueprint(api_blueprint)
    csrf.exempt(api_blueprint)

    # Admin-editable footer pages. Registered LAST so the static_pages
    # catch-all `<path:slug>/` route only matches when no specific
    # `pages.py` / `legal.py` / other route handled the request.
    from .blueprints.static_pages import static_pages as static_pages_blueprint
    app.register_blueprint(static_pages_blueprint)

    # --- Real-time socket handlers (Phase 8) ---
    from .sockets import register_socket_handlers
    register_socket_handlers()

    # --- CLI commands (flask create-admin, ...) ---
    from .cli import register_cli
    register_cli(app)

    # --- Security headers (Phase 14) ---
    # CSP allows the CDNs the KUMO theme + our pages already use
    # (jsdelivr, socket.io, unpkg, Google Fonts). `'unsafe-inline'` /
    # `'unsafe-eval'` are kept for the theme's many inline scripts — a future
    # pass can move to nonces.
    _CSP = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' "
        "https://cdn.jsdelivr.net https://cdn.socket.io https://unpkg.com; "
        "style-src 'self' 'unsafe-inline' "
        "https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "font-src 'self' data: https://fonts.gstatic.com https://cdn.jsdelivr.net; "
        "img-src 'self' data: blob: https:; "
        "connect-src 'self' ws: wss:; "
        "media-src 'self' blob:; "
        "frame-ancestors 'self'; base-uri 'self'; form-action 'self'"
    )
    # Allow voice search (mic) and image upload from camera on first-party pages.
    _PERMISSIONS = "microphone=(self), camera=(self), geolocation=()"

    @app.after_request
    def _security_headers(response):
        response.headers.setdefault("Content-Security-Policy", _CSP)
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
        response.headers.setdefault("Referrer-Policy", "same-origin")
        response.headers.setdefault("Permissions-Policy", _PERMISSIONS)
        # HSTS only over HTTPS — production / proxy with TLS in front.
        if not app.config.get("DEBUG"):
            response.headers.setdefault(
                "Strict-Transport-Security",
                "max-age=31536000; includeSubDomains",
            )
        return response

    # --- Error pages ---
    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    # --- Jinja helpers ---
    app.jinja_env.filters["slugify"] = slugify

    # `{{ obj|tr('title') }}` -> locale-aware field picker. See
    # app/utils/i18n.py for the lookup rules. Use this wherever a
    # template needs a DB-stored string in the current locale.
    from .utils.i18n import tr as _tr_filter
    app.jinja_env.filters["tr"] = _tr_filter

    return app
