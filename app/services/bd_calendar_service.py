"""BD calendar helpers — Phase 15 D-9 B6.

* `hijri_from_gregorian(date)` — converts a `datetime.date` to a
  ``(year, month, day, month_name_en)`` tuple using the Kuwaiti (tabular
  Islamic) algorithm. Accurate to ±1 day vs the Saudi sighting calendar
  — good enough for the "৪ Ramadan / 14 March" surface.
* `bengali_digits(n)` — render an integer with Bengali-Indic digits.
* `format_hijri_and_gregorian(date)` — convenience for the product page.

No external dependency on purpose: a one-day off-by-one for the Hijri
display is not worth adding a package over.
"""
from datetime import date as date_cls
from datetime import datetime

HIJRI_MONTHS = (
    "Muharram", "Safar", "Rabi al-Awwal", "Rabi al-Thani",
    "Jumada al-Awwal", "Jumada al-Thani", "Rajab", "Sha'ban",
    "Ramadan", "Shawwal", "Dhu al-Qi'dah", "Dhu al-Hijjah",
)

_BN_DIGITS = "০১২৩৪৫৬৭৮৯"


def bengali_digits(n):
    """Render `n` (int or string) with Bengali-Indic digits."""
    return "".join(_BN_DIGITS[int(c)] if c.isdigit() else c for c in str(n))


def hijri_from_gregorian(d):
    """Kuwaiti algorithm — gregorian `datetime.date` -> Hijri tuple."""
    if isinstance(d, datetime):
        d = d.date()
    if not isinstance(d, date_cls):
        raise TypeError("hijri_from_gregorian expects a date or datetime")
    g_year, g_month, g_day = d.year, d.month, d.day

    jd = (
        int((1461 * (g_year + 4800 + (g_month - 14) // 12)) / 4)
        + int((367 * (g_month - 2 - 12 * ((g_month - 14) // 12))) / 12)
        - int((3 * ((g_year + 4900 + (g_month - 14) // 12) // 100)) / 4)
        + g_day
        - 32075
    )
    l = jd - 1948440 + 10632
    n = (l - 1) // 10631
    l = l - 10631 * n + 354
    j = (
        ((10985 - l) // 5316) * ((50 * l) // 17719)
        + (l // 5670) * ((43 * l) // 15238)
    )
    l = (
        l
        - ((30 - j) // 15) * ((17719 * j) // 50)
        - (j // 16) * ((15238 * j) // 43)
        + 29
    )
    h_month = (24 * l) // 709
    h_day = l - (709 * h_month) // 24
    h_year = 30 * n + j - 30

    month_name = HIJRI_MONTHS[h_month - 1] if 1 <= h_month <= 12 else "?"
    return h_year, h_month, h_day, month_name


def format_hijri_and_gregorian(d):
    """Return a Daraz-style label: '৪ Ramadan / 14 March'."""
    if d is None:
        return ""
    _, _, h_day, month_en = hijri_from_gregorian(d)
    g = d if isinstance(d, date_cls) else d.date()
    return f"{bengali_digits(h_day)} {month_en} / {g.day} {g.strftime('%B')}"
