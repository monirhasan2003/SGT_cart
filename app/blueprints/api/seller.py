"""API v1 — seller surface: products, order fulfilment, earnings & payouts.

The seller Flutter app ("Seller Center") consumes these. Business logic
(wallet settlement, order split) is reused from the shared services layer so
the API never diverges from the web seller dashboard.
"""
from decimal import Decimal

from flask import request, jsonify
from slugify import slugify

from app.extensions import db
from app.models.catalog import (
    Product, ProductVariant, Category,
    PRODUCT_DRAFT, PRODUCT_PENDING, PRODUCT_REJECTED,
)
from app.models.order import SubOrder, SUBORDER_STATUSES
from app.models.wallet import PayoutRequest
from app.services.wallet_service import get_or_create_wallet, hold_for_payout
from app.services.order_service import update_suborder_status
from app.services.analytics_service import seller_metrics
from .helpers import err, current_api_user, seller_required
from .serializers import media_url, product_detail_json, seller_product_json
from . import api_v1


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def _vendor():
    """The VendorProfile of the current seller token, or None."""
    user = current_api_user()
    return user.vendor_profile if user else None


def _own_product(product_id, vendor):
    """Return the seller's own product, or None."""
    product = db.session.get(Product, product_id)
    if product is None or vendor is None or product.vendor_id != vendor.id:
        return None
    return product


def _unique_product_slug(title):
    base = slugify(title) or "product"
    slug, i = base, 2
    while Product.query.filter_by(slug=slug).first() is not None:
        slug = f"{base}-{i}"
        i += 1
    return slug


def _suborder_json(s, detail=False):
    """A SubOrder — the seller's slice of a customer order."""
    data = {
        "id": s.id,
        "order_number": s.order.order_number if s.order else None,
        "status": s.status,
        "subtotal": float(s.subtotal),
        "commission_amount": float(s.commission_amount),
        "vendor_earning": float(s.vendor_earning),
        "item_count": len(s.items),
        "created_at": s.created_at.isoformat() if s.created_at else None,
    }
    if detail:
        o = s.order
        data["payment_method"] = o.payment_method if o else None
        data["payment_status"] = o.payment_status if o else None
        data["shipping"] = {
            "name": o.ship_name, "phone": o.ship_phone,
            "address_line": o.ship_address_line, "area": o.ship_area,
            "city": o.ship_city, "district": o.ship_district,
            "postal_code": o.ship_postal_code,
        } if o else None
        data["items"] = [
            {
                "title": i.title, "variant": i.variant_label,
                "unit_price": float(i.unit_price), "quantity": i.quantity,
                "line_total": float(i.line_total),
            }
            for i in s.items
        ]
    return data


# --------------------------------------------------------------------------
# profile
# --------------------------------------------------------------------------
@api_v1.route("/seller/profile", methods=["GET"])
@seller_required
def seller_profile():
    vp = _vendor()
    if vp is None:
        return err("Seller profile not found.", 404)
    wallet = get_or_create_wallet(vp.id)
    db.session.commit()
    return jsonify({"seller": {
        "shop_name": vp.shop_name_en,
        "shop_name_bn": vp.shop_name_bn,
        "slug": vp.slug,
        "status": vp.status,
        "is_approved": vp.is_approved,
        "verification_submitted": vp.is_verification_submitted,
        "commission_rate": float(vp.commission_rate or 0),
        "logo": media_url(vp.logo),
        "banner": media_url(vp.banner),
        "wallet": {
            "available": float(wallet.available_balance),
            "pending": float(wallet.pending_balance),
            "total_earned": float(wallet.total_earned),
        },
    }})


# --------------------------------------------------------------------------
# products
# --------------------------------------------------------------------------
@api_v1.route("/seller/products", methods=["GET"])
@seller_required
def seller_products():
    vp = _vendor()
    if vp is None:
        return err("Seller profile not found.", 404)
    query = Product.query.filter_by(vendor_id=vp.id)
    status = (request.args.get("status") or "").strip()
    if status:
        query = query.filter_by(status=status)
    items = query.order_by(Product.id.desc()).all()
    return jsonify({"products": [seller_product_json(p) for p in items]})


