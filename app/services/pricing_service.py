"""Pricing service — Phase 15 D-5.

Single source of truth for the unit-price the customer ultimately pays at
a given quantity:

  base unit price  <-  variant override (if set) or product.current_price
  effective unit   <-  base * (1 - bulk_tier.discount_pct/100) when a tier
                       row's min_quantity is met
"""
from decimal import Decimal, ROUND_HALF_UP

from app.models.catalog import ProductPriceTier

_CENT = Decimal("0.01")
_ZERO = Decimal("0.00")
_HUNDRED = Decimal("100")


def applicable_tier(product, quantity):
    """Return the best `ProductPriceTier` for `quantity`, or None."""
    if not product or quantity is None or quantity < 1:
        return None
    tiers = product.price_tiers or []
    best = None
    for t in tiers:
        if t.min_quantity <= quantity:
            if best is None or t.min_quantity > best.min_quantity:
                best = t
    return best


def effective_unit_price(product, quantity, base_unit_price=None):
    """Apply any matching bulk-pricing tier to `base_unit_price`.

    `base_unit_price` defaults to ``product.current_price``. Returns a
    Decimal quantized to 2 dp.
    """
    if base_unit_price is None:
        base_unit_price = product.current_price
    base = Decimal(base_unit_price or 0)
    tier = applicable_tier(product, quantity)
    if tier is None or not tier.discount_pct:
        return base.quantize(_CENT, rounding=ROUND_HALF_UP)
    factor = (_HUNDRED - Decimal(tier.discount_pct)) / _HUNDRED
    return max(_ZERO, (base * factor).quantize(_CENT, rounding=ROUND_HALF_UP))


def tier_preview(product):
    """Render-friendly list of tiers ascending by quantity.

    Each row carries the discounted unit price already computed so the
    product page table doesn't repeat the math.
    """
    out = []
    base = Decimal(product.current_price or 0)
    for t in sorted(product.price_tiers or [], key=lambda t: t.min_quantity):
        factor = (_HUNDRED - Decimal(t.discount_pct)) / _HUNDRED
        unit = (base * factor).quantize(_CENT, rounding=ROUND_HALF_UP)
        out.append({
            "min_quantity": t.min_quantity,
            "discount_pct": float(t.discount_pct),
            "unit_price": unit,
        })
    return out
