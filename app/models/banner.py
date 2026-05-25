"""Homepage banners — Phase 15 Chunk B polish.

`HomepageBanner` powers two things on the homepage:
  * `hero`  — the carousel of large slides at the top of the page.
  * `strip` — the wide promotional ribbon between the hero and the
              first product section (Daraz's "Eid Shera Deals" strip).

Each row has an uploaded image plus optional overlay text and a single
optional button. Admins manage them from `/admin/banners/`.
"""
from datetime import datetime

from app.extensions import db

BANNER_HERO = "hero"
BANNER_STRIP = "strip"
BANNER_KINDS = (BANNER_HERO, BANNER_STRIP)


class HomepageBanner(db.Model):
    __tablename__ = "homepage_banners"

    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(10), nullable=False, default=BANNER_HERO, index=True)

    image_path = db.Column(db.String(255), nullable=False)   # relative to /static/
    headline = db.Column(db.String(160))
    subheadline = db.Column(db.String(300))
    button_text = db.Column(db.String(60))
    button_url = db.Column(db.String(255))

    sort_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<HomepageBanner {self.id} {self.kind}>"
