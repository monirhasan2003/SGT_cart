# SGT Cart — Footer · Legal · Policy & Help Master Plan

> **Status:** Draft v1 · awaiting user approval before build starts
> **Scope:** every page reachable from the site footer + every legal /
> policy / help / seller / company surface a professional international
> multi-vendor marketplace ships with.
> **Operator:** Smart Global Trade Cart (SGT Cart) · sgtcart.com
> **Markets:** Bangladesh-first, internationally accessible (single-domain
> storefront; localised compliance pages where relevant)

---

## 1. Why this document

Current footer ships only About / Contact / Terms / Privacy / Sell / FAQ /
Shipping / Returns — eight short pages. A real international marketplace
(Amazon, eBay, Daraz, Shopee, AliExpress, Etsy) maintains **50-70 dedicated
pages** across five categories:

1. **Company** — Who we are, where we work, how to reach us, how to join us.
2. **Customer Help / Buy** — Onboarding, ordering, payment, delivery,
   returns, protection, loyalty, troubleshooting.
3. **Seller / Vendor Resources** — Onboard, list, sell, fulfil, get paid,
   stay compliant, grow.
4. **Legal & Policy** — Contractual terms, statutory disclosures, IP,
   privacy, AML/KYC, accessibility, jurisdiction.
5. **Trust, Safety & Compliance** — Reporting channels, transparency,
   counterfeit/IP, modern slavery, anti-bribery.

Without these, SGT Cart can't:
- defend against marketplace liability (counterfeit / illegal goods),
- satisfy Bangladesh's **Digital Commerce Operation Guidelines 2021** +
  **Consumer Rights Protection Act 2009**,
- onboard payment processors at scale (SSLCommerz / Stripe / Adyen all
  require posted policies),
- pass legal review when opening to international shipping.

This plan sequences the work, defines per-page content requirements,
and locks a shared page shell so every page looks/feels the same.

---

## 2. Compliance frameworks the pages must address

| Framework | Applies to | Pages it drives |
|---|---|---|
| **Bangladesh Consumer Rights Protection Act 2009 (CRPA)** | All customer surfaces | Refund, Cancellation, Returns, Pricing, Quality Guarantee, Complaint redressal |
| **Bangladesh Digital Commerce Operation Guidelines 2021** (DCOG) | Marketplace operations | Order timelines, escrow disclosures, seller KYC, dispute resolution, delivery SLA |
| **Bangladesh Bank Foreign Exchange Regulation** | Payouts, cross-border | Payout policy, FX disclosure |
| **NBR VAT & Income Tax Rules** | All sellers | Tax info, VAT collection disclosure, seller TIN requirement |
| **GDPR-style data protection** (forward-looking, voluntary for now) | International users | Privacy Policy, Cookie Policy, Data Subject Rights, DPA for sellers |
| **PCI-DSS** (via SSLCommerz tokenisation) | Payments | Payment Methods, Security policy |
| **WCAG 2.1 AA** | All pages | Accessibility Statement, alt text, contrast, ARIA |
| **OECD Model AML / FATF 40 Recs** | High-value sellers, payouts | KYC, AML, Suspicious activity reporting |
| **Modern Slavery statements** (UK MSA / Aus MSA equivalent) | Supplier base | Supplier Code, Modern Slavery statement |
| **DMCA-equivalent IP takedown** | UGC + listings | IP Infringement / Counterfeit Reporting |

Each page below tags the framework it addresses so legal review is
traceable.

---

## 3. Page taxonomy — 64 pages across 5 hubs

### HUB A · COMPANY (5 pages)

| # | Slug | Title | Compliance | Sec count |
|---|---|---|---|---|
| A1 | `/about/` | About SGT Cart | — | 6 |
| A2 | `/contact/` | Contact Us | CRPA §76 (redressal contact) | 5 |
| A3 | `/careers/` | Careers at SGT Cart | — | 4 |
| A4 | `/newsroom/` | Newsroom & Press | — | 3 |
| A5 | `/sustainability/` | Sustainability & CSR | — | 5 |

### HUB B · CUSTOMER HELP (16 pages)

