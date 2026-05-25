"""DB-backed admin-editable footer pages.

Two halves:

* **Public renderer** — exposes `/<path:slug>/` (registered LAST, so the
  many specific routes in `pages.py` / `legal.py` win for Wave-1 pages
  that already have polished templates). The matcher pulls a published
  `StaticPage` row by its full path slug (e.g. `help/how-to-order`,
  `sell/payouts`, `careers`). Anything not found → 404.

* **Admin CRUD** under `/admin/static-pages/` — list, create, edit,
  delete. Every footer page can be edited from the admin without
  touching code.
"""
import json
from datetime import datetime

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, abort,
)
from slugify import slugify

from app.extensions import db
from app.models.static_page import StaticPage
from app.utils.decorators import admin_required


static_pages = Blueprint("static_pages", __name__)


# ---------------------------------------------------------------------------
# Public renderer
# ---------------------------------------------------------------------------
def _normalize_slug(path):
    """Strip leading / trailing slashes — DB stores the canonical form."""
    return (path or "").strip("/").lower()


@static_pages.route("/<path:slug>/", endpoint="view")
def view_page(slug):
    slug = _normalize_slug(slug)
    if not slug:
        abort(404)
    page = StaticPage.query.filter_by(slug=slug, is_published=True).first()
    if page is None:
        abort(404)
    return render_template("pages/db_page.html", page=page)


# ---------------------------------------------------------------------------
# Admin CRUD
# ---------------------------------------------------------------------------
def _parse_json_field(raw):
    """Validate that the textarea contains a JSON array. Falls back to []."""
    raw = (raw or "").strip()
    if not raw:
        return "[]"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc.msg}") from exc
    if not isinstance(data, list):
        raise ValueError("Must be a JSON array.")
    return json.dumps(data, ensure_ascii=False)


@static_pages.route("/admin/static-pages/", endpoint="admin_list")
@admin_required
def admin_list():
    pages = (StaticPage.query
             .order_by(StaticPage.section, StaticPage.sort_order, StaticPage.title)
             .all())
    return render_template("admin/static_pages.html", pages=pages)


@static_pages.route("/admin/static-pages/new",
                    methods=["GET", "POST"], endpoint="admin_create")
@admin_required
def admin_create():
    if request.method == "POST":
        return _save(None)
    return render_template("admin/static_page_form.html",
                           page=None, form={})


@static_pages.route("/admin/static-pages/<int:page_id>/edit",
                    methods=["GET", "POST"], endpoint="admin_edit")
@admin_required
def admin_edit(page_id):
    page = StaticPage.query.get_or_404(page_id)
    if request.method == "POST":
        return _save(page)
    return render_template("admin/static_page_form.html",
                           page=page, form={})


@static_pages.route("/admin/static-pages/<int:page_id>/delete",
                    methods=["POST"], endpoint="admin_delete")
@admin_required
def admin_delete(page_id):
    page = StaticPage.query.get_or_404(page_id)
    db.session.delete(page)
    db.session.commit()
    flash(f"Deleted page '{page.title}'.", "success")
    return redirect(url_for("static_pages.admin_list"))


def _save(page):
    """Shared create/update handler — driven by the same form template."""
    f = request.form
    slug = _normalize_slug(f.get("slug") or "")
    if not slug:
        # Auto-derive a slug from the title for convenience.
        slug = slugify(f.get("title") or "")
    if not slug:
        flash("Slug or title is required.", "danger")
        return redirect(request.url)

    # Uniqueness — skip the row being edited.
    clash = StaticPage.query.filter_by(slug=slug).first()
    if clash is not None and (page is None or clash.id != page.id):
        flash(f"Another page already uses slug '{slug}'.", "danger")
        return redirect(request.url)

    try:
        toc_json = _parse_json_field(f.get("toc_json"))
        faq_json = _parse_json_field(f.get("faq_json"))
        related_json = _parse_json_field(f.get("related_json"))
        toc_json_bn = _parse_json_field(f.get("toc_json_bn")) if (f.get("toc_json_bn") or "").strip() else None
        faq_json_bn = _parse_json_field(f.get("faq_json_bn")) if (f.get("faq_json_bn") or "").strip() else None
        related_json_bn = _parse_json_field(f.get("related_json_bn")) if (f.get("related_json_bn") or "").strip() else None
    except ValueError as exc:
        flash(str(exc), "danger")
        return redirect(request.url)

    is_new = page is None
    if is_new:
        page = StaticPage()
        db.session.add(page)

    page.slug = slug
    page.title = (f.get("title") or "").strip() or slug
    page.subtitle = (f.get("subtitle") or "").strip() or None
    page.section = (f.get("section") or "Misc").strip()
    page.contact_email = (f.get("contact_email") or "support@sgtcart.com").strip()
    page.body_html = f.get("body_html") or ""
    page.toc_json = toc_json
    page.faq_json = faq_json
    page.related_json = related_json
    # Bangla fields — keep None if blank so localized() falls back to English.
    page.title_bn = (f.get("title_bn") or "").strip() or None
    page.subtitle_bn = (f.get("subtitle_bn") or "").strip() or None
    page.section_bn = (f.get("section_bn") or "").strip() or None
    page.body_html_bn = (f.get("body_html_bn") or "").strip() or None
    page.toc_json_bn = toc_json_bn
    page.faq_json_bn = faq_json_bn
    page.related_json_bn = related_json_bn
    page.version = (f.get("version") or "v1.0").strip()
    page.is_published = bool(f.get("is_published"))
    page.sort_order = int(f.get("sort_order") or 0)
    page.reviewed_at = datetime.utcnow()

    db.session.commit()
    flash(("Created" if is_new else "Updated") + f" page '{page.title}'.",
          "success")
    return redirect(url_for("static_pages.admin_list"))
