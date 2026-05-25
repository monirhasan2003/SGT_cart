"""Smart search & ranking — Phase 10.

`apply_ranking` is the marketplace ranking rule: results lead with featured
products, then sellers with a higher rating (plus any admin boost), then the
product's own rating, then recency. `log_view` / `log_search` capture the
signals the recommendation engine (Chunk B) and analytics (Phase 11) use.
"""
from datetime import datetime

from app.extensions import db
from app.models.catalog import Product, PRODUCT_PUBLISHED
from app.models.vendor import VendorProfile
from app.models.analytics import ProductView, SearchLog

AUTOCOMPLETE_MIN = 2


def apply_ranking(query):
    """Order a Product query by the marketplace ranking rule.

    Score = seller rating + admin boost + delivery-speed bonus − cancel penalty.
    Higher-rated, faster-shipping, lower-cancel sellers surface first. The
    admin stays neutral by default (boost = 0). Delivery and cancel signals
    are refreshed by `vendor_stats_service.recompute_vendor_stats`.

    Admin-paid Sponsored products (Phase 15 v3c) rank just under featured —
    above the organic score — but only while still within their paid window.
    """
    from sqlalchemy import and_, case, or_
    # Delivery bonus: 1 day → +1.0, 3 days → +0.33, no data → 0.
    delivery_bonus = case(
        (VendorProfile.avg_delivery_days > 0,
         1.0 / VendorProfile.avg_delivery_days),
        else_=0,
    )
    # Cancel penalty: 10% cancel rate → −0.2, 50% → −1.0.
    cancel_penalty = VendorProfile.cancel_rate * 2
    score = (VendorProfile.rating_avg + VendorProfile.ranking_boost
             + delivery_bonus - cancel_penalty)
    sponsored_active = case(
        (and_(
            Product.is_sponsored.is_(True),
            or_(Product.sponsored_until.is_(None),
                Product.sponsored_until >= datetime.utcnow()),
         ), 1),
        else_=0,
    )
    return (
        query.join(VendorProfile, Product.vendor_id == VendorProfile.id)
        .order_by(
            Product.is_featured.desc(),
            sponsored_active.desc(),
            score.desc(),
            Product.rating_avg.desc(),
            Product.created_at.desc(),
        )
    )


def log_view(product, user=None):
    """Record a product-detail visit (signal for recommendations)."""
    if product is None:
        return
    db.session.add(ProductView(
        product_id=product.id,
        user_id=user.id if (user is not None and getattr(user, "id", None)) else None,
    ))
    db.session.commit()


def log_search(query_text, user=None, result_count=0):
    """Record a catalog search (signal for autocomplete + trending)."""
    query_text = (query_text or "").strip()
    if not query_text:
        return
    db.session.add(SearchLog(
        term=query_text[:160],
        user_id=user.id if (user is not None and getattr(user, "id", None)) else None,
        result_count=result_count,
    ))
    db.session.commit()


def autocomplete(prefix, limit=8):
    """Product-title suggestions for the search box."""
    prefix = (prefix or "").strip()
    if len(prefix) < AUTOCOMPLETE_MIN:
        return []
    like = f"%{prefix}%"
    rows = (
        Product.query
        .filter(
            Product.status == PRODUCT_PUBLISHED,
            db.or_(Product.title_en.ilike(like), Product.title_bn.ilike(like)),
        )
        .order_by(Product.rating_count.desc(), Product.is_featured.desc(),
                  Product.id.desc())
        .limit(limit).all()
    )
    return [{"title": p.localized_title, "slug": p.slug} for p in rows]


def trending_searches(limit=8, days=30):
    """The most-run search queries (for a 'popular searches' hint)."""
    from datetime import datetime, timedelta
    since = datetime.utcnow() - timedelta(days=days)
    rows = (
        db.session.query(SearchLog.term, db.func.count(SearchLog.id).label("n"))
        .filter(SearchLog.created_at >= since, SearchLog.result_count > 0)
        .group_by(SearchLog.term)
        .order_by(db.text("n DESC"))
        .limit(limit).all()
    )
    return [r[0] for r in rows]
