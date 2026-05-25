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
from app.utils.i18n import localized


class StaticPage(db.Model):
    __tablename__ = "static_pages"

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    title = db.Column(db.String(180), nullable=False)        # English (canonical)
    title_bn = db.Column(db.String(180))                      # Bangla (optional)
    subtitle = db.Column(db.String(400))
    subtitle_bn = db.Column(db.String(400))
    section = db.Column(db.String(80), default="Misc")
    section_bn = db.Column(db.String(80))
    contact_email = db.Column(db.String(120), default="support@sgtcart.com")

    body_html = db.Column(db.Text)
    body_html_bn = db.Column(db.Text)
    toc_json = db.Column(db.Text)         # JSON array
    toc_json_bn = db.Column(db.Text)
    faq_json = db.Column(db.Text)         # JSON array
    faq_json_bn = db.Column(db.Text)
    related_json = db.Column(db.Text)     # JSON array
    related_json_bn = db.Column(db.Text)

    version = db.Column(db.String(20), default="v1.0")
    reviewed_at = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, nullable=False, default=True)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    # --------------------------------------------------------------
    # Localized string accessors
    # --------------------------------------------------------------
    @property
    def localized_title(self):
        return localized(self.title, self.title_bn)

    @property
    def localized_subtitle(self):
        return localized(self.subtitle, self.subtitle_bn)

    @property
    def localized_section(self):
        return localized(self.section, self.section_bn)

    @property
    def localized_body_html(self):
        return localized(self.body_html, self.body_html_bn)

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
        # Prefer Bangla list when on bn locale and a Bangla list was authored.
        bn = self._safe_load(self.toc_json_bn)
        if bn:
            return self._safe_load(localized(self.toc_json, self.toc_json_bn))
        return self._safe_load(self.toc_json)

    @property
    def faq_items(self):
        bn = self._safe_load(self.faq_json_bn)
        if bn:
            return self._safe_load(localized(self.faq_json, self.faq_json_bn))
        return self._safe_load(self.faq_json)

    @property
    def related_items(self):
        bn = self._safe_load(self.related_json_bn)
        if bn:
            return self._safe_load(localized(self.related_json, self.related_json_bn))
        return self._safe_load(self.related_json)

    def __repr__(self):
        return f"<StaticPage {self.slug}>"
