"""Application configuration for SGT Cart.

All secrets and environment-specific values are read from the project-root `.env`
file (never hardcoded). See `.env.example` for the full list of keys.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


def _bool(value, default=False):
    """Parse a truthy string from the environment."""
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


class Config:
    """Base configuration shared by all environments."""

    # --- Core ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-change-me")
    # Session cookie hardening — Lax keeps the cart/session safe from
    # cross-site form submits while still letting OAuth-style redirects work.
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    # Keep CSRF tokens valid for 24h (long-lived forms — checkout, settings).
    WTF_CSRF_TIME_LIMIT = 86400

    # --- Database (PostgreSQL) ---
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # --- JWT (REST API auth — used from Phase 1/7) ---
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    # --- Internationalisation (Bengali / English) ---
    LANGUAGES = ["en", "bn"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "Asia/Dhaka"
    BABEL_TRANSLATION_DIRECTORIES = "translations"

    # --- File uploads (product images, etc.) ---
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "app", "static", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # --- Redis / cache / Celery (provisioned before Phase 8) ---
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CACHE_TYPE = "SimpleCache"  # switched to RedisCache once Redis is available
    CACHE_DEFAULT_TIMEOUT = 300

    # --- Rate limiting (in-memory until Redis is available) ---
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_HEADERS_ENABLED = True

    # --- Real-time (Flask-SocketIO) ---
    # A Redis URL here lets several workers share socket events. Leave unset
    # for single-process development (SocketIO then runs in-process).
    SOCKETIO_MESSAGE_QUEUE = os.environ.get("SOCKETIO_MESSAGE_QUEUE")

    # --- Push notifications (Firebase Cloud Messaging) ---
    # Path to a Firebase service-account JSON file. Unset = push disabled
    # (in-app notifications still work); add the file to enable app push.
    FCM_CREDENTIALS_FILE = os.environ.get("FCM_CREDENTIALS_FILE")

    # --- Payment: SSLCommerz ---
    SSLCOMMERZ_STORE_ID = os.environ.get("SSLCOMMERZ_STORE_ID")
    SSLCOMMERZ_STORE_PASSWORD = os.environ.get("SSLCOMMERZ_STORE_PASSWORD")
    SSLCOMMERZ_SANDBOX = _bool(os.environ.get("SSLCOMMERZ_SANDBOX"), True)

    # --- Email / SMTP ---
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = _bool(os.environ.get("MAIL_USE_TLS"), True)
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER") or os.environ.get("MAIL_USERNAME")
    MAIL_DEBUG = False  # keep SMTP chatter out of the logs

    # --- Auth / OTP ---
    # Customers & sellers verify a one-time code (emailed) on every login;
    # admins log in with password only. Forgot-password also uses an OTP.
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 5
    OTP_MAX_ATTEMPTS = 5
    APP_NAME = "SGT Cart"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