| # | Slug | Title | Compliance | Sec count |
|---|---|---|---|---|
| B1 | `/help/` | Help Center (hub) | — | 1 + cards |
| B2 | `/help/how-to-order/` | How to Order | DCOG §4 | 6 |
| B3 | `/help/payment-methods/` | Payment Methods | PCI-DSS, DCOG §6 | 6 |
| B4 | `/shipping/` | Shipping & Delivery | DCOG §5 (delivery SLA) | 7 |
| B5 | `/help/order-tracking/` | Tracking Your Order | DCOG §5 | 4 |
| B6 | `/returns/` | Returns & Refunds | CRPA §38-46 | 8 |
| B7 | `/help/cancellations/` | Order Cancellation | CRPA §38 | 5 |
| B8 | `/help/damaged-item/` | Damaged / Wrong Item | CRPA §40, §44 | 5 |
| B9 | `/help/buyer-protection/` | Buyer Protection Program | DCOG §7 | 7 |
| B10 | `/help/rewards/` | Reward Points Program | — | 5 |
| B11 | `/help/coupons/` | Coupons & Vouchers | — | 5 |
| B12 | `/help/account/` | Managing Your Account | GDPR-style | 6 |
| B13 | `/help/reviews/` | Reviews & Ratings Guidelines | — | 5 |
| B14 | `/help/report-problem/` | Report a Problem | CRPA §76 | 5 |
| B15 | `/help/counterfeit/` | Report Counterfeit / Fake Item | DMCA-equiv | 5 |
| B16 | `/faq/` | Frequently Asked Questions | — | grouped |

### HUB C · SELLER RESOURCES (14 pages)

| # | Slug | Title | Compliance | Sec count |
|---|---|---|---|---|
| C1 | `/sell/` | Sell on SGT Cart (landing) | — | (rebuild) |
| C2 | `/sell/onboarding/` | Seller Onboarding Guide | DCOG §3 (KYC) | 7 |
| C3 | `/sell/fees/` | Seller Fees & Commission | NBR VAT | 6 |
| C4 | `/sell/payouts/` | Payout Schedule & Methods | BB FX, AML | 6 |
| C5 | `/sell/listing-guidelines/` | Product Listing Guidelines | CRPA labelling | 8 |
| C6 | `/sell/prohibited-items/` | Prohibited & Restricted Items | BD Customs Act | 8 |
| C7 | `/sell/performance-standards/` | Seller Performance Standards | — | 6 |
| C8 | `/sell/seller-protection/` | Seller Protection Program | — | 6 |
| C9 | `/sell/code-of-conduct/` | Seller Code of Conduct | — | 7 |
| C10 | `/sell/dispute-resolution/` | Seller Dispute Resolution | DCOG §8 | 6 |
| C11 | `/sell/tax-info/` | Tax Information for Sellers | NBR | 6 |
| C12 | `/sell/promotion-guide/` | Promotions & Advertising Guide | CRPA §43 | 6 |
| C13 | `/sell/anti-disintermediation/` | Anti-Disintermediation Policy | — | 5 |
| C14 | `/sell/api-docs/` | Seller API (Phase 13 prep) | — | 4 |

### HUB D · LEGAL & POLICY (15 pages)

| # | Slug | Title | Compliance | Sec count |
|---|---|---|---|---|
| D1 | `/terms/` | Customer Terms of Service | CRPA, ICT Act 2006 | 18 |
| D2 | `/seller-terms/` | Seller Agreement | DCOG, NBR | 22 |
| D3 | `/privacy/` | Privacy Policy | GDPR-style, ICT Act | 14 |
| D4 | `/cookie-policy/` | Cookie Policy | GDPR e-Privacy | 6 |
| D5 | `/acceptable-use/` | Acceptable Use Policy | — | 8 |
| D6 | `/ip-policy/` | Intellectual Property Policy | TRIPS, DMCA-equiv | 9 |
| D7 | `/anti-counterfeit/` | Anti-Counterfeit Policy | TRIPS | 7 |
| D8 | `/aml-policy/` | Anti-Money-Laundering Policy | FATF, BFIU | 9 |
| D9 | `/kyc-policy/` | Know-Your-Customer Policy | BFIU, DCOG | 7 |
| D10 | `/data-rights/` | Your Data Rights (Subject Access) | GDPR-style | 7 |
| D11 | `/childrens-privacy/` | Children's Privacy Policy | COPPA-equiv | 5 |
| D12 | `/accessibility/` | Accessibility Statement | WCAG 2.1 AA | 6 |
| D13 | `/affiliate-terms/` | Affiliate Program Terms | NBR | 7 |
| D14 | `/promotions-rules/` | Promotions, Contests & Sweepstakes | CRPA §43 | 7 |
| D15 | `/dispute-resolution/` | Dispute Resolution & Arbitration | CRPA §76, ADR Act 2001 | 7 |

