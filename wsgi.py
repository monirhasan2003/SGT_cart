"""WSGI entry point for production servers (gunicorn / uWSGI).

Usage:
    gunicorn -c gunicorn.conf.py wsgi:app

Flask-SocketIO attaches its long-poll / WebSocket transport to the same
WSGI app, so gunicorn with the `eventlet` worker class serves both regular
HTTP and the real-time channel.
"""
from app import create_app
from app.extensions import socketio  # noqa: F401  (import binds SocketIO to the app)

app = create_app("production")
