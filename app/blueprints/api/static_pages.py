"""Public StaticPage endpoints — power the footer / policy / help pages
inside the Flutter customer + seller apps.

All payloads honour the `?lang=bn` query string (or `Accept-Language`
header) automatically through the `localized_*` properties on the model.
"""
from flask import jsonify, request

from app.models.static_page import StaticPage

from . import api_v1
from .serializers import static_page_json


@api_v1.route("/static-pages", methods=["GET"])
def list_static_pages():
    """List every published static page — summary form, ordered by section
    + sort_order so the Flutter footer renderer can group them."""
    pages = (StaticPage.query
             .filter_by(is_published=True)
             .order_by(StaticPage.section,
                       StaticPage.sort_order,
                       StaticPage.title)
             .all())
    section = request.args.get("section")
    if section:
        pages = [p for p in pages if (p.section or "").lower() == section.lower()]
    return jsonify({
        "pages": [static_page_json(p, detail=False) for p in pages],
        "count": len(pages),
    })


@api_v1.route("/static-pages/<path:slug>", methods=["GET"])
def get_static_page(slug):
    """Fetch a single page — title + body_html + toc + faq + related,
    all in the active locale."""
    slug = (slug or "").strip("/").lower()
    page = StaticPage.query.filter_by(slug=slug, is_published=True).first()
    if page is None:
        return jsonify({"error": "Page not found"}), 404
    return jsonify(static_page_json(page, detail=True))
