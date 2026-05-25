"""Admin-editable static pages (footer content).

A single `StaticPage` row stores everything the public renderer + the
admin form need:

  - `slug` — the URL path *without* leading or trailing slash. For
    top-level pages this is e.g. "careers". For nested pages it includes
    the prefix: "help/how-to-order", "sell/payouts".
  - `body_html` — main page content (raw HTML; admin can paste). The
    shell (ToC + contact card + version footer + cookie banner) is
    drawn by the existing `_layout.html` so this only needs sections.
  - `toc_json` — list of `{"anchor": "scope", "label": "1. Scope"}`
  - `faq_json` — list of `{"q": "...", "a": "..."}`
  - `related_json` — list of `{"href": "...", "title": "...", "desc": "..."}`

Wave-1 polished pages (terms, privacy, seller-terms, …) still have their
hardcoded templates — Werkzeug picks the more specific route over the
StaticPage catch-all, so they keep their rich custom HTML. The
StaticPage system fills in every other footer link and is fully
admin-editable.
"""
import json
from datetime import datetime

from app.extensions import db


class StaticPage(db.Model):
    __tablename__ = "static_pages"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    title = db.Column(db.String(180), nullable=False)
    subtitle = db.Column(db.String(400))
    section = db.Column(db.String(80), default="Misc")
    contact_email = db.Column(db.String(120), default="support@sgtcart.com")

    body_html = db.Column(db.Text)
    toc_json = db.Column(db.Text)         # JSON array
    faq_json = db.Column(db.Text)         # JSON array
    related_json = db.Column(db.Text)     # JSON array

    version = db.Column(db.String(20), default="v1.0")
    reviewed_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # --------------------------------------------------------------
    # JSON convenience accessors used by the public template
    # --------------------------------------------------------------
    @staticmethod
    def _safe_load(raw):
        try:
            data = json.loads(raw or "[]")
        except (TypeError, json.JSONDecodeError):
            return []
        return data if isinstance(data, list) else []

    @property
    def toc_items(self):
        return self._safe_load(self.toc_json)

    @property
    def faq_items(self):
        return self._safe_load(self.faq_json)

    @property
    def related_items(self):
        return self._safe_load(self.related_json)

    def __repr__(self):
        return f"<StaticPage {self.slug}>"
