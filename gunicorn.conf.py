"""Gunicorn configuration for SGT Cart production.

Run from the project root, with the venv activated:

    gunicorn -c gunicorn.conf.py wsgi:app

Install the eventlet worker on the production host (Linux):

    pip install gunicorn eventlet
"""
import multiprocessing
import os

# --- network ---
bind = os.environ.get("GUNICORN_BIND", "127.0.0.1:8000")
backlog = 2048

# --- workers ---
# Flask-SocketIO needs an async worker (eventlet or gevent) so a single
# process can hold many long-poll / WebSocket connections.
worker_class = os.environ.get("GUNICORN_WORKER_CLASS", "eventlet")
# Scaling to multiple workers REQUIRES a shared SocketIO message queue —
# set SOCKETIO_MESSAGE_QUEUE=redis://... in .env, then bump workers.
default_workers = int(os.environ.get("GUNICORN_WORKERS", "1"))
workers = max(1, default_workers)
worker_connections = 1000
threads = 1

# --- timeouts ---
timeout = 60                 # request timeout
graceful_timeout = 30        # SIGTERM grace period
keepalive = 5

# --- logging ---
accesslog = "-"              # stdout
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")
proc_name = "sgt-ecommerce"

# --- security ---
# Trust X-Forwarded-* from the local reverse proxy only.
forwarded_allow_ips = os.environ.get("FORWARDED_ALLOW_IPS", "127.0.0.1")