### HUB E · TRUST, SAFETY & COMPLIANCE (14 pages)

| # | Slug | Title | Compliance | Sec count |
|---|---|---|---|---|
| E1 | `/trust-safety/` | Trust & Safety Hub | — | 1 + cards |
| E2 | `/transparency/` | Transparency Report | DCOG §10 (annual) | 6 |
| E3 | `/report-illegal/` | Report Illegal Content | ICT Act 2006 §57 | 5 |
| E4 | `/whistleblower/` | Whistleblower Policy | OECD | 5 |
| E5 | `/modern-slavery/` | Modern Slavery Statement | MSA-equiv | 6 |
| E6 | `/anti-bribery/` | Anti-Bribery & Corruption Policy | OECD, BD ACC Act | 7 |
| E7 | `/supplier-code/` | Supplier Code of Conduct | — | 8 |
| E8 | `/environmental/` | Environmental Policy | — | 5 |
| E9 | `/refund-policy/` | Detailed Refund Policy | CRPA §38-46 | 9 |
| E10 | `/cancellation-policy/` | Detailed Cancellation Policy | CRPA §38 | 6 |
| E11 | `/quality-guarantee/` | Quality Guarantee | CRPA §41 | 6 |
| E12 | `/pricing-policy/` | Pricing Policy | CRPA §43 | 6 |
| E13 | `/security/` | Security Practices | PCI-DSS, ISO 27001-aligned | 8 |
| E14 | `/governing-law/` | Governing Law & Jurisdiction | — | 4 |

**Total: 64 pages.**

---

## 4. Page shell — the shared template

Every page extends a common `pages/static/_layout.html` (already exists) and
follows this skeleton so navigation, search, version history, and contact
CTA stay consistent.

```
[Header / breadcrumb]
[Title + last-reviewed date + version tag]
[Bilingual toggle (EN / BN) — top right]
[Table of Contents — sticky on desktop, accordion on mobile]
[Sections — each ≥150 words, with subheadings]
[Examples / tables / diagrams where useful]
[Frequently Asked Questions block]
[Related pages cross-link]
[Contact-us footer card — "Still have questions?"]
[Versioning footer — "Last reviewed YYYY-MM-DD · Version X.Y"]
```

