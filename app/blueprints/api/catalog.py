"""API v1 — public catalog: categories, products, search, stores.

These endpoints are unauthenticated; they back the storefront browsing
experience in the customer app.
"""
from flask import request, jsonify

from app.extensions import db
from app.models.catalog import Product, Category, PRODUCT_PUBLISHED
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.services.flash_sale_service import live_sales
from app.services.search_service import apply_ranking, log_view, log_search, autocomplete
from app.services.recommendation_service import similar_products, also_viewed
from app.services import image_search_service
from .helpers import err
from .serializers import (
    category_json, product_card_json, product_detail_json, store_json,
)
from . import api_v1

PER_PAGE = 20
MAX_PER_PAGE = 60


def _page_meta(p):
    """Pagination envelope shared by every list endpoint."""
    return {
        "page": p.page, "per_page": p.per_page, "total": p.total,
        "pages": p.pages, "has_next": p.has_next, "has_prev": p.has_prev,
    }


def _per_page():
    return min(request.args.get("per_page", PER_PAGE, type=int) or PER_PAGE, MAX_PER_PAGE)


def _apply_product_filters(query):
    """Apply the q / min / max query-string filters shared by listings."""
    q = (request.args.get("q") or "").strip()
    min_price = request.args.get("min", type=float)
    max_price = request.args.get("max", type=float)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Product.title_en.ilike(like), Product.title_bn.ilike(like))
        )
    if min_price is not None:
        query = query.filter(Product.base_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.base_price <= max_price)
    return query


def _sorted(query):
    """Apply the `sort` param; the default is the marketplace ranking rule."""
    sort = (request.args.get("sort") or "").strip()
    if sort == "price_asc":
        return query.order_by(Product.base_price.asc())
    if sort == "price_desc":
        return query.order_by(Product.base_price.desc())
    return apply_ranking(query)


@api_v1.route("/categories", methods=["GET"])
def categories():
    """Active root categories, each with its active children."""
    roots = (
        Category.query.filter_by(parent_id=None, is_active=True)
        .order_by(Category.sort_order, Category.name_en).all()
    )
    return jsonify({"categories": [category_json(c) for c in roots]})


@api_v1.route("/products", methods=["GET"])
def products():
    """Published products with category / search / price / sort filters."""
    page = request.args.get("page", 1, type=int)
    category_slug = (request.args.get("category") or "").strip()

    query = Product.query.filter_by(status=PRODUCT_PUBLISHED)
    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat is None:
            return err("Unknown category.", 404)
        cat_ids = [cat.id] + [c.id for c in cat.children]
        query = query.filter(Product.category_id.in_(cat_ids))

    query = _sorted(_apply_product_filters(query))
    p = query.paginate(page=page, per_page=_per_page(), error_out=False)
    q = (request.args.get("q") or "").strip()
    if q:
        log_search(q, result_count=p.total)
    return jsonify({
        "products": [product_card_json(x) for x in p.items],
        "pagination": _page_meta(p),
    })


@api_v1.route("/products/<slug>", methods=["GET"])
def product_detail(slug):
    """Full product detail plus a few related products."""
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        return err("Product not found.", 404)
    log_view(product)

    data = product_detail_json(product)
    # Raw bilingual fields so the app can offer a language toggle.
    data["title_en"] = product.title_en
    data["title_bn"] = product.title_bn
    data["description_en"] = product.description_en
    data["description_bn"] = product.description_bn

    related = (
        Product.query.filter_by(category_id=product.category_id, status=PRODUCT_PUBLISHED)
        .filter(Product.id != product.id)
        .order_by(Product.created_at.desc()).limit(6).all()
    )
    data["related"] = [product_card_json(r) for r in related]
    return jsonify({"product": data})


@api_v1.route("/products/<slug>/similar", methods=["GET"])
def product_similar(slug):
    """Same-category products, ranked by quality (content-based)."""
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        return err("Product not found.", 404)
    return jsonify({
        "products": [product_card_json(p) for p in similar_products(product)]
    })


@api_v1.route("/products/<slug>/also-viewed", methods=["GET"])
def product_also_viewed(slug):
    """Products other customers viewed alongside this one (collaborative)."""
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        return err("Product not found.", 404)
    return jsonify({
        "products": [product_card_json(p) for p in also_viewed(product)]
    })


@api_v1.route("/search/image", methods=["POST"])
def search_by_image():
    """Find visually-similar products. Body: multipart field `image`."""
    upload = request.files.get("image")
    if upload is None or not upload.filename:
        return err("An image file is required.", 400)
    if not image_search_service.is_available():
        return err("Image search is unavailable on this server.", 503)
    results = image_search_service.search_by_image(upload, limit=24)
    return jsonify({"products": [
        dict(product_card_json(p), similarity=round(s, 4)) for p, s in results
    ]})


@api_v1.route("/search/suggest", methods=["GET"])
def search_suggest():
    """Product-title autocomplete suggestions."""
    return jsonify({"suggestions": autocomplete(request.args.get("q", ""))})


@api_v1.route("/flash-sales", methods=["GET"])
def flash_sales():
    """Live flash sales with their discounted products."""
    return jsonify({"flash_sales": [
        {
            "title": s.title,
            "slug": s.slug,
            "description": s.description,
            "ends_at": s.ends_at.isoformat() if s.ends_at else None,
            "products": [
                dict(product_card_json(it.product), flash_price=float(it.flash_price))
                for it in s.items
                if it.product is not None and it.product.is_published
            ],
        }
        for s in live_sales()
    ]})


@api_v1.route("/stores", methods=["GET"])
def stores():
    """All approved seller storefronts."""
    vendors = (
        VendorProfile.query.filter_by(status=VENDOR_APPROVED)
        .order_by(VendorProfile.id.desc()).all()
    )
    return jsonify({"stores": [store_json(v) for v in vendors]})


@api_v1.route("/stores/<slug>", methods=["GET"])
def store_detail(slug):
    """A seller's store page — branding, its categories, filtered products."""
    vendor = VendorProfile.query.filter_by(slug=slug, status=VENDOR_APPROVED).first()
    if vendor is None:
        return err("Store not found.", 404)

    page = request.args.get("page", 1, type=int)
    category_slug = (request.args.get("category") or "").strip()

    query = Product.query.filter_by(vendor_id=vendor.id, status=PRODUCT_PUBLISHED)
    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first()
        if cat is not None:
            query = query.filter(Product.category_id == cat.id)
    query = _sorted(_apply_product_filters(query))
    p = query.paginate(page=page, per_page=_per_page(), error_out=False)

    # The categories this store actually sells in (for the in-store filter).
    cat_ids = [
        row[0] for row in db.session.query(Product.category_id)
        .filter_by(vendor_id=vendor.id, status=PRODUCT_PUBLISHED).distinct()
    ]
    cats = (
        Category.query.filter(Category.id.in_(cat_ids))
        .order_by(Category.name_en).all() if cat_ids else []
    )

    data = store_json(vendor)
    data["categories"] = [category_json(c, with_children=False) for c in cats]
    data["products"] = [product_card_json(x) for x in p.items]
    data["pagination"] = _page_meta(p)
    return jsonify({"store": data})
