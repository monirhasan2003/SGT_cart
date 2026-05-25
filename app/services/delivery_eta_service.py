"""District-wise delivery ETA — Phase 15 D-9 B1.

Falls back to a platform-default window when the buyer's saved-address
city is unknown. The product page's Delivery sidebar consults this to
show "Dhaka: 1-2 days" instead of the generic "1-5 days" from D-1.
"""
from app.models.district import DistrictEta

DEFAULT_MIN = 1
DEFAULT_MAX = 5


def _normalize(name):
    return (name or "").strip().lower()


def eta_for_district(district_name):
    """Return ``(min_days, max_days, matched_district_or_None)``.

    Looks up a `DistrictEta` row case-insensitively. Returns the platform
    default + None match when nothing is configured or the input is blank.
    """
    name = _normalize(district_name)
    if not name:
        return DEFAULT_MIN, DEFAULT_MAX, None
    row = DistrictEta.query.filter(
        DistrictEta.district.ilike(name)
    ).first()
    if row is None:
        return DEFAULT_MIN, DEFAULT_MAX, None
    return row.min_days, row.max_days, row.district


def eta_for_address(address):
    """Pick the best district name off the buyer's address (district >
    city). Returns the same tuple as `eta_for_district`.
    """
    if address is None:
        return DEFAULT_MIN, DEFAULT_MAX, None
    candidate = address.district or address.city
    return eta_for_district(candidate)


SEED_DISTRICTS = [
    ("Dhaka", 1, 2),
    ("Chittagong", 3, 4),
    ("Sylhet", 4, 5),
    ("Khulna", 3, 4),
    ("Rajshahi", 4, 5),
    ("Barisal", 4, 6),
    ("Rangpur", 5, 7),
    ("Mymensingh", 3, 5),
    ("Comilla", 3, 4),
    ("Narayanganj", 1, 2),
    ("Gazipur", 1, 2),
    ("Cox's Bazar", 4, 6),
]