**Per-page minimum content quality bar:**
- Real content, **1,200–3,000 words** per page (not a one-paragraph stub)
- 4–9 logical sections — see "Sec count" in the taxonomy
- At least one table, list, or diagram per page where relevant
- 3–6 FAQs at the bottom
- Examples where the rule needs illustrating ("e.g., a refund within 7
  days of delivery looks like this…")
- Cross-links to related pages
- Concrete contact channels (`support@sgtcart.com` for general,
  `policy@sgtcart.com` for legal escalations, `seller-support@sgtcart.com`
  for vendor issues)
- **Last-reviewed date** — keeps legal review auditable

---

## 5. Bilingual policy

| Page tier | English | Bangla | Strategy |
|---|---|---|---|
| **Critical legal** (D1, D2, D3, D6, D8, D15) | Required | Required at launch | Side-by-side language toggle |
| **Customer help** (B1-B16) | Required | Required at launch | Toggle |
| **Seller resources** (C1-C14) | Required | Phase 2 | Toggle, EN first |
| **Trust & safety, company** | Required | Phase 2 | EN first, BN as we expand |

Bilingual content lives in twin templates — `terms_en.html` +
`terms_bn.html` — with a JS toggle that flips visible blocks and stores
the preference in `localStorage["sgt_doc_lang"]`. URL stays the same so
SEO indexes the English version.

---

## 6. Cross-cutting requirements

1. **Mobile-first layout** — every page readable in single-column under
   360px. ToC collapses to accordion. No `display-5` or `p-5`
   (lesson from D-1..D-10 polish round).
2. **Search across all 64 pages** — small client-side fuzzy search over
   page titles + section headings on `/help/` and `/sell/` hubs.
3. **SEO** — every page gets a custom `<title>` + meta description +
   Open Graph image. `robots.txt` permits indexing; `sitemap.xml`
   regenerated after build.
4. **Last-reviewed metadata** — stored as a Jinja variable per template
   so we can render "Last reviewed: 15 Jun 2026" in the footer card.
5. **Versioning** — major changes bump version (1.0 → 1.1). Store a
   changelog block at the bottom of every legal page.
6. **Print-friendly** — `@media print` CSS so legal pages can be saved
   to PDF cleanly (regulators, dispute evidence).
7. **Accessibility** — semantic `<section>` / `<h2>` hierarchy, ARIA
   landmarks, alt text on all images, keyboard-navigable accordion.
8. **Schema.org JSON-LD** — FAQ pages emit `FAQPage` schema; legal
   pages emit `Article` schema for Google's structured-data crawler.
9. **Sub-footer reorganisation** — current footer has 4 columns
   (Help / Shop / Company / Payments); we'll expand to 5
   (+ "Sell" hub) and pivot category links to top categories from DB.
10. **Cookie banner** — required for D4 (cookie policy). Sticky bottom
    bar with "Accept all / Necessary only / Manage".

---

## 7. Ship sequence — phased delivery

The 64 pages won't ship in one go. Three release waves:

### Wave 1 · MVP-legal (must ship before public launch) — 16 pages

Pages an international marketplace **must** publish before taking
real customer money:

- D1 `/terms/` · D2 `/seller-terms/` · D3 `/privacy/` ·
  D4 `/cookie-policy/` · D6 `/ip-policy/` · D15 `/dispute-resolution/`
- B6 `/returns/` · B7 `/help/cancellations/` ·
  B9 `/help/buyer-protection/` · E9 `/refund-policy/`
- B3 `/help/payment-methods/` · B4 `/shipping/`
- C2 `/sell/onboarding/` · C3 `/sell/fees/` · C5 `/sell/listing-guidelines/`
- A2 `/contact/` (full rewrite)

### Wave 2 · Customer + Seller depth — 26 pages

- All remaining HUB B (10 pages)
- All remaining HUB C (10 pages)
- A1 / A4 / A5 (rebuilds + new)
- D5 / D7 / D10 / D11 / D12 / D13

### Wave 3 · Trust + Compliance + Bangla — 22 pages

- All HUB E
- D8 / D9 / D14
- A3 careers
- Bangla translation of Wave 1 + Wave 2 critical pages

---

## 8. Per-page detailed content outlines

Below is the chapter-by-chapter outline of what each page contains so
nothing is forgotten when implementation begins. Pages marked with **★**
ship in Wave 1.

### D1 · Customer Terms of Service ★  (18 sections, ~3,000 words)

1. Definitions (User, Customer, Seller, Marketplace, Order, etc.)
2. Acceptance and capacity to contract (Bangladesh majority-age rules)
3. Account registration & responsibility
4. Marketplace role — SGT Cart facilitates; the **seller** is the
   contractual counter-party
5. Listings & accuracy disclaimers
6. Pricing & currency disclosure
7. Order formation (offer / acceptance moment)
8. Payment authorisation (incl. SSLCommerz tokenisation)
9. Delivery timelines + delays + force majeure
10. Reward points & promotion participation
11. User-generated content licence (reviews, photos, Q&A)
12. Prohibited customer behaviour
13. Account suspension & termination
14. Indemnity, warranties, limitation of liability (capped at order value)
15. Modifications to the terms
16. Governing law (Bangladesh), jurisdiction (Dhaka courts)
17. Dispute resolution before litigation (CRPA §76 redressal path)
18. Contact + Annex (linked policies)

### D2 · Seller Agreement ★  (22 sections, ~3,500 words)

1. Definitions (Seller, Listing, Sub-Order, Commission, Payout)
2. Eligibility — Bangladesh-resident or registered entity, valid TIN
3. KYC documents required (Trade License + NID + bank/bKash/Nagad)
4. Listing requirements & accuracy obligation
5. Pricing autonomy + price-gouging prevention
6. Inventory & stock-management obligation
7. Order acceptance & fulfilment SLA
8. Packaging standards & branding restrictions
9. Shipping responsibilities (vs. SGT-managed carriers)
10. Commission schedule (link to C3 fees page)
11. Payout cycle (link to C4 payouts page)
12. Tax withholding by SGT Cart (NBR rules)
13. Returns, refunds & chargeback responsibility
14. Customer complaints handling timeline
15. Anti-disintermediation (no contact off-platform — link to C13)
16. Counterfeit, IP, prohibited items
17. Performance standards — auto-suspension thresholds
18. Account suspension / termination triggers
19. Confidentiality & data use
20. Indemnity (seller indemnifies SGT for listing infringement)
21. Modifications & notice period (30-day notice for material changes)
22. Governing law, jurisdiction, arbitration

### D3 · Privacy Policy ★  (14 sections, ~2,500 words)

1. Who we are + DPO contact (`privacy@sgtcart.com`)
2. Personal data we collect (full enumeration: name, email, phone, address, NID for sellers, payment tokens, behavioural data)
3. How we collect it (provided by user, automated, third-party APIs)
4. Lawful basis for each processing purpose
5. How we use the data (operate platform, fraud prevention, marketing,
   analytics, AI summaries)
6. Sharing with sellers, payment processors, delivery partners,
   law enforcement
7. International transfers (when international shipping launches)
8. Data retention schedule (orders 7y for tax, marketing 2y, KYC 5y
   per BFIU)
9. Security measures (PCI-DSS via SSLCommerz, encryption-at-rest,
   access controls)
10. Your rights — access / correction / deletion / portability /
    object to marketing
11. Children's privacy summary (link to D11)
12. Cookies summary (link to D4)
13. Updates to the policy + notification mechanism
14. Contact for privacy queries + supervisory authority

### B6 · Returns & Refunds ★  (8 sections, ~2,000 words)

1. Eligibility window (7 days from delivery — CRPA §38 default)
2. Items eligible vs. non-eligible (perishables, intimate use, custom-made)
3. Condition requirements (original packaging, tags, no use)
4. How to start a return (step-by-step + screenshots)
5. Refund methods + timelines (COD: bKash/Nagad back; SSLCommerz: original card 7-10 days)
6. Damaged / wrong item flow (no return-shipping fee — covered by seller)
7. Seller refusal & dispute escalation
8. Frequently Asked Questions

### B9 · Buyer Protection Program ★  (7 sections, ~1,800 words)

1. What's covered: non-delivery, item-not-as-described, counterfeit, damaged
2. Claim window (60 days from order)
3. How to file a claim
4. Evidence we ask for (photos, video, unboxing if available)
5. Resolution timeline (we mediate within 7 business days)
6. Outcomes — refund / replacement / partial credit
7. What's NOT covered (buyer's remorse on used items, late claims)

