"""Flash sale service — Phase 9.

Activating a flash sale snapshots each product's `discount_price` and
replaces it with the flash price; deactivating restores the snapshot. Because
the rest of the app already prices off `Product.current_price` (which uses
`discount_price`), flash pricing flows through cart, checkout and the API
with no further changes.
"""
from datetime import datetime

from app.extensions import db
from app.models.marketing import FlashSale, FlashSaleItem


def is_live(sale):
    """True when the sale is active and within its time window."""
    now = datetime.utcnow()
    return (
        sale.is_active
        and (sale.starts_at is None or sale.starts_at <= now)
        and (sale.ends_at is None or sale.ends_at >= now)
    )


def live_sales():
    """Active flash sales currently within their window."""
    return [s for s in FlashSale.query.filter_by(is_active=True).all() if is_live(s)]


def product_on_active_sale(product_id, exclude_sale_id=None):
    """True when the product already belongs to another active flash sale."""
    q = (FlashSaleItem.query
         .join(FlashSale, FlashSaleItem.flash_sale_id == FlashSale.id)
         .filter(FlashSaleItem.product_id == product_id,
                 FlashSale.is_active.is_(True)))
    if exclude_sale_id is not None:
        q = q.filter(FlashSale.id != exclude_sale_id)
    return q.first() is not None


def active_sale_for_product(product):
    """Return the currently-live FlashSale containing `product`, or None.

    Drives the product-page promotional strip (Phase 15 D-10): when the
    product is on a live flash sale, the strip surfaces the sale's title +
    a countdown to `ends_at` inline at the top of the page.
    """
    if product is None:
        return None
    sale = (
        FlashSale.query
        .join(FlashSaleItem, FlashSaleItem.flash_sale_id == FlashSale.id)
        .filter(FlashSale.is_active.is_(True),
                FlashSaleItem.product_id == product.id)
        .order_by(FlashSale.id.desc()).first()
    )
    return sale if (sale and is_live(sale)) else None


def _apply_item(item):
    product = item.product
    if product is None:
        return
    item.original_discount_price = product.discount_price
    product.discount_price = item.flash_price


def _restore_item(item):
    product = item.product
    if product is None:
        return
    product.discount_price = item.original_discount_price
    item.original_discount_price = None


def activate(sale):
    """Apply every item's flash price to its product (caller commits)."""
    if sale.is_active:
        return
    for item in sale.items:
        _apply_item(item)
    sale.is_active = True


def deactivate(sale):
    """Restore the products' original prices (caller commits)."""
    if not sale.is_active:
        return
    for item in sale.items:
        _restore_item(item)
    sale.is_active = False


def add_item(sale, product, flash_price):
    """Add a product to a sale, applying its price now if the sale is live."""
    item = FlashSaleItem(
        flash_sale_id=sale.id, product_id=product.id, flash_price=flash_price,
    )
    item.product = product
    db.session.add(item)
    if sale.is_active:
        _apply_item(item)
    return item


def remove_item(item):
    """Remove a sale item, restoring the product price if the sale is live."""
    if item.flash_sale is not None and item.flash_sale.is_active:
        _restore_item(item)
    db.session.delete(item)
