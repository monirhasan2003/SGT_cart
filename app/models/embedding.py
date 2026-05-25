"""Product image embeddings — Phase 10 Chunk C.

A CLIP image embedding is a 512-float vector that places an image in a
semantic space; visually similar products land close to each other. The
vector is stored as raw little-endian float32 bytes for compactness
(~2 KB per product) and similarity is computed in Python (cosine).

When pgvector becomes available later, swapping `embedding` to a
`Vector(512)` column is the only schema change needed.
"""
from datetime import datetime

from app.extensions import db


class ProductEmbedding(db.Model):
    """One CLIP image embedding per product (its primary image)."""

    __tablename__ = "product_embeddings"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"),
        unique=True, nullable=False, index=True,
    )
    # 512 float32 values packed as little-endian bytes (~2 KB).
    embedding = db.Column(db.LargeBinary, nullable=False)
    # Which image produced this embedding — re-embed if the primary changes.
    image_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = db.relationship(
        "Product",
        backref=db.backref("embedding", uselist=False,
                           cascade="all, delete-orphan"),
    )

    def __repr__(self):
        return f"<ProductEmbedding product={self.product_id}>"