### C2 · Seller Onboarding Guide ★  (7 sections, ~2,200 words)

1. Who can sell (individual vs. company, BD resident requirement)
2. Documents you'll need (Trade License, NID, bank statement)
3. Step 1 — create account
4. Step 2 — submit KYC verification
5. Step 3 — set up your store profile (logo, banner, description)
6. Step 4 — add your first 5 products
7. Step 5 — payout setup + tax info

### C3 · Seller Fees & Commission ★  (6 sections, ~1,500 words)

1. Platform commission table by category (default 10%, electronics 8%, fashion 12%)
2. Payment-processing fee passthrough
3. Optional promotion/sponsorship rates
4. Refunded-order commission reversal
5. VAT collection & deposit (NBR Mushok-6.3 mention)
6. Worked example — Tk 1,000 sale breakdown

### C5 · Product Listing Guidelines ★  (8 sections, ~2,200 words)

1. Title rules (length, keyword stuffing, brand misuse)
2. Description quality (no copied text, real specs)
3. Image standards (min resolution, no watermarks, no contact info)
4. Bilingual title encouragement
5. Pricing rules (no inflated MRP, no bait-and-switch)
6. Variant + bulk-tier rules
7. Category selection
8. Common rejection reasons + how to fix

### E9 · Detailed Refund Policy ★  (9 sections, ~2,200 words)

Expands B6 with seller-side, payment-method-specific timelines, COD
vs. prepaid flows, dispute escalation matrix, partial-refund formula
for damaged items, and CRPA §38-46 mapping.

### D6 · IP Policy ★  (9 sections, ~2,200 words)

1. Our role (we are a host, not a publisher of seller listings)
2. What infringes (trademark, copyright, design, patent, passing-off)
3. Notice-and-takedown procedure (DMCA-equivalent)
4. Required information in a takedown notice
5. Counter-notice procedure
6. Repeat-infringer policy (3-strike termination)
7. Brand Registry programme (future)
8. Counterfeit reporting (link to E?)
9. Contact for IP claims (`ip-takedown@sgtcart.com`)

### D4 · Cookie Policy ★  (6 sections, ~1,200 words)

