# Phase 15 Chunk D — Product Detail Page Upgrade

User-approved feature plan for overhauling `/product/<slug>/`. Decision date:
**2026-05-24**. Total scope: **Daraz parity (17) + 26 bespoke features = 43 items**,
plus a cross-cutting anti-disintermediation hardening pass (D-0), split into
**11 sub-chunks**. Each sub-chunk ships with its own smoke test, following
the same model as Chunk B v3a / v3b / v3c.

> **D-0 must ship first** — it expands the existing phone-share guard from
> chat into reviews and Q&A, and adds a 2-strike auto-suspend for offending
> sellers. See [marketplace-feature-rules](../../../.claude/projects/d--Ecommerce/memory/marketplace-feature-rules.md)
> memory for the full policy.

---

## Section 1 — Daraz Parity (17 must-haves)

### Layout & Conversion
1. **Right-side Delivery sidebar** — location picker, ETA date range, shipping
   fee, COD availability, return policy, warranty info
2. **Share + Wishlist icons** at the top of the product header
3. **Buy Now button** — skip cart, direct checkout
4. **Color / Variant image swatches** — clickable image-based, not just text
   badges
5. **Quantity selector** — `−  1  +` style buttons (not just a numeric input)
6. **"Cash on Delivery" / "Free Shipping" stickers** — inline trust badges
7. **Image zoom on hover** — magnifier lens (also Section 6 R6)

### Content
8. **Structured spec list** — bulleted key–value pairs with a "View More"
   expand toggle, distinct from the seller's free-form description

### Discovery
9. **Brand entity surface** — "Brand: X" + "More from Brand" link (our
   `Brand` model already exists, just unsurfaced)
10. **Promotional context strip** — when a flash sale is live, show its banner
    inline on relevant product pages
11. **Limited stock / Limited time overlay** on the gallery image

### Reviews
12. **Rating distribution bars** — 5★ X, 4★ X, 3★ X, 2★ X, 1★ X visual
    breakdown
13. **Review sort + filter + pagination** — sort by Relevance / Newest /
    Highest / Lowest, filter by star count

### Mobile / App
14. **App download QR code** — only when Flutter apps are live

### Q&A
15. **Public Q&A system** — buyers ask publicly, seller (or community) answers;
    "X Answered Questions" counter near the rating

### Sold By panel (right sidebar lower section)
16. **Mall / Flagship Store badge** — premium vendor tier indicator
17. **Live chat with seller** — "Chat Now" button (we already have `Ask
    Seller` — needs presence + quick-questions added in Section 5)

---

## Section 2 — Trust & Transparency (3 features)

| ID | Feature | Notes |
|----|---------|-------|
| T1 | **"Verified by SGT" badge** — KYC verified seller (Trade License + NID checked) | All KYC fields already on `VendorProfile`, just surface them |
| T2 | **Seller stats inline** — avg delivery days + cancel rate | Phase 15 v3b already computes these on `VendorProfile` |
| T5 | **Bilingual verification badges** — "ব্যবসায়িক লাইসেন্স যাচাইকৃত" / "Trade License Verified" | Pure rendering — no new data |

## Section 3 — Smart Decision Helpers (5 features)

| ID | Feature | Notes |
|----|---------|-------|
| D1 | **Frequently Bought Together** — bundle suggestion shown on product + at checkout | Compute from past order pairs |
| D3 | **AI Pros & Cons summary** — auto-extracted from review text | LLM call cached per product |
| D4 | **"Why buy from this seller?" card** — auto-computed: 95% positive, 1-day delivery avg, 2-hour chat reply | Aggregates existing seller stats |
| D5 | **Stock urgency** — "Only 3 left" + "5 sold in last 24h" + "23 viewing now" | "viewing now" needs Redis or socket counter |
| D6 | **"Notify when back in stock"** — email notify on out-of-stock products | New `StockNotification` table |

## Section 4 — Money & Loyalty (6 features)

| ID | Feature | Notes |
|----|---------|-------|
| M1 | **Reward points earned shown inline** — "Earn 16 points" | `RewardLedger` + `reward_service` already exist |
| M2 | **Apply coupon on product page** — input inline, don't wait for checkout | Reuse `coupon_service` |
| M3 | **"Pay with reward points" inline** | `reward_service.balance(user)` already computes |
| M4 | **Bulk pricing tiers** — "2-pack 5% off, 5-pack 10% off" | New `ProductPriceTier` table |
| M5 | **Free shipping threshold helper** — "Add ৳200 more to unlock free shipping" | Uses existing `shipping_fee_per_vendor` setting |
| M6 | **Affiliate link generator** — logged-in user sees their own affiliate URL | `AffiliateCommission` model already exists |

## Section 5 — Enhanced Communication (5 features)

| ID | Feature | Notes |
|----|---------|-------|
| C1 | **Live chat with seller** — already covered as Daraz parity #17 | — |
| C3 | **Chat presence indicator** — "Online now" / "Last seen 5 min ago" / "Typically replies in 30 min" | Combines socket presence + ChatMessage timestamps |
| C4 | **Pre-set quick questions** — one-tap buttons for common questions ("ডেলিভারি কত দিনে?", "Original কি?", "Warranty আছে?") | Static list + send-as-message |
| C5 | **Voice message in chat** — record + upload audio | `ChatMessage` needs `audio_path` column |
| C6 | **Public Q&A + answer-helpful voting** — already covered as Daraz parity #15, this adds helpful upvotes | Builds on the Q&A model |

