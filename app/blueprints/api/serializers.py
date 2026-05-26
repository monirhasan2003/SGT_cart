"""JSON serializers for the REST API.

Image fields are returned as absolute URLs so mobile apps can load them.
"""
from flask import url_for

from app.utils.i18n import localized


def media_url(path):
    return url_for("static", filename=path, _external=True) if path else None


def store_json(v):
    """A seller's public store — identity, branding, contact city."""
    return {
        "id": v.id,
        "name": localized(v.shop_name_en, v.shop_name_bn),
        "name_en": v.shop_name_en,
        "name_bn": v.shop_name_bn,
        "slug": v.slug,
        "logo": media_url(v.logo),
        "banner": media_url(v.banner),
        "description": localized(v.description_en, v.description_bn),
        "city": v.city,
        "rating": float(v.rating_avg or 0),
        "rating_count": v.rating_count or 0,
    }


def seller_product_json(p):
    """A product as the owning seller sees it (includes lifecycle status)."""
    data = product_card_json(p)
    data.update({
        "status": p.status,
        "stock": p.stock,
        "sku": p.sku,
        "is_featured": p.is_featured,
        "image_count": len(p.images),
        "variant_count": len(p.variants),
        "created_at": p.created_at.isoformat() if p.created_at else None,
    })
    return data


def category_json(category, with_children=True):
    data = {
        "id": category.id,
        "name": category.localized_name,
        "slug": category.slug,
        "image": media_url(category.image),
    }
    if with_children:
        data["children"] = [
            category_json(child, with_children=False)
            for child in category.children if child.is_active
        ]
    return data


def product_card_json(product):
    return {
        "id": product.id,
        "title": product.localized_title,
        "slug": product.slug,
        "base_price": float(product.base_price),
        "discount_price": float(product.discount_price) if product.discount_price else None,
        "current_price": float(product.current_price),
        "image": media_url(product.primary_image),
        "rating": float(product.rating_avg or 0),
        "rating_count": product.rating_count or 0,
        "vendor": (
            {"name": product.vendor.localized_shop_name,
             "name_en": product.vendor.shop_name_en,
             "name_bn": product.vendor.shop_name_bn,
             "slug": product.vendor.slug}
            if product.vendor else None
        ),
    }


def product_detail_json(product):
    data = product_card_json(product)
    data.update({
        "description": product.localized_description,
        "stock": product.stock,
        "sku": product.sku,
        "category": (
            {"name": product.category.localized_name, "slug": product.category.slug}
            if product.category else None
        ),
        "images": [media_url(i.image_path) for i in product.images],
        "variants": [
            {
                "id": v.id, "size": v.size, "color": v.color,
                "price": float(v.price) if v.price is not None else None,
                "stock": v.stock,
            }
            for v in product.variants
        ],
    })
    return data


def cart_item_json(item):
    return {
        "id": item.id,
        "product_id": item.product_id,
        "variant_id": item.variant_id,
        "title": item.product.localized_title,
        "slug": item.product.slug,
        "image": media_url(item.product.primary_image),
        "unit_price": float(item.unit_price),
        "quantity": item.quantity,
        "line_total": float(item.line_total),
        "variant": (
            {"size": item.variant.size, "color": item.variant.color}
            if item.variant else None
        ),
    }


def address_json(a):
    return {
        "id": a.id, "label": a.label, "full_name": a.full_name, "phone": a.phone,
        "address_line": a.address_line, "area": a.area, "city": a.city,
        "district": a.district, "postal_code": a.postal_code, "is_default": a.is_default,
    }


def static_page_json(page, detail=True):
    """Footer / policy page from the StaticPage table — bilingual fields
    resolve to the active locale via localized_* properties."""
    data = {
        "slug": page.slug,
        "title": page.localized_title,
        "subtitle": page.localized_subtitle,
        "section": page.localized_section,
        "contact_email": page.contact_email,
        "version": page.version,
    }
    if detail:
        data.update({
            "body_html": page.localized_body_html,
            "toc": page.toc_items,
            "faq": page.faq_items,
            "related": page.related_items,
            "reviewed_at": (page.reviewed_at.isoformat()
                            if page.reviewed_at else None),
        })
    return data


def order_json(order, detail=False):
    data = {
        "order_number": order.order_number,
        "subtotal": float(order.subtotal),
        "shipping_fee": float(order.shipping_fee),
        "discount_amount": float(order.discount_amount or 0),
        "coupon_code": order.coupon_code,
        "points_redeemed": order.points_redeemed or 0,
        "points_discount": float(order.points_discount or 0),
        "total_amount": float(order.total_amount),
        "payment_method": order.payment_method,
        "payment_status": order.payment_status,
        "item_count": order.item_count,
        "created_at": order.created_at.isoformat() if order.created_at else None,
    }
    if detail:
        data["shipping"] = {
            "name": order.ship_name, "phone": order.ship_phone,
            "address_line": order.ship_address_line, "area": order.ship_area,
            "city": order.ship_city, "postal_code": order.ship_postal_code,
        }
        data["suborders"] = [
            {
                "id": s.id,
                "vendor": s.vendor.localized_shop_name if s.vendor else None,
                "status": s.status,
                "subtotal": float(s.subtotal),
                "items": [
                    {
                        "title": i.title, "variant": i.variant_label,
                        "unit_price": float(i.unit_price), "quantity": i.quantity,
                        "line_total": float(i.line_total),
                    }
                    for i in s.items
                ],
                # Live order-tracking timeline.
                "tracking": [
                    {
                        "status": e.status, "note": e.note,
                        "at": e.created_at.isoformat() if e.created_at else None,
                    }
                    for e in s.events
                ],
            }
            for s in order.suborders
        ]
    return data