Strictly necessary cookies (CSRF, session) · Preferences (locale,
currency) · Analytics (first-party only) · Marketing (none currently) ·
how to manage in-browser · cookie banner control.

### D15 · Dispute Resolution & Arbitration ★  (7 sections, ~1,800 words)

1. Step 1 — direct contact between buyer and seller through SGT chat
2. Step 2 — file a Buyer/Seller Protection claim
3. Step 3 — SGT mediation (7 business days)
4. Step 4 — escalation to **CRPA §76 redressal** (National Consumer
   Right Protection Department)
5. Step 5 — arbitration under **Arbitration Act 2001 (BD)**, sole
   arbitrator, Dhaka seat, English/Bangla
6. Class action waiver (where enforceable)
7. International users — choice-of-law clause

### B3 · Payment Methods ★  (6 sections, ~1,500 words)

Cash on Delivery (eligibility, max order value, COD fee) ·
bKash / Nagad mobile wallets · Credit/debit card via SSLCommerz ·
Reward Points redemption rules · Failed-payment retries ·
Security disclosure (we never see your card number).

### B4 · Shipping & Delivery ★  (7 sections, ~1,800 words)

District-wise ETA table (D-9 already wired) · Shipping fee structure
(per vendor) · Free-shipping threshold rules · Delivery partners ·
Tracking · Failed delivery / re-attempt policy · International
shipping (when launched).

### A2 · Contact Us ★  (5 sections, ~1,200 words)

General support · Seller support · Press · Legal · Compliance ·
Each with a dedicated email + response-time SLA · Address (Mirpur,
Dhaka) · Office hours · Emergency contact for ongoing-fraud reports.

### (… full outlines for the remaining 48 pages live in section 11 of this doc — to be authored in the corresponding ship-wave.)

---

## 9. Footer reorganisation

Current footer columns: Help · Shop · Company · Payments.

**New 6-column footer** (collapses to 2 on mobile):

| Col 1 — Brand | Col 2 — Buy | Col 3 — Sell | Col 4 — Company | Col 5 — Legal | Col 6 — Pay & Trust |
|---|---|---|---|---|---|
| Logo · address · email · socials | Help Center · How to Order · Payment Methods · Shipping · Returns · Track Order · Buyer Protection · Rewards | Sell on SGT Cart · Onboarding · Fees · Payouts · Listing Guidelines · Seller Protection · API | About · Careers · Newsroom · Sustainability · Contact | Terms · Seller Terms · Privacy · Cookies · IP Policy · Dispute Resolution · Accessibility | COD · bKash · Nagad · Card · Trust & Safety · Transparency · Report illegal |

Below the columns: copyright line + legal-entity disclosure +
sub-row of small badges (SSL secure · PCI compliant · Verified by SGT
KYC · BD VAT registered).

---

## 10. Data + admin requirements

Some pages need **structured data** (not just static HTML):

1. **Per-page "last reviewed" date** — store in a YAML front-matter or a
   small `legal_pages` DB table with `slug` + `version` + `reviewed_at`
   + `reviewer_name`. Admin can bump from `/admin/legal-pages/`.
2. **Transparency Report (E2)** — pulls live numbers: total products,
   active sellers, takedowns last quarter, policy violations
   (we already have `PolicyViolation` table from D-0).
3. **Sitemap.xml** — auto-regenerated to include every new page.
4. **Sub-footer payment badges** — image assets in
   `static/assets/img/badges/` (visa, mastercard, bkash, nagad,
   ssl-secure, pci-compliant).

---

## 11. Engineering / template plan

