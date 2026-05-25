"""Product recommendations — Phase 10 (content + collaborative).

Three recommendation flavours, all built from `ProductView` and `OrderItem`
signals — no ML model needed for this MVP. They run on the product detail
page, the customer dashboard, and the REST API.
"""
from sqlalchemy import func, text

from app.extensions import db
from app.models.catalog import Product, PRODUCT_PUBLISHED
from app.models.analytics import ProductView
from app.models.order import Order, SubOrder, OrderItem
from app.services.search_service import apply_ranking


def similar_products(product, limit=8):
    """Same-category products (content-based), ranked by quality."""
    if product is None:
        return []
    query = (
        Product.query.filter(
            Product.id != product.id,
            Product.category_id == product.category_id,
            Product.status == PRODUCT_PUBLISHED,
        )
    )
    return apply_ranking(query).limit(limit).all()


def also_viewed(product, limit=8):
    """Products other users viewed alongside this one (item-to-item collab).

    For each user who viewed `product`, count the OTHER products they viewed;
    return the most-co-viewed.
    """
    if product is None:
        return []

    viewer_ids = [
        row[0] for row in
        db.session.query(ProductView.user_id)
        .filter(ProductView.product_id == product.id,
                ProductView.user_id.isnot(None))
        .distinct().all()
    ]
    if not viewer_ids:
        return []

    co_rows = (
        db.session.query(ProductView.product_id,
                         func.count(ProductView.id).label("n"))
        .filter(ProductView.user_id.in_(viewer_ids),
                ProductView.product_id != product.id)
        .group_by(ProductView.product_id)
        .order_by(text("n DESC")).limit(limit * 3).all()
    )
    if not co_rows:
        return []

    pids = [row[0] for row in co_rows]
    products = (
        Product.query.filter(Product.id.in_(pids),
                             Product.status == PRODUCT_PUBLISHED).all()
    )
    rank = {pid: i for i, pid in enumerate(pids)}
    products.sort(key=lambda p: rank.get(p.id, 999))
    return products[:limit]


def frequently_bought_together(product, limit=4):
    """Products commonly bought alongside `product` (Phase 15 D-8 D1).

    Walks past orders containing this product and counts how often each
    *other* product appeared in the same order. Highest-co-occurrence
    products are returned. When there's no signal yet the result is empty
    (the product page degrades to its existing "Similar" recommendations).
    """
    if product is None:
        return []

    # Orders that contained this product.
    order_ids = [
        row[0] for row in
        db.session.query(Order.id)
        .join(SubOrder, SubOrder.order_id == Order.id)
        .join(OrderItem, OrderItem.sub_order_id == SubOrder.id)
        .filter(OrderItem.product_id == product.id)
        .distinct().all()
    ]
    if not order_ids:
        return []

    # Other products in those orders — co-occurrence count.
    rows = (
        db.session.query(OrderItem.product_id,
                         func.count(OrderItem.id).label("n"))
        .join(SubOrder, OrderItem.sub_order_id == SubOrder.id)
        .filter(
            SubOrder.order_id.in_(order_ids),
            OrderItem.product_id.isnot(None),
            OrderItem.product_id != product.id,
        )
        .group_by(OrderItem.product_id)
        .order_by(text("n DESC")).limit(limit * 3).all()
    )
    if not rows:
        return []

    pids = [row[0] for row in rows]
    items = (
        Product.query.filter(
            Product.id.in_(pids),
            Product.status == PRODUCT_PUBLISHED,
        ).all()
    )
    rank = {pid: i for i, pid in enumerate(pids)}
    items.sort(key=lambda p: rank.get(p.id, 999))
    return items[:limit]


def best_sellers(limit=8):
    """Top products by units sold across delivered/placed orders."""
    rows = (
        db.session.query(Product.id, func.count(OrderItem.id).label("n"))
        .join(OrderItem, OrderItem.product_id == Product.id)
        .filter(Product.status == PRODUCT_PUBLISHED)
        .group_by(Product.id).order_by(text("n DESC")).limit(limit).all()
    )
    ids = [row[0] for row in rows]
    if not ids:
        # No sales yet — fall back to the ranking rule.
        return (apply_ranking(Product.query.filter_by(status=PRODUCT_PUBLISHED))
                .limit(limit).all())
    products = Product.query.filter(Product.id.in_(ids)).all()
    order = {pid: i for i, pid in enumerate(ids)}
    products.sort(key=lambda p: order.get(p.id, 999))
    return products


def for_you(user, limit=8):
    """Personal mix — recent-interest categories minus already-seen products,
    padded with best-sellers when the signal is thin."""
    if user is None or getattr(user, "id", None) is None:
        return best_sellers(limit)

    cat_rows = (
        db.session.query(Product.category_id,
                         func.count(ProductView.id).label("n"))
        .join(ProductView, Product.id == ProductView.product_id)
        .filter(ProductView.user_id == user.id)
        .group_by(Product.category_id)
        .order_by(text("n DESC")).limit(5).all()
    )
    cat_ids = [row[0] for row in cat_rows if row[0] is not None]
    if not cat_ids:
        return best_sellers(limit)

    viewed_ids = {
        row[0] for row in
        db.session.query(ProductView.product_id)
        .filter(ProductView.user_id == user.id).distinct().all()
    }
    query = Product.query.filter(
        Product.category_id.in_(cat_ids),
        Product.status == PRODUCT_PUBLISHED,
    )
    if viewed_ids:
        query = query.filter(~Product.id.in_(viewed_ids))
    items = apply_ranking(query).limit(limit).all()

    if len(items) < limit:
        # Pad with best-sellers — never re-include products the user has seen.
        chosen = {p.id for p in items} | viewed_ids
        for p in best_sellers(limit):
            if p.id not in chosen:
                items.append(p)
                chosen.add(p.id)
                if len(items) >= limit:
                    break
    return items
