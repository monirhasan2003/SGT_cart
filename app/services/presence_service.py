"""Lightweight in-memory product viewer counter — Phase 15 D-6.

Drives the "Z viewing now" urgency badge on the product page. Each call to
`record_view` stamps a per-product, per-viewer timestamp; `active_viewers`
returns the count of distinct viewers seen within the last `_WINDOW_SECONDS`.

This is *per-process* state — counts are approximate. Behind a multi-worker
Gunicorn deployment each worker keeps its own dict, so the displayed number
is a lower bound. A Redis-backed implementation is the obvious upgrade path
(swap this module's two functions, keep the call sites). For SGT's current
single-worker dev/staging setup the approximation is fine.
"""
import time
import threading
from collections import defaultdict

_WINDOW_SECONDS = 60          # how recent a tick counts as "active"
_PRUNE_AFTER = 120            # garbage-collect viewers older than this

# {product_id: {viewer_key: last_seen_epoch}}
_views = defaultdict(dict)
_lock = threading.Lock()


def record_view(product_id, viewer_key):
    """Stamp now() as the latest view of `product_id` by `viewer_key`.

    `viewer_key` is `user.id` for authenticated users, the Flask session
    id for anonymous ones — anything stable for the duration of a visit.
    """
    if not product_id or not viewer_key:
        return
    now = time.time()
    with _lock:
        bucket = _views[product_id]
        bucket[viewer_key] = now
        # Opportunistic prune — keep the bucket small.
        if len(bucket) > 256:
            stale = now - _PRUNE_AFTER
            for key in list(bucket.keys()):
                if bucket[key] < stale:
                    bucket.pop(key, None)


def active_viewers(product_id):
    """Return the distinct viewers seen in the last `_WINDOW_SECONDS`.

    The current viewer's own row is counted — the displayed number starts
    at 1 ("you are viewing now"), which matches Daraz's surface.
    """
    if not product_id:
        return 0
    cutoff = time.time() - _WINDOW_SECONDS
    with _lock:
        bucket = _views.get(product_id) or {}
        return sum(1 for ts in bucket.values() if ts >= cutoff)


def reset():
    """Test-only helper to wipe the in-memory state."""
    with _lock:
        _views.clear()
        _user_seen.clear()


# --------------------------------------------------------------------------
# User presence — Phase 15 D-7 chat presence indicator.
# --------------------------------------------------------------------------
# Online means "has emitted a socket event in the last ONLINE_WINDOW_SECONDS".
# Falls back to the DB-stamped `User.last_seen_at` for offline users so the
# "Last seen X ago" line keeps working across process restarts.
_user_seen = {}                          # {user_id: last_seen_epoch}
ONLINE_WINDOW_SECONDS = 120


def mark_user_online(user_id):
    """Stamp `user_id` as currently online (socket-driven)."""
    if not user_id:
        return
    with _lock:
        _user_seen[user_id] = time.time()


def is_user_online(user_id):
    """True when the user has emitted a socket event within the window."""
    if not user_id:
        return False
    cutoff = time.time() - ONLINE_WINDOW_SECONDS
    with _lock:
        return _user_seen.get(user_id, 0) >= cutoff


def user_last_seen_epoch(user_id):
    """Last in-memory tick for `user_id`, or None."""
    if not user_id:
        return None
    with _lock:
        return _user_seen.get(user_id)