```
app/templates/
├── pages/
│   ├── static/
│   │   ├── _layout.html          ← shared shell (extend)
│   │   ├── _toc.html             ← table-of-contents partial
│   │   ├── _faq.html             ← FAQ accordion partial
│   │   ├── _contact_card.html    ← "Still have questions?" CTA
│   │   ├── _version_footer.html  ← last-reviewed metadata
│   │   ├── about.html            ← Wave 1 (rebuild)
│   │   ├── contact.html          ← Wave 1 (rebuild)
│   │   ├── terms.html            ← Wave 1 (rebuild, 18 sections)
│   │   ├── seller_terms.html     ← Wave 1 (new)
│   │   ├── privacy.html          ← Wave 1 (rebuild)
│   │   ├── cookies.html          ← Wave 1 (new)
│   │   ├── ip_policy.html        ← Wave 1 (new)
│   │   ├── dispute_resolution.html ← Wave 1 (new)
│   │   ├── refund_policy.html    ← Wave 1 (new — distinct from /returns/)
│   │   ├── shipping.html         ← Wave 1 (rebuild)
│   │   ├── returns.html          ← Wave 1 (rebuild)
│   │   ├── payment_methods.html  ← Wave 1 (new)
│   │   ├── buyer_protection.html ← Wave 1 (new)
│   │   ├── cancellations.html    ← Wave 1 (new)
│   │   ├── seller_onboarding.html ← Wave 1 (new)
│   │   ├── seller_fees.html      ← Wave 1 (new)
│   │   ├── seller_listing_guidelines.html ← Wave 1 (new)
│   │   └── …Wave 2 + Wave 3 files…
│   └── help/                     ← /help/* hub
│       ├── index.html            ← help hub
│       └── …
```

Routes live in a new blueprint `app/blueprints/legal.py` (or extend
`pages.py`) — one `@legal.route("/terms/")` style per page, all
rendering the appropriate template.

Bilingual templates are split as `terms.html` + `terms_bn.html` and
selected by a query string (`?lang=bn`) + sticky locale toggle.

---

## 12. Estimated effort (rough)

| Wave | Pages | Avg page wordcount | Estimated hours |
|---|---|---|---|
| Wave 1 — MVP legal | 16 | 2,000 | ~40 h |
| Wave 2 — depth | 26 | 1,500 | ~50 h |
| Wave 3 — compliance + Bangla | 22 + BN translation of Wave 1+2 | varies | ~50 h |
| **Total** | **64 pages + BN of Wave 1+2** | — | **~140 h** |

If the goal is to launch sgtcart.com **publicly**, Wave 1 is the gate.
~5-6 sessions, each shipping 3-4 pages with full content + smoke test
that the route renders 200 + the ToC + FAQ block exist.

---

## 13. Acceptance criteria per page

Before a page ships:
1. Word count meets the section's target (≥1,200 words for legal,
   ≥1,500 for seller-resource, ≥1,000 for customer-help).
2. All sections from §8's outline are present.
3. Mobile-readable at 360px — no horizontal scroll, ToC collapses.
4. ToC anchors all work.
5. FAQ block has ≥3 questions.
6. Cross-links to ≥2 related pages.
7. Contact card with the relevant `*@sgtcart.com` email.
8. Last-reviewed date in the version footer.
9. Smoke test: `GET <slug>` returns 200, body contains the page title,
   ToC, and "Last reviewed".
10. Lighthouse SEO score ≥ 90 on the page.

---

## 14. Decisions — LOCKED (user-approved 2026-05-24)

1. **Jurisdiction:** Bangladesh / Dhaka courts MUST be the primary forum
   (mandatory clause). International users get an additional carve-out
   recognising their local consumer-rights statutes where Bangladesh
   law allows. Dispute pages mention both.
2. **Currency:** **BDT only** at launch. Pricing Policy + Payment
   Methods + Seller Fees show Tk throughout. No USD/EUR toggle until
   international shipping ships in a later phase.
3. **Children's policy floor age:** **13** (COPPA standard).
4. **Cookie consent:** **simple two-button** banner — "Accept all" /
   "Necessary only". No per-category granular consent for now. Cookie
   Policy (D4) describes the cookies but doesn't add UI controls.
5. **Legal review timing:** ship templates without lawyer review. We
   own the risk. Pages note they were "Drafted by SGT Cart team —
   not legal advice" in the version footer to flag this clearly.
6. **Seller subdomain:** keep everything under `/sell/*` for now;
   architect routes so a future move to `seller.sgtcart.com` is a
   blueprint-prefix swap, not a content rewrite.

---

## 15. Next action

If this plan is acceptable, **Wave 1 starts** with these four files in
order:

1. `_layout.html` upgrade (shared shell with ToC, FAQ, contact card,
   version footer partials)
2. `terms.html` rebuild (18 sections, full text)
3. `privacy.html` rebuild (14 sections, full text)
4. `seller_terms.html` (new, 22 sections, full text)

Each comes with a smoke test asserting it renders + has the required
sections. After all 16 Wave-1 pages ship, the footer rewires (§9) and
we mark `sgtcart.com` as **public-launch ready** from a legal /
compliance posture.

---

*End of master plan v1 — awaiting approval / redirection before any
template work begins.*