@api_v1.route("/seller/products", methods=["POST"])
@seller_required
def seller_create_product():
    vp = _vendor()
    if vp is None:
        return err("Seller profile not found.", 404)
    if not vp.is_approved:
        return err("Your shop must be approved before you can list products.", 403)

    data = request.get_json(silent=True) or {}
    title_en = (data.get("title_en") or "").strip()
    if not title_en:
        return err("title_en is required.")
    category = db.session.get(Category, data.get("category_id")) if data.get("category_id") else None
    if category is None:
        return err("A valid category_id is required.")

    try:
        base_price = float(data.get("base_price", 0))
    except (TypeError, ValueError):
        return err("base_price must be a number.")
    discount_price = data.get("discount_price")
    if discount_price not in (None, ""):
        try:
            discount_price = float(discount_price)
        except (TypeError, ValueError):
            return err("discount_price must be a number.")
    else:
        discount_price = None
    try:
        stock = int(data.get("stock", 0))
    except (TypeError, ValueError):
        return err("stock must be an integer.")

    product = Product(
        vendor_id=vp.id, category_id=category.id,
        title_en=title_en, title_bn=(data.get("title_bn") or "").strip() or None,
        slug=_unique_product_slug(title_en),
        description_en=(data.get("description_en") or "").strip() or None,
        description_bn=(data.get("description_bn") or "").strip() or None,
        base_price=base_price, discount_price=discount_price,
        sku=(data.get("sku") or "").strip() or None, stock=stock,
        status=PRODUCT_DRAFT,
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"product": seller_product_json(product)}), 201


@api_v1.route("/seller/products/<int:product_id>", methods=["GET"])
@seller_required
def seller_product_detail(product_id):
    product = _own_product(product_id, _vendor())
    if product is None:
        return err("Product not found.", 404)
    data = product_detail_json(product)
    data["status"] = product.status
    data["title_en"] = product.title_en
    data["title_bn"] = product.title_bn
    data["description_en"] = product.description_en
    data["description_bn"] = product.description_bn
    return jsonify({"product": data})


@api_v1.route("/seller/products/<int:product_id>", methods=["PATCH"])
@seller_required
def seller_update_product(product_id):
    product = _own_product(product_id, _vendor())
    if product is None:
        return err("Product not found.", 404)
    data = request.get_json(silent=True) or {}

    if "title_en" in data:
        title = (data.get("title_en") or "").strip()
        if not title:
            return err("title_en cannot be empty.")
        product.title_en = title
    if "title_bn" in data:
        product.title_bn = (data.get("title_bn") or "").strip() or None
    if "description_en" in data:
        product.description_en = (data.get("description_en") or "").strip() or None
    if "description_bn" in data:
        product.description_bn = (data.get("description_bn") or "").strip() or None
    if "category_id" in data:
        category = db.session.get(Category, data.get("category_id"))
        if category is None:
            return err("Invalid category_id.")
        product.category_id = category.id
    if "base_price" in data:
        try:
            product.base_price = float(data["base_price"])
        except (TypeError, ValueError):
            return err("base_price must be a number.")
    if "discount_price" in data:
        dp = data["discount_price"]
        if dp in (None, ""):
            product.discount_price = None
        else:
            try:
                product.discount_price = float(dp)
            except (TypeError, ValueError):
                return err("discount_price must be a number.")
    if "stock" in data:
        try:
            product.stock = int(data["stock"])
        except (TypeError, ValueError):
            return err("stock must be an integer.")
    if "sku" in data:
        product.sku = (data.get("sku") or "").strip() or None

    db.session.commit()
    return jsonify({"product": seller_product_json(product)})


