"""CLIP image search — Phase 10 Chunk C (Python fallback, no pgvector).

The small `clip-ViT-B-32` sentence-transformers model encodes both images
and text into the same 512-d semantic space. Visually similar products land
close together; cosine similarity is computed in NumPy.

Storage swap-out: when pgvector arrives, only `_to_bytes` / `_from_bytes`
and the `search_by_image` query change — the model code and the service
contract stay identical.
"""
import io
import logging
import os

from app.extensions import db
from app.models.catalog import Product, PRODUCT_PUBLISHED
from app.models.embedding import ProductEmbedding

logger = logging.getLogger(__name__)

_MODEL_NAME = "clip-ViT-B-32"
_model = None
_np_module = None


def _np():
    """Lazily import numpy so the app boots without the ML stack."""
    global _np_module
    if _np_module is None:
        import numpy as np
        _np_module = np
    return _np_module


def _load_model():
    """Load the CLIP model on first use (cached). Returns None if unavailable."""
    global _model
    if _model is not None:
        return _model
    try:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(_MODEL_NAME)
    except Exception as exc:  # noqa: BLE001 — package missing or weights failed
        logger.warning("CLIP model unavailable: %s", exc)
        return None
    return _model


def is_available():
    """True when image search can actually run (model loadable)."""
    return _load_model() is not None


# --------------------------------------------------------------------------
# image -> vector
# --------------------------------------------------------------------------
def _open_image(source):
    """Accept a filesystem path, a Flask FileStorage, raw bytes, or BytesIO."""
    from PIL import Image
    if hasattr(source, "read"):
        return Image.open(source).convert("RGB")
    if isinstance(source, (bytes, bytearray)):
        return Image.open(io.BytesIO(source)).convert("RGB")
    return Image.open(source).convert("RGB")


def encode_image(source):
    """Unit-norm CLIP embedding for an image — numpy float32 [512]. None on
    failure (model not loaded or image unreadable)."""
    model = _load_model()
    if model is None:
        return None
    try:
        img = _open_image(source)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Could not open image for embedding: %s", exc)
        return None
    vec = model.encode(img, normalize_embeddings=True, convert_to_numpy=True)
    return _np().asarray(vec, dtype=_np().float32)


def _to_bytes(vec):
    return _np().asarray(vec, dtype=_np().float32).tobytes()


def _from_bytes(blob):
    return _np().frombuffer(blob, dtype=_np().float32)


def _static_path(image_path):
    """Map a product image_path (relative to /static) to a filesystem path."""
    from flask import current_app
    return os.path.join(current_app.root_path, "static", image_path)


# --------------------------------------------------------------------------
# embedding maintenance
# --------------------------------------------------------------------------
def embed_product(product):
    """Encode the product's primary image into a `ProductEmbedding` row.

    Returns the row, or None when the product has no readable image / the
    model is unavailable. Caller commits.
    """
    if product is None or not product.primary_image:
        return None
    file_path = _static_path(product.primary_image)
    if not os.path.exists(file_path):
        return None
    vec = encode_image(file_path)
    if vec is None:
        return None

    row = ProductEmbedding.query.filter_by(product_id=product.id).first()
    if row is None:
        row = ProductEmbedding(product_id=product.id)
        db.session.add(row)
    row.embedding = _to_bytes(vec)
    row.image_path = product.primary_image
    return row


def embed_all_published(verbose=False):
    """Backfill embeddings for every published product. Returns (done, skipped).

    Caller commits.
    """
    products = Product.query.filter_by(status=PRODUCT_PUBLISHED).all()
    done = skipped = 0
    for p in products:
        row = embed_product(p)
        if row is None:
            skipped += 1
        else:
            done += 1
        if verbose:
            print(f"  {p.slug}: {'embedded' if row else 'skipped'}")
    return done, skipped


# --------------------------------------------------------------------------
# search
# --------------------------------------------------------------------------
def search_by_image(image_source, limit=12):
    """Top visually-similar published products.

    Returns ``[(product, similarity), ...]``, highest similarity first.
    """
    query_vec = encode_image(image_source)
    if query_vec is None:
        return []

    rows = (
        db.session.query(ProductEmbedding, Product)
        .join(Product, Product.id == ProductEmbedding.product_id)
        .filter(Product.status == PRODUCT_PUBLISHED).all()
    )
    if not rows:
        return []

    np = _np()
    matrix = np.stack([_from_bytes(emb.embedding) for emb, _ in rows])
    # Unit-norm vectors → cosine similarity == dot product.
    sims = matrix @ query_vec
    top = np.argsort(-sims)[:limit]
    return [(rows[i][1], float(sims[i])) for i in top]
