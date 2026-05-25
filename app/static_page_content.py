"""Seed content for the 16 footer URLs that returned 404 before Phase 15
made StaticPage admin-editable.

These dicts are consumed by `flask seed-static-pages` and stored in the
`static_pages` table. Admins can edit any of them from
`/admin/static-pages/` without touching code.

Slug == full URL path without leading/trailing slashes. So:
  help/how-to-order  -> /help/how-to-order/
  sell/payouts       -> /sell/payouts/
  careers            -> /careers/
"""

FOOTER_PAGES = [
    # ----------------------------------------------------------------
    # /help/ — Customer help hub
    # ----------------------------------------------------------------
    {
        "slug": "help",
        "title": "Help Center",
        "subtitle": "Find quick answers and contact channels for every part of your SGT Cart experience.",
        "section": "Customer Help",
        "contact_email": "support@sgtcart.com",
        "sort_order": 1,
        "toc": [
            {"anchor": "ordering", "label": "Ordering"},
            {"anchor": "payments", "label": "Payments"},
            {"anchor": "delivery", "label": "Delivery"},
            {"anchor": "returns",  "label": "Returns & refunds"},
            {"anchor": "account",  "label": "Account & security"},
        ],
        "body_html": """
<p class="lead small">Browse the most common topics, or scroll down for our
full self-service library. If you can't find what you need, our team
replies on email within 1 business day.</p>

<h2 id="ordering">Ordering</h2>
<ul>
  <li><a href="/help/how-to-order/">How to place an order</a></li>
  <li><a href="/help/cancellations/">Cancelling an order</a></li>
  <li><a href="/shipping/">Delivery times &amp; charges</a></li>
</ul>

<h2 id="payments">Payments</h2>
<ul>
  <li><a href="/help/payment-methods/">Accepted payment methods</a></li>
  <li><a href="/help/buyer-protection/">Buyer Protection Program</a></li>
  <li><a href="/refund-policy/">Refund policy</a></li>
</ul>

<h2 id="delivery">Delivery</h2>
<ul>
  <li><a href="/shipping/">Shipping zones &amp; ETAs</a></li>
  <li><a href="/returns/">Return shipments</a></li>
</ul>

<h2 id="returns">Returns &amp; refunds</h2>
<p>Most items can be returned within 7 days of delivery. See the full
<a href="/returns/">Returns &amp; Refunds</a> policy.</p>

<h2 id="account">Account &amp; security</h2>
<p>Forgot your password? Use the "Forgot password" link on the
<a href="/auth/login">sign-in page</a>. For anything else, contact
<a href="mailto:support@sgtcart.com">support@sgtcart.com</a>.</p>
""",
        "faq": [
            {"q": "How do I track my order?",
             "a": "Sign in and open <a href='/account/orders/'>My Orders</a>. Each item shows its current status — Processing, Shipped, or Delivered."},
            {"q": "What if my item arrives damaged?",
             "a": "Open the order in your account and click 'Request return'. We approve refunds within 2 business days after the courier returns the item to the seller."},
        ],
        "related": [
            {"href": "/help/how-to-order/", "title": "How to order",
             "desc": "Step-by-step guide for first-time buyers."},
            {"href": "/help/payment-methods/", "title": "Payment methods",
             "desc": "Cards, COD, mobile wallets, bank transfer."},
            {"href": "/contact/", "title": "Contact us",
             "desc": "Phone, WhatsApp, email — every channel."},
        ],
    },

    # ----------------------------------------------------------------
    # /help/how-to-order/
    # ----------------------------------------------------------------
    {
        "slug": "help/how-to-order",
        "title": "How to Order",
        "subtitle": "From browse to delivery — a five-minute walkthrough.",
        "section": "Customer Help",
        "contact_email": "support@sgtcart.com",
        "sort_order": 2,
        "toc": [
            {"anchor": "find",     "label": "1. Find a product"},
            {"anchor": "cart",     "label": "2. Add to cart"},
            {"anchor": "checkout", "label": "3. Checkout"},
            {"anchor": "pay",      "label": "4. Pay or choose COD"},
            {"anchor": "track",    "label": "5. Track your order"},
        ],
        "body_html": """
<h2 id="find">1. Find a product</h2>
<p>Use the top search bar, browse the category menu, or open the
homepage carousel. Click any product card to open the product page —
you'll see photos, specs, seller, reviews, and a stock indicator.</p>

<h2 id="cart">2. Add to cart</h2>
<p>Choose a variant (size, colour, etc. if applicable), pick the
quantity, and click <strong>Add to Cart</strong>. You can keep
shopping; the cart icon at the top right shows your total.</p>

<h2 id="checkout">3. Checkout</h2>
<p>Open the cart, review your items, and click <strong>Proceed to
Checkout</strong>. You'll be asked to sign in or create an account if
you haven't already. Enter the delivery address — we deliver to every
district in Bangladesh.</p>

<h2 id="pay">4. Pay or choose Cash on Delivery</h2>
<p>Pick a payment method on the checkout page. We accept Visa,
Mastercard, bKash, Nagad, Rocket, and Cash on Delivery
(<a href="/help/payment-methods/">full list</a>).</p>

<h2 id="track">5. Track your order</h2>
<p>You'll receive an email confirmation and SMS update each time the
order status changes. Open
<a href="/account/orders/">My Orders</a> any time to see live status.</p>

<blockquote>Tip: Bookmark <a href="/help/">/help/</a> — every
customer-facing policy and how-to article is one click from there.</blockquote>
""",
        "faq": [
            {"q": "Do I need an account to order?",
             "a": "Yes — an account lets us send tracking updates and resolve any issues. Sign-up takes 30 seconds."},
            {"q": "Can I order multiple items from different sellers?",
             "a": "Absolutely. Each seller ships their items independently — you'll get separate tracking for each sub-order."},
        ],
        "related": [
            {"href": "/help/payment-methods/", "title": "Payment methods",
             "desc": "Cards, COD, mobile wallets."},
            {"href": "/help/cancellations/", "title": "Cancellations",
             "desc": "Before & after dispatch."},
            {"href": "/help/buyer-protection/", "title": "Buyer Protection",
             "desc": "How your purchase is safeguarded."},
        ],
    },

    # ----------------------------------------------------------------
    # /sell/payouts/
    # ----------------------------------------------------------------
    {
        "slug": "sell/payouts",
        "title": "Seller Payouts",
        "subtitle": "How and when SGT Cart settles your earnings.",
        "section": "Seller Resources",
        "contact_email": "seller-support@sgtcart.com",
        "sort_order": 10,
        "toc": [
            {"anchor": "cycle",   "label": "Settlement cycle"},
            {"anchor": "methods", "label": "Payout methods"},
            {"anchor": "fees",    "label": "Fees deducted"},
            {"anchor": "hold",    "label": "Hold &amp; reserve"},
            {"anchor": "issues",  "label": "Payout issues"},
        ],
        "body_html": """
<h2 id="cycle">Settlement cycle</h2>
<p>SGT Cart settles seller payouts on a <strong>weekly cycle</strong>.
Orders that are <em>Delivered</em> and have passed the 7-day return
window become eligible for payout the following Monday. Funds are
released as a single transfer to your registered payout account by
Wednesday end-of-day.</p>

<h2 id="methods">Payout methods</h2>
<ul>
  <li><strong>Bank transfer (BEFTN)</strong> — any Bangladesh-licensed bank.</li>
  <li><strong>bKash Merchant</strong> — instant for amounts under ৳25,000.</li>
  <li><strong>Nagad Business</strong> — daily settlement.</li>
</ul>
<p>Add or update your payout details in the
<a href="/seller/wallet/">Seller Wallet</a> page after admin approval.</p>

<h2 id="fees">Fees deducted</h2>
<p>Your payout is calculated as:</p>
<p><code>(item total + shipping fee paid by buyer) − category commission
− payment-gateway fee − any refund or chargeback</code></p>
<p>See <a href="/sell/fees/">Seller Fees &amp; Commission</a> for the
exact percentages by category.</p>

<h2 id="hold">Hold &amp; reserve</h2>
<p>SGT Cart may temporarily reserve up to 10% of weekly settlements
during the first 30 days of a new shop, or after any disputed
transaction, to cover potential buyer refunds. The reserve is
automatically released once outstanding issues are resolved.</p>

<h2 id="issues">Payout issues</h2>
<p>If a payout is delayed, email
<a href="mailto:seller-support@sgtcart.com">seller-support@sgtcart.com</a>
with your shop name and the settlement week. We respond within
1 business day.</p>
""",
        "faq": [
            {"q": "Why is my first payout delayed?",
             "a": "New sellers go through a 14-day verification period — payouts begin the Monday after that window closes."},
            {"q": "Can I change my payout bank account?",
             "a": "Yes, but a 48-hour cool-off applies before the new account becomes active, for fraud-protection reasons."},
        ],
        "related": [
            {"href": "/sell/fees/", "title": "Fees & commission",
             "desc": "Category-wise commission rates."},
            {"href": "/sell/onboarding/", "title": "Seller onboarding",
             "desc": "Open your shop in 1-2 days."},
            {"href": "/seller-terms/", "title": "Seller agreement",
             "desc": "The legal framework you accept."},
        ],
    },

    # ----------------------------------------------------------------
    # /sell/prohibited-items/
    # ----------------------------------------------------------------
    {
        "slug": "sell/prohibited-items",
        "title": "Prohibited Items",
        "subtitle": "Categories of products you cannot list on SGT Cart.",
        "section": "Seller Resources",
        "contact_email": "policy@sgtcart.com",
        "sort_order": 11,
        "toc": [
            {"anchor": "illegal",    "label": "Illegal goods"},
            {"anchor": "regulated",  "label": "Regulated items"},
            {"anchor": "restricted", "label": "Restricted categories"},
            {"anchor": "ip",         "label": "IP-infringing items"},
            {"anchor": "enforcement","label": "Enforcement"},
        ],
        "body_html": """
<h2 id="illegal">Illegal goods</h2>
<p>The following are <strong>never allowed</strong> on SGT Cart:</p>
<ul>
  <li>Narcotics, controlled drugs, and drug paraphernalia.</li>
  <li>Firearms, ammunition, explosives, and replica weapons.</li>
  <li>Stolen goods, counterfeit currency, or fraudulent documents.</li>
  <li>Human remains, body parts, or trafficked wildlife.</li>
  <li>Content that sexualises minors or promotes terrorism.</li>
</ul>

<h2 id="regulated">Regulated items</h2>
<p>These require special licensing — DM
<a href="mailto:policy@sgtcart.com">policy@sgtcart.com</a> before
listing:</p>
<ul>
  <li>Prescription medicines and medical devices.</li>
  <li>Alcohol and tobacco.</li>
  <li>Pesticides, industrial chemicals.</li>
  <li>Live animals (only registered breeders/sellers).</li>
</ul>

<h2 id="restricted">Restricted categories</h2>
<ul>
  <li>Used cosmetics, undergarments, or intimate items.</li>
  <li>Used child car seats or infant safety equipment.</li>
  <li>Foreign currency exchange.</li>
  <li>Adult content of any kind.</li>
  <li>Items requiring cold-chain shipping (without an approved courier).</li>
</ul>

<h2 id="ip">IP-infringing items</h2>
<p>Counterfeit branded products, unauthorised replicas, and bootleg
media are removed on first detection. See our
<a href="/ip-policy/">Intellectual Property Policy</a>.</p>

<h2 id="enforcement">Enforcement</h2>
<p>Violations result in: removal of the listing, a strike on your
account, and — for repeat or severe offences — permanent shop closure
and forfeiture of the wallet balance to cover buyer refunds. We
co-operate with Bangladesh law enforcement when required.</p>
""",
        "faq": [
            {"q": "I sell herbal supplements — are those allowed?",
             "a": "Yes, if they are DGDA-registered. Upload the registration certificate in your seller dashboard before listing."},
            {"q": "What about second-hand electronics?",
             "a": "Allowed, with the 'Used / Refurbished' badge applied. Falsely listing a used item as new is treated as fraud."},
        ],
        "related": [
            {"href": "/ip-policy/", "title": "IP policy",
             "desc": "Trademark & copyright takedowns."},
            {"href": "/seller-terms/", "title": "Seller agreement",
             "desc": "Full legal terms."},
            {"href": "/sell/code-of-conduct/", "title": "Code of conduct",
             "desc": "How we expect sellers to behave."},
        ],
    },

    # ----------------------------------------------------------------
    # /sell/seller-protection/
    # ----------------------------------------------------------------
    {
        "slug": "sell/seller-protection",
        "title": "Seller Protection",
        "subtitle": "How SGT Cart shields honest sellers from chargebacks and bad-faith claims.",
        "section": "Seller Resources",
        "contact_email": "seller-support@sgtcart.com",
        "sort_order": 12,
        "toc": [
            {"anchor": "what",        "label": "What's protected"},
            {"anchor": "requirements","label": "Eligibility"},
            {"anchor": "process",     "label": "Claim process"},
            {"anchor": "excluded",    "label": "Not covered"},
        ],
        "body_html": """
<h2 id="what">What's protected</h2>
<p>If a buyer files a dispute and you've followed every step below,
SGT Cart covers the loss instead of passing it through to you:</p>
<ul>
  <li>"Item not received" claims when courier proof-of-delivery is on file.</li>
  <li>"Item significantly not as described" claims that are objectively
  refuted by your published listing (photos, specs, dimensions).</li>
  <li>Buyer refusal to accept a Cash-on-Delivery package after dispatch
  (we waive the return-leg shipping charge twice per month).</li>
</ul>

<h2 id="requirements">Eligibility</h2>
<ol>
  <li>The shop is in <em>Active</em> status with no open policy violations.</li>
  <li>The order shipped via an SGT-approved courier (signed POD captured).</li>
  <li>The listing accurately matched the delivered item — photos,
  specs, and condition.</li>
  <li>You responded to the buyer within 24 hours of the dispute
  opening.</li>
</ol>

<h2 id="process">Claim process</h2>
<p>Disputes open automatically in the
<a href="/seller/disputes/">Disputes</a> tab. Reply with evidence
(courier slip, packaging photos, chat history). Our team adjudicates
within 5 business days, applying the
<a href="/dispute-resolution/">dispute-resolution policy</a>.</p>

<h2 id="excluded">Not covered</h2>
<ul>
  <li>Listings flagged for IP infringement or counterfeit goods.</li>
  <li>Shops with three or more open policy strikes.</li>
  <li>Self-shipped orders that bypassed SGT's approved couriers.</li>
  <li>Custom / made-to-order items unless explicitly insured.</li>
</ul>
""",
        "faq": [
            {"q": "How long after dispatch does protection apply?",
             "a": "Up to 30 days from the courier scan-out date, or 7 days after delivery — whichever is earlier."},
            {"q": "Do I need to pay anything to enrol?",
             "a": "No. Seller Protection is included with every active SGT Cart shop at no extra cost."},
        ],
        "related": [
            {"href": "/dispute-resolution/", "title": "Dispute resolution",
             "desc": "How we adjudicate buyer-seller conflicts."},
            {"href": "/sell/code-of-conduct/", "title": "Code of conduct",
             "desc": "Seller behaviour expectations."},
            {"href": "/sell/payouts/", "title": "Payouts",
             "desc": "How wins are credited."},
        ],
    },

    # ----------------------------------------------------------------
    # /sell/code-of-conduct/
    # ----------------------------------------------------------------
    {
        "slug": "sell/code-of-conduct",
        "title": "Seller Code of Conduct",
        "subtitle": "The professional standards every SGT Cart seller agrees to.",
        "section": "Seller Resources",
        "contact_email": "policy@sgtcart.com",
        "sort_order": 13,
        "toc": [
            {"anchor": "honesty",    "label": "Honesty in listings"},
            {"anchor": "service",    "label": "Service standards"},
            {"anchor": "behaviour",  "label": "Communication"},
            {"anchor": "competition","label": "Fair competition"},
            {"anchor": "consequences","label": "Consequences"},
        ],
        "body_html": """
<h2 id="honesty">Honesty in listings</h2>
<ul>
  <li>Use your own product photos or photos with proper licensing.</li>
  <li>Describe condition accurately (new, refurbished, used).</li>
  <li>Never inflate the original price to fake a discount.</li>
  <li>Disclose all variants, fees, and lead-times up-front.</li>
</ul>

<h2 id="service">Service standards</h2>
<ul>
  <li>Dispatch within the lead-time you committed to (typically 24-48 hours).</li>
  <li>Maintain on-time-delivery above 90% and order-defect rate below 2%.</li>
  <li>Reply to buyer chats within one business day.</li>
  <li>Honour the published returns policy without harassment.</li>
</ul>

<h2 id="behaviour">Communication</h2>
<p>All communication must remain on SGT Cart. Sharing phone numbers,
external links, or asking buyers to transact off-platform is a
violation — both for safety and to keep our buyer-protection programme
functional.</p>

<h2 id="competition">Fair competition</h2>
<ul>
  <li>Do not manipulate reviews on your own or competitor listings.</li>
  <li>Do not run multiple shops to circumvent strikes or bans.</li>
  <li>Do not bid up your own products or run fake-order schemes.</li>
</ul>

<h2 id="consequences">Consequences</h2>
<p>Three strikes within 12 months → 30-day suspension. Severe
violations (IP theft, fraud, repeated buyer harassment) → permanent
shop closure. We follow the appeal process described in
<a href="/dispute-resolution/">Dispute Resolution</a>.</p>
""",
        "related": [
            {"href": "/seller-terms/", "title": "Seller agreement",
             "desc": "The binding legal terms."},
            {"href": "/sell/prohibited-items/", "title": "Prohibited items",
             "desc": "What you cannot list."},
            {"href": "/sell/seller-protection/", "title": "Seller protection",
             "desc": "When SGT Cart absorbs the loss."},
        ],
    },

    # ----------------------------------------------------------------
    # /accessibility/
    # ----------------------------------------------------------------
    {
        "slug": "accessibility",
        "title": "Accessibility Statement",
        "subtitle": "Our commitment to making SGT Cart usable by everyone.",
        "section": "Company",
        "contact_email": "accessibility@sgtcart.com",
        "sort_order": 20,
        "toc": [
            {"anchor": "commitment", "label": "Our commitment"},
            {"anchor": "standards",  "label": "Standards we follow"},
            {"anchor": "features",   "label": "Accessibility features"},
            {"anchor": "feedback",   "label": "Feedback & assistance"},
        ],
        "body_html": """
<h2 id="commitment">Our commitment</h2>
<p>SGT Cart is built and maintained as a marketplace that everyone in
Bangladesh can use — including people who rely on assistive technology
or have low-bandwidth connections. We treat accessibility as an
ongoing engineering priority, not a one-off audit.</p>

<h2 id="standards">Standards we follow</h2>
<p>We target <strong>WCAG 2.1 Level AA</strong> for the web storefront
and the seller dashboard. Where individual pages fall short, we
prioritise fixes based on user impact.</p>

<h2 id="features">Accessibility features</h2>
<ul>
  <li>Keyboard navigation across every interactive control.</li>
  <li>Visible focus indicators on links, buttons, and form fields.</li>
  <li>Image alt-text on product photos (we ask sellers to provide it
  too).</li>
  <li>Sufficient colour contrast on body copy and primary actions.</li>
  <li>Bangla and English language toggle on every page.</li>
  <li>Mobile-first responsive layout that reflows down to 320 px wide.</li>
</ul>

<h2 id="feedback">Feedback &amp; assistance</h2>
<p>If you hit a barrier on any page, email
<a href="mailto:accessibility@sgtcart.com">accessibility@sgtcart.com</a>
with the page URL and what didn't work. We aim to acknowledge within
2 business days and fix within 30 days for issues that block use.</p>
""",
        "related": [
            {"href": "/contact/", "title": "Contact us",
             "desc": "All support channels."},
            {"href": "/privacy/", "title": "Privacy",
             "desc": "How we handle your data."},
            {"href": "/help/", "title": "Help Center",
             "desc": "Self-service articles."},
        ],
    },

    # ----------------------------------------------------------------
    # /governing-law/
    # ----------------------------------------------------------------
    {
        "slug": "governing-law",
        "title": "Governing Law & Jurisdiction",
        "subtitle": "Which laws apply to disputes involving SGT Cart.",
        "section": "Legal",
        "contact_email": "legal@sgtcart.com",
        "sort_order": 21,
        "toc": [
            {"anchor": "law",      "label": "Governing law"},
            {"anchor": "venue",    "label": "Exclusive venue"},
            {"anchor": "currency", "label": "Currency"},
            {"anchor": "consumer", "label": "Consumer rights"},
        ],
        "body_html": """
<h2 id="law">Governing law</h2>
<p>All transactions on SGT Cart and the relationship between buyers,
sellers, and SGT Cart are governed by the laws of the
<strong>People's Republic of Bangladesh</strong>, without regard to
its conflict-of-law principles.</p>

<h2 id="venue">Exclusive venue</h2>
<p>Subject to the binding arbitration clause in our
<a href="/dispute-resolution/">Dispute Resolution policy</a>, any
court proceeding arising out of or relating to SGT Cart shall be
brought exclusively in the competent courts of
<strong>Dhaka, Bangladesh</strong>. Both parties consent to personal
jurisdiction there.</p>

<h2 id="currency">Currency</h2>
<p>All prices, fees, and settlements on SGT Cart are denominated in
<strong>Bangladeshi Taka (BDT, ৳)</strong>. We do not offer
multi-currency pricing or international settlement at this time.</p>

<h2 id="consumer">Consumer rights</h2>
<p>Nothing in our terms limits any non-waivable statutory rights you
have under the Bangladesh Consumer Rights Protection Act, 2009, or any
successor legislation.</p>
""",
        "related": [
            {"href": "/terms/", "title": "Customer terms",
             "desc": "The buyer-side contract."},
            {"href": "/seller-terms/", "title": "Seller agreement",
             "desc": "The seller-side contract."},
            {"href": "/dispute-resolution/", "title": "Dispute resolution",
             "desc": "Arbitration framework."},
        ],
    },

    # ----------------------------------------------------------------
    # /careers/
    # ----------------------------------------------------------------
    {
        "slug": "careers",
        "title": "Careers at SGT Cart",
        "subtitle": "Help us build Bangladesh's most trusted marketplace.",
        "section": "Company",
        "contact_email": "careers@sgtcart.com",
        "sort_order": 30,
        "toc": [
            {"anchor": "why",      "label": "Why SGT Cart"},
            {"anchor": "openings", "label": "Current openings"},
            {"anchor": "apply",    "label": "How to apply"},
            {"anchor": "internships","label": "Internships"},
        ],
        "body_html": """
<h2 id="why">Why SGT Cart</h2>
<p>SGT Cart is part of Smart Global Trade — a Bangladeshi technology
group building the digital backbone for online commerce in our home
market. We are a small, senior team that prizes craftsmanship, fast
iteration, and ownership of outcomes.</p>

<h2 id="openings">Current openings</h2>
<p>We hire continuously across the following functions. Even if no
specific role is listed, send us a strong CV — we keep good
applications on file.</p>
<ul>
  <li><strong>Engineering</strong> — Python / Flask, Flutter (mobile), DevOps.</li>
  <li><strong>Operations</strong> — Seller success, logistics, courier coordination.</li>
  <li><strong>Customer support</strong> — Bilingual (Bangla + English) chat &amp; voice.</li>
  <li><strong>Trust &amp; safety</strong> — Policy enforcement and dispute analysts.</li>
  <li><strong>Marketing</strong> — Performance, content, and brand.</li>
</ul>

<h2 id="apply">How to apply</h2>
<p>Send your CV, a short note about what you're great at, and any
links you're proud of to
<a href="mailto:careers@sgtcart.com">careers@sgtcart.com</a>. We
reply to every email — usually within 5 business days.</p>

<h2 id="internships">Internships</h2>
<p>Final-year undergraduates from Bangladeshi universities can apply
for our 3-month paid internships in engineering and operations.
Mention <em>"Internship"</em> in your subject line.</p>
""",
        "related": [
            {"href": "/about/", "title": "About us",
             "desc": "Our mission and founders."},
            {"href": "/newsroom/", "title": "Newsroom",
             "desc": "Latest announcements."},
            {"href": "/contact/", "title": "Contact",
             "desc": "Other ways to reach us."},
        ],
    },

    # ----------------------------------------------------------------
    # /newsroom/
    # ----------------------------------------------------------------
    {
        "slug": "newsroom",
        "title": "Newsroom",
        "subtitle": "Press releases, milestones, and media resources.",
        "section": "Company",
        "contact_email": "press@sgtcart.com",
        "sort_order": 31,
        "toc": [
            {"anchor": "press",    "label": "Press releases"},
            {"anchor": "kit",      "label": "Media kit"},
            {"anchor": "contact",  "label": "Press contact"},
        ],
        "body_html": """
<h2 id="press">Press releases</h2>
<p>We publish formal announcements when we hit major company
milestones — funding rounds, regulatory approvals, seller-count
records, new product launches. Subscribe to the newsroom RSS feed or
email <a href="mailto:press@sgtcart.com">press@sgtcart.com</a> to be
added to our distribution list.</p>

<p><em>No public releases yet — we're launching with this version of
the site. Check back here for updates.</em></p>

<h2 id="kit">Media kit</h2>
<p>Need our logo, brand colours, or executive photography? Email
<a href="mailto:press@sgtcart.com">press@sgtcart.com</a> and we'll
share the asset bundle (logos in PNG/SVG, brand-style PDF, and
high-resolution photos).</p>

<h2 id="contact">Press contact</h2>
<p>For interviews, podcast guests, or off-the-record briefings,
contact <strong>SGT Cart Communications</strong> at
<a href="mailto:press@sgtcart.com">press@sgtcart.com</a>. We respond
to journalists within 24 hours on weekdays.</p>
""",
        "related": [
            {"href": "/about/", "title": "About us",
             "desc": "Company background."},
            {"href": "/careers/", "title": "Careers",
             "desc": "Join the team."},
            {"href": "/sustainability/", "title": "Sustainability",
             "desc": "Our environmental commitments."},
        ],
    },

    # ----------------------------------------------------------------
    # /sustainability/
    # ----------------------------------------------------------------
    {
        "slug": "sustainability",
        "title": "Sustainability",
        "subtitle": "Building a marketplace that doesn't cost the planet.",
        "section": "Company",
        "contact_email": "sustainability@sgtcart.com",
        "sort_order": 32,
        "toc": [
            {"anchor": "packaging", "label": "Packaging"},
            {"anchor": "logistics", "label": "Logistics"},
            {"anchor": "supply",    "label": "Supply chain"},
            {"anchor": "future",    "label": "Looking ahead"},
        ],
        "body_html": """
<h2 id="packaging">Packaging</h2>
<p>We're working with our partner couriers to phase out single-use
plastic mailers in favour of recycled-paper alternatives. Sellers
joining our <em>Green Pack</em> programme receive subsidised compostable
packaging and a "Green Pack" badge on their listings.</p>

<h2 id="logistics">Logistics</h2>
<p>Wherever feasible we ship orders bound for the same district in
consolidated runs. Inside Dhaka we are piloting electric two-wheelers
with two of our courier partners for short-distance last-mile delivery.</p>

<h2 id="supply">Supply chain</h2>
<p>We actively reduce platform support for products with high
environmental risk — single-use vape kits, microplastic-laden glitter
craft kits, and disposable thin-film fashion items. We encourage
sellers in those categories to offer refillable or higher-quality
alternatives.</p>

<h2 id="future">Looking ahead</h2>
<p>By 2028 we aim to:</p>
<ul>
  <li>Power all SGT Cart-operated warehouses with rooftop solar
  (target: 60% on-site generation).</li>
  <li>Publish an annual sustainability report co-signed with our top
  10 courier &amp; warehousing partners.</li>
  <li>Offer carbon-neutral checkout as a default for every order.</li>
</ul>
<p>This is an honest "in-progress" page — we will not greenwash. As
real numbers are available we'll publish them here.</p>
""",
        "related": [
            {"href": "/about/", "title": "About us",
             "desc": "Company background."},
            {"href": "/trust-safety/", "title": "Trust & safety",
             "desc": "Marketplace integrity."},
            {"href": "/transparency/", "title": "Transparency",
             "desc": "Reporting commitments."},
        ],
    },

    # ----------------------------------------------------------------
    # /trust-safety/
    # ----------------------------------------------------------------
    {
        "slug": "trust-safety",
        "title": "Trust & Safety",
        "subtitle": "How we keep buyers, sellers, and the platform safe.",
        "section": "Trust & Safety",
        "contact_email": "trust@sgtcart.com",
        "sort_order": 40,
        "toc": [
            {"anchor": "pillars",     "label": "Our four pillars"},
            {"anchor": "moderation",  "label": "Content moderation"},
            {"anchor": "fraud",       "label": "Fraud prevention"},
            {"anchor": "report",      "label": "Report a concern"},
        ],
        "body_html": """
<h2 id="pillars">Our four pillars</h2>
<ol>
  <li><strong>Genuine sellers.</strong> Every shop is verified before
  publishing — National ID, trade license, and bank account checks.</li>
  <li><strong>Honest listings.</strong> Automated checks plus human
  review for high-risk categories, plus instant takedown for
  counterfeit goods.</li>
  <li><strong>Safe transactions.</strong> Encrypted payments, escrowed
  COD reconciliation, and 7-day return windows.</li>
  <li><strong>Respectful communities.</strong> Reviews, Q&amp;A, and
  chat are all moderated against our
  <a href="/sell/code-of-conduct/">code of conduct</a>.</li>
</ol>

<h2 id="moderation">Content moderation</h2>
<p>We combine ML classifiers, keyword filters, and human review.
Listings flagged for prohibited goods are taken offline within
4 hours; appeals are reviewed in 48 hours.</p>

<h2 id="fraud">Fraud prevention</h2>
<p>SGT Cart's risk engine watches for orders with suspicious payment
patterns, repeat-chargeback buyers, and seller activity that looks
like wash-trading. Decisions are explainable — both buyers and sellers
get a reason for any restriction.</p>

<h2 id="report">Report a concern</h2>
<p>Spotted something? File a quick report at
<a href="/report-illegal/">/report-illegal/</a> or email
<a href="mailto:trust@sgtcart.com">trust@sgtcart.com</a>. Critical
safety reports are triaged within 1 hour.</p>
""",
        "related": [
            {"href": "/transparency/", "title": "Transparency",
             "desc": "Reports & disclosures."},
            {"href": "/anti-counterfeit/", "title": "Anti-counterfeit",
             "desc": "Brand protection programme."},
            {"href": "/report-illegal/", "title": "Report illegal content",
             "desc": "Open a safety report."},
        ],
    },

    # ----------------------------------------------------------------
    # /transparency/
    # ----------------------------------------------------------------
    {
        "slug": "transparency",
        "title": "Transparency",
        "subtitle": "Annual disclosures, take-down stats, and government request logs.",
        "section": "Trust & Safety",
        "contact_email": "transparency@sgtcart.com",
        "sort_order": 41,
        "toc": [
            {"anchor": "principle",  "label": "Our principle"},
            {"anchor": "takedowns",  "label": "Take-down reporting"},
            {"anchor": "requests",   "label": "Government requests"},
            {"anchor": "data",       "label": "Data access logs"},
        ],
        "body_html": """
<h2 id="principle">Our principle</h2>
<p>SGT Cart is a young company, but we commit publicly to the same
transparency standards as established global marketplaces:</p>
<ul>
  <li>An annual transparency report (first edition due
  Q1 2027).</li>
  <li>Disclosure of every government / law-enforcement request we
  receive, in aggregate.</li>
  <li>A clear appeals path for any seller or buyer affected by a
  platform decision.</li>
</ul>

<h2 id="takedowns">Take-down reporting</h2>
<p>We publish quarterly numbers on:</p>
<ul>
  <li>Listings removed for IP infringement (split by reporter type).</li>
  <li>Accounts suspended for fraud, harassment, or prohibited goods.</li>
  <li>Reviews removed for fake-review rules violations.</li>
</ul>
<p>The first quarter of reportable data covers
<strong>April-June 2026</strong> and will appear here by
1 August 2026.</p>

<h2 id="requests">Government requests</h2>
<p>SGT Cart cooperates with Bangladesh law-enforcement when presented
with a valid warrant or court order. We narrow disclosures to the
minimum data legally required, notify the user when permitted, and
log every request for the annual report.</p>

<h2 id="data">Data access logs</h2>
<p>Internal access to user data is restricted to the smallest possible
team and logged for review. The logs are audited quarterly by an
independent reviewer.</p>
""",
        "related": [
            {"href": "/trust-safety/", "title": "Trust & safety",
             "desc": "Marketplace integrity overview."},
            {"href": "/privacy/", "title": "Privacy policy",
             "desc": "How we use your data."},
            {"href": "/governing-law/", "title": "Governing law",
             "desc": "Applicable jurisdiction."},
        ],
    },

    # ----------------------------------------------------------------
    # /report-illegal/
    # ----------------------------------------------------------------
    {
        "slug": "report-illegal",
        "title": "Report Illegal Content",
        "subtitle": "How to alert SGT Cart to listings, content, or behaviour that violates the law.",
        "section": "Trust & Safety",
        "contact_email": "trust@sgtcart.com",
        "sort_order": 42,
        "toc": [
            {"anchor": "what",     "label": "What counts as illegal"},
            {"anchor": "how",      "label": "How to report"},
            {"anchor": "anonymous","label": "Anonymous tips"},
            {"anchor": "emergency","label": "Emergencies"},
        ],
        "body_html": """
<h2 id="what">What counts as illegal</h2>
<p>If a listing, review, message, or seller appears to involve any of
the following, please report it:</p>
<ul>
  <li>Counterfeit branded goods or pirated digital content.</li>
  <li>Weapons, ammunition, explosives, or related parts.</li>
  <li>Drugs (recreational, controlled, or unlicensed prescription).</li>
  <li>Child sexual abuse material or grooming behaviour.</li>
  <li>Trafficked goods (wildlife, antiquities, stolen vehicles, etc.).</li>
  <li>Terrorism financing or extremist content.</li>
  <li>Threats, harassment, or doxxing.</li>
</ul>

<h2 id="how">How to report</h2>
<ol>
  <li>Email <a href="mailto:trust@sgtcart.com">trust@sgtcart.com</a> with the
  URL(s), screenshots, and a short description.</li>
  <li>If you are a rights-holder reporting IP infringement, follow the
  <a href="/ip-policy/">IP Policy</a> notice format.</li>
  <li>We acknowledge within 4 hours and act within 24 hours for
  Severity-1 reports.</li>
</ol>

<h2 id="anonymous">Anonymous tips</h2>
<p>Anonymous reports are accepted, but include enough detail
(screenshots, URLs, dates) for us to investigate. We can't follow up
with you if you don't share contact information.</p>

<h2 id="emergency">Emergencies</h2>
<p>If you believe someone is in immediate physical danger, contact
Bangladesh emergency services on <strong>999</strong> first, then
notify us.</p>
""",
        "related": [
            {"href": "/trust-safety/", "title": "Trust & safety",
             "desc": "How we keep the marketplace safe."},
            {"href": "/anti-counterfeit/", "title": "Anti-counterfeit",
             "desc": "Brand protection programme."},
            {"href": "/ip-policy/", "title": "IP policy",
             "desc": "Trademark & copyright procedure."},
        ],
    },

    # ----------------------------------------------------------------
    # /anti-counterfeit/
    # ----------------------------------------------------------------
    {
        "slug": "anti-counterfeit",
        "title": "Anti-Counterfeit Programme",
        "subtitle": "How brand owners protect their IP on SGT Cart.",
        "section": "Trust & Safety",
        "contact_email": "brand-protect@sgtcart.com",
        "sort_order": 43,
        "toc": [
            {"anchor": "commitment", "label": "Our commitment"},
            {"anchor": "enrol",      "label": "Brand enrolment"},
            {"anchor": "process",    "label": "Take-down process"},
            {"anchor": "penalties",  "label": "Seller penalties"},
        ],
        "body_html": """
<h2 id="commitment">Our commitment</h2>
<p>SGT Cart does not tolerate counterfeit listings. Verified brand
owners can register with our Anti-Counterfeit Programme to get
expedited take-downs, proactive listing screening, and a direct
account manager.</p>

<h2 id="enrol">Brand enrolment</h2>
<p>To enrol, send the following to
<a href="mailto:brand-protect@sgtcart.com">brand-protect@sgtcart.com</a>:</p>
<ul>
  <li>Registered trademark certificate (Bangladesh or international,
  with WIPO designation).</li>
  <li>Proof of authority to act on behalf of the brand.</li>
  <li>A primary contact and authorised escalation list.</li>
</ul>
<p>We confirm enrolment within 5 business days.</p>

<h2 id="process">Take-down process</h2>
<ol>
  <li>Enrolled brands file take-down requests through the brand
  portal (or email until the portal launches).</li>
  <li>We action requests within <strong>24 hours</strong> for
  enrolled brands, <strong>72 hours</strong> for non-enrolled
  rights-holders.</li>
  <li>Sellers can appeal within 14 days with documented authenticity
  evidence (invoices, distributor agreements).</li>
</ol>

<h2 id="penalties">Seller penalties</h2>
<ul>
  <li><strong>First strike</strong> — listing removed, written warning.</li>
  <li><strong>Second strike</strong> — 30-day suspension, wallet hold.</li>
  <li><strong>Third strike</strong> — permanent shop closure;
  outstanding balance reserved for buyer refunds.</li>
</ul>
""",
        "related": [
            {"href": "/ip-policy/", "title": "IP policy",
             "desc": "Full takedown procedure."},
            {"href": "/trust-safety/", "title": "Trust & safety",
             "desc": "Marketplace integrity programme."},
            {"href": "/sell/code-of-conduct/", "title": "Seller code of conduct",
             "desc": "Behaviour standards."},
        ],
    },

    # ----------------------------------------------------------------
    # /security/
    # ----------------------------------------------------------------
    {
        "slug": "security",
        "title": "Security",
        "subtitle": "How SGT Cart protects accounts, payments, and platform data.",
        "section": "Trust & Safety",
        "contact_email": "security@sgtcart.com",
        "sort_order": 44,
        "toc": [
            {"anchor": "account",  "label": "Account security"},
            {"anchor": "payments", "label": "Payment security"},
            {"anchor": "platform", "label": "Platform security"},
            {"anchor": "report",   "label": "Report a vulnerability"},
        ],
        "body_html": """
<h2 id="account">Account security</h2>
<ul>
  <li>Passwords are hashed with industry-standard work-factor
  algorithms — we never store them in plain text.</li>
  <li>Sensitive actions (changing payout details, exporting data)
  require a one-time code sent to your registered email.</li>
  <li>Sessions auto-expire after a period of inactivity, and you can
  sign-out remote sessions from your account page.</li>
</ul>

<h2 id="payments">Payment security</h2>
<ul>
  <li>Card payments are processed through PCI-DSS-compliant gateways
  (SSLCommerz). SGT Cart never stores raw card numbers.</li>
  <li>All payment-page traffic is TLS-encrypted end-to-end.</li>
  <li>Suspicious payment patterns trigger automated review before
  funds are released.</li>
</ul>

<h2 id="platform">Platform security</h2>
<ul>
  <li>Production servers are isolated behind a reverse proxy with
  HSTS, modern TLS, and rate-limited public endpoints.</li>
  <li>Internal access is least-privilege, MFA-enforced, and logged.</li>
  <li>Backups are encrypted at rest and tested regularly for
  restorability.</li>
</ul>

<h2 id="report">Report a vulnerability</h2>
<p>Security researchers, please email
<a href="mailto:security@sgtcart.com">security@sgtcart.com</a> with a
proof-of-concept and your contact details. We commit to:</p>
<ul>
  <li>Acknowledging within 2 business days.</li>
  <li>A safe-harbour for good-faith research that doesn't impact other
  users.</li>
  <li>Public credit (if you'd like) after the fix ships.</li>
</ul>
""",
        "related": [
            {"href": "/privacy/", "title": "Privacy",
             "desc": "How your data is handled."},
            {"href": "/trust-safety/", "title": "Trust & safety",
             "desc": "Marketplace integrity."},
            {"href": "/transparency/", "title": "Transparency",
             "desc": "Reporting commitments."},
        ],
    },
]