@api_v1.route("/seller/products/<int:product_id>", methods=["DELETE"])
@seller_required
def seller_delete_product(product_id):
    product = _own_product(product_id, _vendor())
    if product is None:
        return err("Product not found.", 404)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted."})


@api_v1.route("/seller/products/<int:product_id>/submit", methods=["POST"])
@seller_required
def seller_submit_product(product_id):
    """Submit a draft/rejected product for admin review."""
    product = _own_product(product_id, _vendor())
    if product is None:
        return err("Product not found.", 404)
    if not product.images:
        return err("Add at least one product image before submitting.", 400)
    if product.status not in (PRODUCT_DRAFT, PRODUCT_REJECTED):
        return err("This product has already been submitted.", 409)
    product.status = PRODUCT_PENDING
    db.session.commit()
    return jsonify({"product": seller_product_json(product)})


# --------------------------------------------------------------------------
# variants
# --------------------------------------------------------------------------
@api_v1.route("/seller/products/<int:product_id>/variants", methods=["POST"])
@seller_required
def seller_add_variant(product_id):
    product = _own_product(product_id, _vendor())
    if product is None:
        return err("Product not found.", 404)
    data = request.get_json(silent=True) or {}
    size = (data.get("size") or "").strip()
    color = (data.get("color") or "").strip()
    if not size and not color:
        return err("A variant needs at least a size or a color.")
    price = data.get("price")
    if price not in (None, ""):
        try:
            price = float(price)
        except (TypeError, ValueError):
            return err("price must be a number.")
    else:
        price = None
    try:
        stock = int(data.get("stock", 0))
    except (TypeError, ValueError):
        return err("stock must be an integer.")

    variant = ProductVariant(
        product_id=product.id, size=size or None, color=color or None,
        price=price, stock=stock,
    )
    db.session.add(variant)
    db.session.commit()
    return jsonify({"variant": {
        "id": variant.id, "size": variant.size, "color": variant.color,
        "price": float(variant.price) if variant.price is not None else None,
        "stock": variant.stock,
    }}), 201


@api_v1.route("/seller/products/<int:product_id>/variants/<int:variant_id>",
              methods=["DELETE"])
@seller_required
def seller_delete_variant(product_id, variant_id):
    product = _own_product(product_id, _vendor())
    if product is None:
        return err("Product not found.", 404)
    variant = db.session.get(ProductVariant, variant_id)
    if variant is None or variant.product_id != product.id:
        return err("Variant not found.", 404)
    db.session.delete(variant)
    db.session.commit()
    return jsonify({"message": "Variant deleted."})


# --------------------------------------------------------------------------
# order fulfilment
# --------------------------------------------------------------------------
@api_v1.route("/seller/orders", methods=["GET"])
@seller_required
def seller_orders():
    vp = _vendor()
    if vp is None:
        return err("Seller profile not found.", 404)
    query = SubOrder.query.filter_by(vendor_id=vp.id)
    status = (request.args.get("status") or "").strip()
    if status:
        query = query.filter_by(status=status)
    subs = query.order_by(SubOrder.id.desc()).all()
    return jsonify({"orders": [_suborder_json(s) for s in subs]})


@api_v1.route("/seller/orders/<int:sub_order_id>", methods=["GET"])
@seller_required
def seller_order_detail(sub_order_id):
    vp = _vendor()
    sub = db.session.get(SubOrder, sub_order_id)
    if sub is None or vp is None or sub.vendor_id != vp.id:
        return err("Order not found.", 404)
    return jsonify({"order": _suborder_json(sub, detail=True)})


@api_v1.route("/seller/orders/<int:sub_order_id>/status", methods=["POST"])
@seller_required
def seller_order_status(sub_order_id):
    """Advance fulfilment status; delivery settles the wallet earning."""
    vp = _vendor()
    sub = db.session.get(SubOrder, sub_order_id)
    if sub is None or vp is None or sub.vendor_id != vp.id:
        return err("Order not found.", 404)

    new_status = (request.get_json(silent=True) or {}).get("status", "")
    if new_status not in SUBORDER_STATUSES:
        return err("status must be one of: " + ", ".join(SUBORDER_STATUSES) + ".")

    # Centralised: records tracking event, settles wallet, notifies customer.
    update_suborder_status(sub, new_status)
    db.session.commit()
    return jsonify({"order": _suborder_json(sub, detail=True)})


