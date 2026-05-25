"""District delivery ETAs — Phase 15 D-9 B1.

A small lookup table the storefront consults to show realistic delivery
windows like "Dhaka: 1-2 days, Sylhet: 4-5 days" in the product page's
Delivery sidebar. Seeded by the `seed-district-eta` CLI command; admin
edits can come later if needed.
"""
from app.extensions import db


class DistrictEta(db.Model):
    __tablename__ = "district_etas"

    id = db.Column(db.Integer, primary_key=True)
    # Matched case-insensitively against the buyer's saved-address city or
    # district (BD addresses use both interchangeably).
    district = db.Column(db.String(80), unique=True, nullable=False, index=True)
    min_days = db.Column(db.Integer, nullable=False, default=1)
    max_days = db.Column(db.Integer, nullable=False, default=3)

    def __repr__(self):
        return f"<DistrictEta {self.district} {self.min_days}-{self.max_days}d>"