## Section 6 — Rich Media (1 feature)

| ID | Feature | Notes |
|----|---------|-------|
| R6 | **Image zoom + magnifier on hover** — also listed as Daraz parity #7 | JS overlay library |

## Section 7 — BD / Local-specific (5 features)

| ID | Feature | Notes |
|----|---------|-------|
| B1 | **District-wise delivery ETA** — "Dhaka: 1 day, Chittagong: 3 days, Sylhet: 4 days" | New `DistrictEta` table |
| B2 | **Same-city seller badge** — "একই শহরের সেলার — দ্রুত পাবেন" | Compare buyer's saved address city with seller's city |
| B4 | **Prayer time delivery preference** — don't deliver during Jumma / Maghrib | Buyer preference flag + Bangladesh Hijri prayer time API or static table |
| B5 | **Eid / Festival pricing countdown** — auto-show "Eid Special" badge with timer | Tied to `FlashSale` or new `Campaign` |
| B6 | **Hijri date alongside Gregorian** — "৪ Ramadan / 14 March" | Pure rendering helper |

---

## Implementation chunking (11 sub-chunks)

Order is suggested by dependency + value-per-effort. Each sub-chunk = one
deliverable + smoke test + regression run.

### D-0 — Anti-disintermediation enforcement (cross-cutting, must ship first)

Phone-share policy already exists for chat (`phone_guard.py` redacts in
`chat_service`). Before D-2 (Q&A), D-3 (reviews UX), and D-7 (chat enhancements)
expand the surface area for user-authored text, harden it everywhere:

- Wire `redact_phone_numbers` into `review_service.create_review` and the
  upcoming Q&A `Answer` model (and any other seller-authored free-text fields
  we add).
- New `PolicyViolation` table — one row per redaction triggered by a SELLER
  account (timestamp, user_id, surface=chat|review|qa, original_excerpt,
  thread_id/review_id/etc).
- After **2 violations** by the same seller: auto-set
  `VendorProfile.status = VENDOR_SUSPENDED`, notify the admin
  (`NOTIF_SYSTEM`), and notify the seller with the reason.
- Admin UI: a "Policy Violations" list under `/admin/`, plus the violation
  count + last-violation date surfaced on `vendor_detail.html`. Admin can
  un-suspend manually.
- Customer-side violations: redact only, **no auto-block**.
- Public surfaces — block phone fields from rendering on the seller store
  page, the product page Sold-By panel, and any other vendor-facing public
  view (most are already not rendered; verify and lock down).
- Smoke test: 2-strike suspend, customer redacts-only, admin unsuspend round-trip.

### D-1 — Layout & Daraz parity foundation
- Right delivery sidebar (location, ETA, shipping fee, COD, return, warranty)
- Sold By panel with Chat Now + Visit Store + Mall badge + seller stats
- Buy Now button
- Quantity − / + selector
- Color / Variant image swatches
- Share + Wishlist icons
- COD / Free shipping inline stickers
- Image zoom magnifier
- Brand "More from Brand" link

### D-2 — Specs & Q&A
- Structured spec list (key-value pairs) + "View More"
- Public Q&A system — new `Question` / `Answer` tables, helpful-vote later

### D-3 — Reviews upgrade
- Star distribution bars
- Sort + filter + pagination
- Customer photo gallery (aggregate `ReviewImage` rows)

### D-4 — Trust & seller credibility
- T1 "Verified by SGT" badge
- T5 bilingual verification badges
- T2 seller stats inline
- D4 "Why buy from this seller?" card

### D-5 — Money & loyalty inline
- M1 "Earn X points" preview
- M2 apply coupon inline
- M3 pay-with-points option
- M5 free shipping threshold helper
- M4 bulk pricing tiers (new `ProductPriceTier` table)
- M6 affiliate link generator

### D-6 — Urgency & inventory signals
- D5 "Only X left" + "Y sold in last 24h" + "Z viewing now"
- D6 "Notify when back in stock" — new `StockNotification` table
- Limited stock / Limited time image overlay

### D-7 — Communication enhancement
- C3 chat presence indicator
- C4 pre-set quick questions
- C5 voice message in chat

### D-8 — Smart helpers (AI / discovery)
- D1 Frequently Bought Together
- D3 AI Pros & Cons summary
- Q&A helpful-vote (C6 follow-on)

### D-9 — BD / Local features
- B1 district-wise delivery ETA
- B2 same-city seller badge
- B4 prayer time delivery preference
- B5 Eid / Festival pricing countdown
- B6 Hijri date alongside Gregorian

### D-10 — Promotional polish
- Promotional context strip (active flash sale banner inline)
- App download QR code (after Flutter app ships in Phase 12)

---

## Notes

- Every sub-chunk must pass its own smoke test + a regression run of all
  prior smoke tests before being marked done.
- Re-uses existing models wherever possible: `VendorProfile`, `Brand`,
  `Coupon`, `RewardLedger`, `AffiliateCommission`, `FlashSale`, `ChatMessage`,
  `ReviewImage`.
- New tables to add over the chunks: `PolicyViolation` (D-0), `Question`,
  `Answer` (D-2), `ProductPriceTier` (D-5), `StockNotification` (D-6),
  `DistrictEta` (D-9).
- Bilingual rendering throughout — every new label must have a Bengali +
  English form per project rules.
