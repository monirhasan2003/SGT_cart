"""Legal / Policy / Help / Seller-resource pages — Phase 15 footer
documentation Wave 1.

`pages.py` continues to own the original public-page slugs (terms, privacy,
returns, shipping, contact, about, faq, sell). This blueprint adds the
NEW Wave-1 slugs that didn't exist before.

Each route is a thin view: passes page_title, page_section, page_contact
into the shared `_layout.html` shell. Real content lives in the
corresponding Jinja template under `pages/static/`.

Master plan: `SGT_Ecommerce/FOOTER_LEGAL_MASTER_PLAN.md`.
"""
from flask import Blueprint, render_template

legal = Blueprint("legal", __name__)

# slug → (title, section, contact, template_file)
_PAGES = {
    # ---- D · Legal (new) ----
    "seller-terms":         ("Seller Agreement",                 "Legal",
                             "policy@sgtcart.com",      "seller_terms.html"),
    "cookie-policy":        ("Cookie Policy",                    "Legal",
                             "privacy@sgtcart.com",     "cookies.html"),
    "ip-policy":            ("Intellectual Property Policy",     "Legal",
                             "ip-takedown@sgtcart.com", "ip_policy.html"),
    "dispute-resolution":   ("Dispute Resolution & Arbitration", "Legal",
                             "disputes@sgtcart.com",    "dispute_resolution.html"),

    # ---- E · Trust & policy detail (new) ----
    "refund-policy":        ("Refund Policy",                    "Trust & Safety",
                             "support@sgtcart.com",     "refund_policy.html"),

    # ---- B · Customer Help (new sub-paths) ----
    "help-payment-methods": ("Payment Methods",                  "Customer Help",
                             "support@sgtcart.com",     "payment_methods.html"),
    "help-cancellations":   ("Order Cancellation",               "Customer Help",
                             "support@sgtcart.com",     "cancellations.html"),
    "help-buyer-protection":("Buyer Protection Program",         "Customer Help",
                             "support@sgtcart.com",     "buyer_protection.html"),

    # ---- C · Seller resources (new sub-paths) ----
    "sell-onboarding":      ("Seller Onboarding Guide",          "Seller Resources",
                             "seller-support@sgtcart.com", "seller_onboarding.html"),
    "sell-fees":            ("Seller Fees & Commission",         "Seller Resources",
                             "seller-support@sgtcart.com", "seller_fees.html"),
    "sell-listing-guidelines":("Product Listing Guidelines",     "Seller Resources",
                             "seller-support@sgtcart.com", "seller_listing_guidelines.html"),
}

# slug → URL path (defaults to /<slug>/ when not in this map).
_PATHS = {
    "help-payment-methods":   "/help/payment-methods/",
    "help-cancellations":     "/help/cancellations/",
    "help-buyer-protection":  "/help/buyer-protection/",
    "sell-onboarding":        "/sell/onboarding/",
    "sell-fees":              "/sell/fees/",
    "sell-listing-guidelines":"/sell/listing-guidelines/",
}


def _make_view(slug, title, section, contact, template):
    def view():
        return render_template(
            f"pages/static/{template}",
            slug=slug, page_title=title, page_section=section,
            page_contact=contact, page_version="v1.0",
            page_reviewed_at="24 May 2026",
        )
    view.__name__ = f"legal_{slug.replace('-', '_')}"
    return view


for _slug, (_title, _section, _contact, _template) in _PAGES.items():
    legal.add_url_rule(
        _PATHS.get(_slug, f"/{_slug}/"),
        endpoint=_slug,
        view_func=_make_view(_slug, _title, _section, _contact, _template),
    )
