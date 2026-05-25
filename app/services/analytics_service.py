"""Sales & analytics reports — Phase 11.

`seller_metrics` powers the seller's analytics dashboard and API; the simple
moving-average forecast projects expected revenue. `platform_metrics` powers
the admin reports page. Both run as plain SQL queries against the existing
SubOrder / Order tables — no analytics warehouse needed for an MVP.
"""
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal

from app.extensions import db
from app.models.catalog import Product, Category
from app.models.order import Order, SubOrder, SUBORDER_CANCELLED
from app.models.review import Review

# Stock below this count triggers a "low stock" alert (Phase 11).
LOW_STOCK_THRESHOLD = 5


def _daily_window(days):
    """Inclusive list of ISO-formatted dates covering the last `days` days."""
    today = datetime.utcnow().date()
    return [(today - timedelta(days=i)).isoformat() for i in range(days - 1, -1, -1)]


def _forecast(daily_revenue, days_ahead=7):
    """Simple moving-average projection over the days with activity."""
    active_days = [v for v in daily_revenue.values() if v > 0]
    if not active_days:
        return Decimal("0.00")
    avg = sum(active_days) / Decimal(len(active_days))
    return (avg * Decimal(days_ahead)).quantize(Decimal("0.01"))


def seller_metrics(vendor, days=30):
    """Sales metrics for one seller over the past `days` days."""
    since = datetime.utcnow() - timedelta(days=days)
    subs = SubOrder.query.filter(
        SubOrder.vendor_id == vendor.id,
        SubOrder.created_at >= since,
        SubOrder.status != SUBORDER_CANCELLED,
    ).all()

    revenue = sum((Decimal(s.subtotal) for s in subs), Decimal("0"))
    commission = sum((Decimal(s.commission_amount) for s in subs), Decimal("0"))
    units = sum(sum(i.quantity for i in s.items) for s in subs)
    avg_order = (revenue / Decimal(len(subs))) if subs else Decimal("0")

    # Daily series.
    daily_rev = defaultdict(Decimal)
    daily_ord = defaultdict(int)
    for s in subs:
        key = s.created_at.date().isoformat()
        daily_rev[key] += Decimal(s.subtotal)
        daily_ord[key] += 1
    series = [
        {"date": d,
         "revenue": float(daily_rev.get(d, Decimal("0"))),
         "orders": daily_ord.get(d, 0)}
        for d in _daily_window(days)
    ]

    # Top products + categories.
    by_product = defaultdict(lambda: {"qty": 0, "revenue": Decimal("0"), "title": ""})
    for s in subs:
        for item in s.items:
            pid = item.product_id
            entry = by_product[pid]
            entry["qty"] += item.quantity
            entry["revenue"] += Decimal(item.line_total)
            entry["title"] = item.title
    top_products = [
        {"product_id": pid, "title": v["title"], "qty": v["qty"],
         "revenue": float(v["revenue"])}
        for pid, v in sorted(by_product.items(),
                             key=lambda kv: -kv[1]["revenue"])[:5]
    ]

    top_categories = []
    if by_product:
        rows = (db.session.query(Product.id, Category.name_en)
                .join(Category, Product.category_id == Category.id)
                .filter(Product.id.in_(by_product.keys())).all())
        cat_rev = defaultdict(Decimal)
        for pid, cat_name in rows:
            cat_rev[cat_name] += by_product[pid]["revenue"]
        top_categories = [
            {"category": c, "revenue": float(r)}
            for c, r in sorted(cat_rev.items(), key=lambda kv: -kv[1])[:5]
        ]

    recent_reviews = (
        Review.query.join(Product, Review.product_id == Product.id)
        .filter(Product.vendor_id == vendor.id)
        .order_by(Review.id.desc()).limit(5).all()
    )

    return {
        "period_days": days,
        "total_revenue": float(revenue),
        "total_commission": float(commission),
        "net_earnings": float(revenue - commission),
        "total_orders": len(subs),
        "total_units": units,
        "avg_order_value": float(avg_order),
        "daily_series": series,
        "top_products": top_products,
        "top_categories": top_categories,
        "recent_reviews": recent_reviews,
        "forecast_7d_revenue": float(_forecast(daily_rev, 7)),
    }


def platform_metrics(days=30):
    """Marketplace-wide metrics for the admin reports page."""
    since = datetime.utcnow() - timedelta(days=days)
    orders = Order.query.filter(Order.created_at >= since).all()
    subs = SubOrder.query.filter(
        SubOrder.created_at >= since,
        SubOrder.status != SUBORDER_CANCELLED,
    ).all()

    gmv = sum((Decimal(o.total_amount) for o in orders), Decimal("0"))
    commission = sum((Decimal(s.commission_amount) for s in subs), Decimal("0"))
    customers = len({o.customer_id for o in orders})
    sellers_active = len({s.vendor_id for s in subs})

    daily_gmv = defaultdict(Decimal)
    daily_comm = defaultdict(Decimal)
    for o in orders:
        daily_gmv[o.created_at.date().isoformat()] += Decimal(o.total_amount)
    for s in subs:
        daily_comm[s.created_at.date().isoformat()] += Decimal(s.commission_amount)
    series = [
        {"date": d,
         "gmv": float(daily_gmv.get(d, Decimal("0"))),
         "commission": float(daily_comm.get(d, Decimal("0")))}
        for d in _daily_window(days)
    ]

    by_seller = defaultdict(lambda: {"name": "", "revenue": Decimal("0"), "orders": 0})
    for s in subs:
        entry = by_seller[s.vendor_id]
        entry["revenue"] += Decimal(s.subtotal)
        entry["orders"] += 1
        entry["name"] = s.vendor.shop_name_en if s.vendor else "—"
    top_sellers = [
        {"vendor_id": vid, "shop": v["name"], "orders": v["orders"],
         "revenue": float(v["revenue"])}
        for vid, v in sorted(by_seller.items(),
                             key=lambda kv: -kv[1]["revenue"])[:5]
    ]

    return {
        "period_days": days,
        "gmv": float(gmv),
        "commission_earned": float(commission),
        "total_orders": len(orders),
        "customers": customers,
        "sellers_active": sellers_active,
        "daily_series": series,
        "top_sellers": top_sellers,
    }