# --------------------------------------------------------------------------
# earnings & payouts
# --------------------------------------------------------------------------
@api_v1.route("/seller/earnings", methods=["GET"])
@seller_required
def seller_earnings():
    vp = _vendor()
    if vp is None:
        return err("Seller profile not found.", 404)
    wallet = get_or_create_wallet(vp.id)
    db.session.commit()

    subs = SubOrder.query.filter_by(vendor_id=vp.id).all()
    payouts = (
        PayoutRequest.query.filter_by(vendor_id=vp.id)
        .order_by(PayoutRequest.id.desc()).all()
    )
    return jsonify({
        "wallet": {
            "available": float(wallet.available_balance),
            "pending": float(wallet.pending_balance),
            "total_earned": float(wallet.total_earned),
        },
        "stats": {
            "orders": len(subs),
            "total_sales": float(sum((s.subtotal for s in subs), Decimal("0"))),
            "total_commission": float(
                sum((s.commission_amount for s in subs), Decimal("0"))
            ),
        },
        "payout_requests": [
            {
                "id": p.id, "amount": float(p.amount), "method": p.method,
                "status": p.status,
                "requested_at": p.requested_at.isoformat() if p.requested_at else None,
            }
            for p in payouts
        ],
    })


@api_v1.route("/seller/analytics", methods=["GET"])
@seller_required
def seller_analytics():
    """Sales metrics, top products, and a simple revenue forecast."""
    vp = _vendor()
    if vp is None:
        return err("Seller profile not found.", 404)
    days = max(7, min(365, request.args.get("days", 30, type=int) or 30))
    metrics = seller_metrics(vp, days=days)
    # ORM Review rows aren't JSON-serializable — flatten them.
    metrics["recent_reviews"] = [
        {
            "rating": r.rating, "title": r.title, "comment": r.comment,
            "product": r.product.title_en if r.product else None,
            "author": r.user.name if r.user else None,
            "at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in metrics.get("recent_reviews", [])
    ]
    return jsonify(metrics)


@api_v1.route("/seller/payouts", methods=["POST"])
@seller_required
def seller_request_payout():
    """Request a withdrawal against the available wallet balance."""
    vp = _vendor()
    if vp is None:
        return err("Seller profile not found.", 404)
    wallet = get_or_create_wallet(vp.id)
    db.session.commit()

    data = request.get_json(silent=True) or {}
    method = (data.get("method") or "").strip()
    try:
        amount = Decimal(str(data.get("amount", "0")))
    except Exception:  # noqa: BLE001
        return err("amount must be a number.")

    account_detail = {
        "bkash": vp.bkash_number or "",
        "nagad": vp.nagad_number or "",
        "bank": f"{vp.bank_name or ''} {vp.bank_account_number or ''}".strip(),
    }.get(method, "")

    if amount <= 0:
        return err("Enter a valid payout amount.")
    if method not in ("bkash", "nagad", "bank"):
        return err("method must be 'bkash', 'nagad' or 'bank'.")
    if amount > Decimal(str(wallet.available_balance or 0)):
        return err("Amount exceeds your available balance.")
    if not account_detail.strip():
        return err(f"Set up your {method} payout details first.")

    hold_for_payout(vp.id, amount)
    payout = PayoutRequest(
        vendor_id=vp.id, amount=amount, method=method,
        account_detail=account_detail.strip(),
    )
    db.session.add(payout)
    db.session.commit()
    return jsonify({"payout": {
        "id": payout.id, "amount": float(payout.amount),
        "method": payout.method, "status": payout.status,
    }}), 201
