"""Static informational pages — About, Contact, FAQ, Privacy, Terms,
Returns, Shipping, and the public "Sell on SGT" landing.

The page bodies live in `templates/pages/static/`; an admin can edit those
files in-repo without code changes.
"""
from flask import Blueprint, render_template

pages = Blueprint("pages", __name__)

# Each entry: slug -> (heading, section, contact-email, template).
# All pages now extend the upgraded `_layout.html` shell (ToC, FAQ,
# contact card, version footer). Phase 15 footer Wave 1.
_PAGES = {
    "about":    ("About SGT Cart",           "Company",
                 "support@sgtcart.com",  "about.html"),
    "contact":  ("Contact Us",               "Company",
                 "support@sgtcart.com",  "contact.html"),
    "faq":      ("Frequently Asked Questions", "Customer Help",
                 "support@sgtcart.com",  "faq.html"),
    "privacy":  ("Privacy Policy",           "Legal",
                 "privacy@sgtcart.com",  "privacy.html"),
    "terms":    ("Customer Terms of Service","Legal",
                 "policy@sgtcart.com",   "terms.html"),
    "returns":  ("Returns & Refunds",        "Customer Help",
                 "support@sgtcart.com",  "returns.html"),
    "shipping": ("Shipping & Delivery",      "Customer Help",
                 "support@sgtcart.com",  "shipping.html"),
    "sell":     ("Sell on SGT Cart",         "Seller Resources",
                 "seller-support@sgtcart.com", "sell.html"),
}


def _make_view(slug, title, section, contact, template):
    def view():
        return render_template(
            f"pages/static/{template}",
            slug=slug, page_title=title, page_section=section,
            page_contact=contact, page_version="v1.0",
            page_reviewed_at="24 May 2026",
        )
    view.__name__ = f"page_{slug}"
    return view


for _slug, (_title, _section, _contact, _template) in _PAGES.items():
    pages.add_url_rule(
        f"/{_slug}/", endpoint=_slug,
        view_func=_make_view(_slug, _title, _section, _contact, _template),
    )
