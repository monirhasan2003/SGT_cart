"""AI pros/cons summary for the product page — Phase 15 D-8 D3.

The output is cached on `Product.ai_pros_json` / `ai_cons_json` (+
`ai_summary_at` for freshness). Two producers share the same JSON shape:

  * `_anthropic_summary(product, reviews)` — Claude API call when
    `ANTHROPIC_API_KEY` is configured (graceful fallback if it fails).
  * `_heuristic_summary(product, reviews)` — splits review text by rating,
    pulls the most-frequent short fragments from positives (rating ≥ 4) /
    negatives (rating ≤ 2). Always available, no external dep.

`refresh_product_summary(product)` recomputes and commits; `pros(product)`
/ `cons(product)` parse the JSON for the template. The
`refresh-ai-summaries` CLI hits every published product (used as a cron).
"""
import json
import logging
import os
import re
from collections import Counter
from datetime import datetime

from app.extensions import db
from app.models.review import Review

_log = logging.getLogger(__name__)

# Phrases shorter than this don't survive the heuristic — we want sentences
# the buyer can read in a glance, not single words.
_MIN_FRAGMENT_LEN = 12
_MAX_FRAGMENTS = 3                  # bullets returned per side
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?।])\s+|\n+")


def _split_sentences(text):
    if not text:
        return []
    return [s.strip() for s in _SENTENCE_SPLIT.split(text) if s and s.strip()]


def _common_fragments(reviews, *, min_rating=None, max_rating=None):
    """Most-cited short sentences across the filtered reviews."""
    counter = Counter()
    for r in reviews:
        if min_rating is not None and r.rating < min_rating:
            continue
        if max_rating is not None and r.rating > max_rating:
            continue
        for sentence in _split_sentences(r.comment or r.title or ""):
            if len(sentence) < _MIN_FRAGMENT_LEN:
                continue
            counter[sentence[:160]] += 1
    return [s for s, _ in counter.most_common(_MAX_FRAGMENTS)]


def _heuristic_summary(product, reviews):
    """Build pros + cons from review sentences keyed by star count."""
    pros = _common_fragments(reviews, min_rating=4)
    cons = _common_fragments(reviews, max_rating=2)
    return pros, cons


def _anthropic_summary(product, reviews):
    """Optional Claude-API path. Returns ``(pros, cons)`` or raises."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not configured")
    try:
        from anthropic import Anthropic        # type: ignore
    except ImportError as e:
        raise RuntimeError("anthropic SDK not installed") from e

    # Trim the prompt so cost stays small — only the most-recent 30 reviews.
    sample = sorted(reviews, key=lambda r: r.id, reverse=True)[:30]
    bullets = "\n".join(
        f"- ({r.rating}★) {(r.comment or r.title or '').strip()[:300]}"
        for r in sample if (r.comment or r.title)
    )
    if not bullets:
        return [], []

    client = Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": (
                "Below are customer reviews for a product. Summarise into a "
                "JSON object with two arrays: \"pros\" (up to 3 short "
                "positives buyers should know) and \"cons\" (up to 3 "
                "downsides). Output JSON only.\n\n"
                f"Product: {product.title_en}\n\nReviews:\n{bullets}"
            ),
        }],
    )
    text = "".join(part.text for part in msg.content
                   if getattr(part, "type", "") == "text")
    # Strip code fences if Claude wrapped the JSON.
    text = text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    data = json.loads(text)
    pros = [str(x).strip()[:200] for x in (data.get("pros") or [])][:_MAX_FRAGMENTS]
    cons = [str(x).strip()[:200] for x in (data.get("cons") or [])][:_MAX_FRAGMENTS]
    return pros, cons


def refresh_product_summary(product):
    """Recompute the cached AI pros/cons summary. Commits."""
    reviews = (
        Review.query.filter_by(product_id=product.id)
        .order_by(Review.id.desc()).limit(60).all()
    )
    if len(reviews) < 3:
        # Not enough signal yet — clear stale caches so the UI hides itself.
        product.ai_pros_json = None
        product.ai_cons_json = None
        product.ai_summary_at = datetime.utcnow()
        db.session.commit()
        return [], []

    pros, cons = [], []
    try:
        pros, cons = _anthropic_summary(product, reviews)
    except Exception as exc:                # noqa: BLE001
        _log.info("AI summary fallback for product=%s: %s", product.id, exc)
        pros, cons = _heuristic_summary(product, reviews)

    product.ai_pros_json = json.dumps(pros, ensure_ascii=False) if pros else None
    product.ai_cons_json = json.dumps(cons, ensure_ascii=False) if cons else None
    product.ai_summary_at = datetime.utcnow()
    db.session.commit()
    return pros, cons


def _load(value):
    if not value:
        return []
    try:
        out = json.loads(value)
    except Exception:                       # noqa: BLE001
        return []
    return out if isinstance(out, list) else []


def pros(product):
    return _load(product.ai_pros_json if product else None)


def cons(product):
    return _load(product.ai_cons_json if product else None)


def refresh_all_published():
    """Cron entry point — refresh every published product. Returns count."""
    from app.models.catalog import Product, PRODUCT_PUBLISHED
    n = 0
    for product in Product.query.filter_by(status=PRODUCT_PUBLISHED).all():
        refresh_product_summary(product)
        n += 1
    return n
