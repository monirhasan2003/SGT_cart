"""Wave-1 polished footer pages — extracted from the static templates so
the StaticPage system can serve them in both English and Bangla.

Consumed by `flask seed-static-pages` together with `static_page_content.py`
(stub 16 pages) and `static_page_content_bn.py` (Bangla translations).
"""

WAVE1_PAGES = [{'slug': 'terms',
  'title': 'Customer Terms of Service',
  'subtitle': 'The agreement between you and SGT Cart for using sgtcart.com and the SGT Cart mobile apps.',
  'section': 'Legal',
  'contact_email': 'policy@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 100,
  'body_html': '<p class="lead small">\n'
               '\tThese Terms of Service ("<strong>Terms</strong>") form a binding contract between\n'
               '\t<strong>you</strong> (every person who visits, browses, registers or purchases on\n'
               '\tthe SGT Cart website at <a href="https://sgtcart.com">sgtcart.com</a> or any\n'
               '\trelated mobile app — collectively "the Platform") and\n'
               '\t<strong>Smart Global Trade Cart</strong>, doing business as\n'
               '\t<strong>SGT Cart</strong> ("we", "us", "our").\n'
               '\tBy creating an account or placing an order you confirm that you have read,\n'
               '\tunderstood and agreed to be bound by these Terms together with our\n'
               '\t<a href="/privacy/">Privacy Policy</a>, <a href="/cookie-policy/">Cookie Policy</a>,\n'
               '\t<a href="/refund-policy/">Refund Policy</a> and\n'
               '\t<a href="/help/buyer-protection/">Buyer Protection Program</a>.\n'
               '\tIf you do not agree, please do not use the Platform.\n'
               '</p>\n'
               '\n'
               '<h2 id="definitions">1. Definitions</h2>\n'
               '<p>In these Terms, capitalised words have the following meaning:</p>\n'
               '<table>\n'
               '\t<tr><th>Term</th><th>Meaning</th></tr>\n'
               '\t<tr><td>Platform</td><td>sgtcart.com, the SGT Cart Customer mobile app, the SGT Cart '
               'Seller Center app, the REST API at <code>/api/v1</code>, and any other channel SGT Cart '
               'operates.</td></tr>\n'
               '\t<tr><td>Customer / Buyer / "You"</td><td>An individual who browses, registers or purchases '
               'on the Platform for personal, non-commercial use.</td></tr>\n'
               '\t<tr><td>Seller / Vendor</td><td>A natural person or legal entity registered on the '
               'Platform under a separate <a href="/seller-terms/">Seller Agreement</a> who lists and sells '
               'products to Customers.</td></tr>\n'
               '\t<tr><td>Listing</td><td>A product page created by a Seller, including title, description, '
               'price, images, variants and stock.</td></tr>\n'
               '\t<tr><td>Order</td><td>A confirmed purchase request placed by a Customer for one or more '
               'Listings.</td></tr>\n'
               '\t<tr><td>Sub-Order</td><td>The portion of an Order fulfilled by a single Seller. One Order '
               'may contain multiple Sub-Orders.</td></tr>\n'
               '\t<tr><td>Reward Points</td><td>Loyalty units credited to your account on delivered Orders, '
               'redeemable at checkout. See §11.</td></tr>\n'
               '\t<tr><td>BDT / Tk</td><td>Bangladeshi Taka — the only currency the Platform transacts '
               'in.</td></tr>\n'
               '</table>\n'
               '\n'
               '<h2 id="eligibility">2. Eligibility &amp; capacity to contract</h2>\n'
               '<p>\n'
               '\tTo use the Platform you must:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Be at least <strong>18 years old</strong> (the age of majority under\n'
               '\t\tthe Majority Act, 1875 of Bangladesh) and capable of forming a legally\n'
               '\t\tbinding contract under the Contract Act 1872.</li>\n'
               '\t<li>Provide accurate, current and complete information at signup, and keep it up to '
               'date.</li>\n'
               '\t<li>Use the Platform only for lawful personal purposes — re-sale of items\n'
               '\t\tpurchased on SGT Cart through another platform requires explicit\n'
               '\t\twritten permission.</li>\n'
               '\t<li>Not be a person prohibited from receiving services under Bangladesh\n'
               '\t\tlaw or any applicable international sanctions list.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tIf you are between <strong>13 and 17</strong> you may browse the Platform but\n'
               '\tmay only place Orders through the account of a parent or legal guardian\n'
               '\twho accepts these Terms on your behalf. Children under 13 are not\n'
               '\tpermitted to register — see our\n'
               '\t<a href="/childrens-privacy/">Children\'s Privacy Policy</a>.\n'
               '</p>\n'
               '\n'
               '<h2 id="account">3. Your account</h2>\n'
               '<p>\n'
               '\tYour account is personal. You are responsible for:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Keeping your password and one-time login codes (OTPs) confidential.</li>\n'
               '\t<li>All activity that occurs through your account, whether or not authorised by you.</li>\n'
               '\t<li>Notifying us immediately at <a '
               'href="mailto:support@sgtcart.com">support@sgtcart.com</a>\n'
               '\t\tif you suspect unauthorised access.</li>\n'
               '\t<li>Updating your delivery address, contact email and mobile number so\n'
               '\t\tOrders and notifications reach you.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tWe reserve the right to suspend or close accounts that show signs of fraud,\n'
               '\tmultiple-account abuse, voucher gaming, or other behaviour that violates\n'
               '\tthese Terms or harms other users.\n'
               '</p>\n'
               '\n'
               '<h2 id="marketplace-role">4. SGT Cart\'s marketplace role</h2>\n'
               '<p>\n'
               '\t<strong>SGT Cart is an online marketplace — a venue that connects independent\n'
               '\tSellers with Customers.</strong> For every Listing:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>The <strong>Seller</strong> is the contracting party who actually\n'
               '\t\tsells the product to you.</li>\n'
               '\t<li>SGT Cart provides the technology, payment processing, dispute\n'
               '\t\tmediation, and delivery coordination — but does not own the inventory\n'
               '\t\tlisted by Sellers (unless a Listing is expressly marked\n'
               '\t\t"Sold &amp; Shipped by SGT Cart").</li>\n'
               '\t<li>The legal contract for the sale of goods is formed between you and\n'
               '\t\tthe Seller. SGT Cart is not a party to that contract of sale, except\n'
               '\t\twhere it acts as Seller of record.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tDespite this, SGT Cart commits to the <strong>customer protections</strong>\n'
               '\tdescribed in <a href="/help/buyer-protection/">Buyer Protection</a>,\n'
               '\t<a href="/refund-policy/">Refund Policy</a> and\n'
               '\t<a href="/dispute-resolution/">Dispute Resolution</a> — so you have a\n'
               '\tclear path to remedy if a Seller fails to deliver, delivers the wrong\n'
               '\titem, or sells a counterfeit.\n'
               '</p>\n'
               '\n'
               '<h2 id="listings">5. Listings &amp; accuracy</h2>\n'
               '<p>\n'
               '\tSellers are responsible for the accuracy of every Listing, including\n'
               '\ttitle, description, photographs, specifications, price, weight, variant\n'
               '\toptions and stock quantity. SGT Cart screens Listings for prohibited\n'
               '\titems, counterfeits and policy violations, but does not warrant that\n'
               '\tevery Listing is error-free or that the product depicted is identical\n'
               '\tin every detail to the item shipped.\n'
               '</p>\n'
               '<p>\n'
               '\tIf you receive a product that materially differs from its Listing, you\n'
               '\tmay seek a refund or replacement under §10 and the\n'
               '\t<a href="/refund-policy/">Refund Policy</a>.\n'
               '</p>\n'
               '\n'
               '<h2 id="pricing">6. Pricing &amp; currency</h2>\n'
               '<p>\n'
               '\tAll prices on the Platform are shown in <strong>Bangladeshi Taka (BDT, Tk)</strong>\n'
               '\tand are <strong>inclusive of VAT</strong> where applicable. Sellers are required\n'
               '\tto display VAT-inclusive pricing under NBR rules.\n'
               '</p>\n'
               '<p>\n'
               '\tShipping fees, optional add-ons and Cash-on-Delivery surcharges (if any)\n'
               '\tare shown separately at checkout before you confirm the Order.\n'
               '\tPromotional discounts, coupon savings, reward-point redemptions and\n'
               '\tbulk-pricing tiers are likewise displayed before payment.\n'
               '</p>\n'
               '<p>\n'
               '\tIf a Listing displays a price that is clearly a mistake (for example,\n'
               '\ta Tk 50,000 product mistakenly listed at Tk 50), SGT Cart and the\n'
               '\tSeller reserve the right to cancel the affected Sub-Order and refund\n'
               '\tin full. We will notify you and never charge a price you did not\n'
               '\tconfirm at checkout.\n'
               '</p>\n'
               '\n'
               '<h2 id="orders">7. Placing an order</h2>\n'
               '<p>\n'
               '\tWhen you place an Order:\n'
               '</p>\n'
               '<ol>\n'
               '\t<li>You make an <strong>offer to buy</strong> the items in your cart from the\n'
               '\t\trespective Sellers, on the terms shown at checkout.</li>\n'
               '\t<li>SGT Cart sends you an <strong>order confirmation</strong> email and an\n'
               '\t\tin-app notification with a unique Order number.</li>\n'
               '\t<li>An Order is <strong>accepted</strong> by a Seller only when that Seller\n'
               '\t\tmarks the Sub-Order as "processing". Until then the Seller may\n'
               '\t\tdecline (typically for out-of-stock, address-unreachable, or\n'
               '\t\tpayment-not-cleared reasons) and you will be refunded in full.</li>\n'
               '</ol>\n'
               '<p>\n'
               '\tMulti-vendor Orders are split into Sub-Orders, one per Seller. Each\n'
               '\tSub-Order is fulfilled and may be cancelled or refunded independently.\n'
               '</p>\n'
               '\n'
               '<h2 id="payment">8. Payment</h2>\n'
               '<p>\n'
               '\tThe Platform supports the following payment methods (full details at\n'
               '\t<a href="/help/payment-methods/">Payment Methods</a>):\n'
               '</p>\n'
               '<ul>\n'
               '\t<li><strong>Cash on Delivery (COD)</strong> — pay the delivery agent in cash on '
               'receipt.</li>\n'
               '\t<li><strong>bKash &amp; Nagad</strong> — via mobile-wallet redirection.</li>\n'
               '\t<li><strong>Card (Visa, MasterCard, AMEX, Discover)</strong> — via SSLCommerz, a '
               'PCI-DSS-compliant gateway. SGT Cart never sees or stores your full card number.</li>\n'
               '\t<li><strong>Reward Points</strong> — redeem your balance at checkout up to the cap '
               'displayed.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tBy submitting payment information you authorise SGT Cart and our\n'
               '\tpayment processor to charge the total displayed at checkout. Failed\n'
               '\tprepaid payments leave the Order in an unpaid state — you can retry\n'
               '\tfrom your <a href="/my-orders/">My Orders</a> page.\n'
               '</p>\n'
               '\n'
               '<h2 id="delivery">9. Delivery &amp; risk of loss</h2>\n'
               '<p>\n'
               '\tEstimated delivery times are shown on each product page and at checkout,\n'
               "\tbased on the destination district and the Seller's processing time\n"
               '\t(typically 1-7 business days within Bangladesh). Delivery time may\n'
               '\tvary during national holidays, force-majeure events, and severe weather.\n'
               '</p>\n'
               '<p>\n'
               '\t<strong>Risk of loss</strong> transfers to you upon successful delivery\n'
               '\tto the address you provided. If delivery fails because nobody was\n'
               '\tavailable, the carrier will reattempt up to twice; thereafter the\n'
               '\tSub-Order may be cancelled and refunded (less actual return-shipping\n'
               '\tcost where applicable). Full details: <a href="/shipping/">Shipping &amp; Delivery</a>.\n'
               '</p>\n'
               '\n'
               '<h2 id="returns">10. Returns &amp; refunds</h2>\n'
               '<p>\n'
               '\tYou may return most products within <strong>7 days of delivery</strong> if\n'
               '\tthey are unused, in original packaging, and with all tags. Some categories\n'
               '\tare non-returnable for health or hygiene reasons (perishables, intimate\n'
               '\twear, custom-made goods) — these are clearly marked on the product page.\n'
               '</p>\n'
               '<p>\n'
               '\tDamaged-on-arrival, wrong-item, or counterfeit deliveries are eligible\n'
               '\tfor a <strong>full refund or replacement at no return-shipping cost to you</strong>,\n'
               '\tregardless of category. The full procedure, timelines and refund methods\n'
               '\tlive in the <a href="/refund-policy/">Refund Policy</a> and\n'
               '\t<a href="/returns/">Returns</a> pages.\n'
               '</p>\n'
               '\n'
               '<h2 id="rewards">11. Rewards &amp; promotions</h2>\n'
               '<p>\n'
               '\tReward Points are credited to your account when a Sub-Order is marked\n'
               '\tdelivered, at a rate disclosed in\n'
               '\t<a href="/help/rewards/">Rewards Program</a>. Points are non-transferable\n'
               '\tand have no cash-out value; they can only be redeemed at checkout on\n'
               '\tsubsequent Orders.\n'
               '</p>\n'
               '<p>\n'
               '\tCoupons, flash sales, sponsored placements and "free-shipping threshold"\n'
               '\tpromotions are governed by their individual terms shown at the point\n'
               '\tof use. Promotions are non-stackable unless explicitly allowed. SGT\n'
               '\tCart reserves the right to revoke promotional benefits gained through\n'
               '\tabuse (account farming, voucher resale, click fraud).\n'
               '</p>\n'
               '\n'
               '<h2 id="ugc">12. Reviews, Q&amp;A, user content</h2>\n'
               '<p>\n'
               '\tWhen you post a review, rating, photo, Q&amp;A entry, or any other\n'
               '\tcontent on the Platform ("User Content"), you grant SGT Cart a\n'
               '\tworldwide, royalty-free, non-exclusive licence to host, display,\n'
               '\treproduce, translate and excerpt that content in any medium for the\n'
               '\tpurpose of operating and promoting the Platform.\n'
               '</p>\n'
               '<p>\n'
               '\tYou promise that your User Content:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>is original to you or you have rights to share it;</li>\n'
               '\t<li>does not contain personal contact details, phone numbers, off-platform URLs, or '
               'anything that violates our <a href="/sell/anti-disintermediation/">Anti-Disintermediation '
               'Policy</a>;</li>\n'
               '\t<li>is not defamatory, obscene, hateful, harassing or unlawful;</li>\n'
               '\t<li>only reviews products you actually purchased — verified-purchase enforcement '
               'applies.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tWe may remove User Content that violates these rules without prior notice.\n'
               '</p>\n'
               '\n'
               '<h2 id="prohibited">13. Prohibited customer conduct</h2>\n'
               '<p>You agree not to:</p>\n'
               '<ul>\n'
               '\t<li>Use the Platform for any illegal purpose or in violation of Bangladesh law.</li>\n'
               '\t<li>Buy from, or attempt to make payment to, sellers outside the Platform after using SGT '
               'Cart to discover them.</li>\n'
               '\t<li>Defraud Sellers (e.g., false damaged-on-arrival claims, friendly fraud '
               'chargebacks).</li>\n'
               '\t<li>Resell items purchased on SGT Cart without authorisation in a way that misleads '
               'buyers.</li>\n'
               '\t<li>Use bots, scrapers, or automated tools to access the Platform without our written '
               'consent.</li>\n'
               "\t<li>Reverse-engineer, decompile, or tamper with the Platform's code or APIs.</li>\n"
               '\t<li>Upload viruses, malware, or any code intended to disrupt the Platform.</li>\n'
               '\t<li>Impersonate another person, a Seller, or an SGT Cart staff member.</li>\n'
               '</ul>\n'
               '\n'
               '<h2 id="suspension">14. Suspension &amp; termination</h2>\n'
               '<p>\n'
               '\tWe may, at our discretion and without prior notice, suspend or\n'
               '\tpermanently close your account, cancel pending Orders, revoke unused\n'
               '\treward points, and refuse future service if we have reasonable grounds\n'
               '\tto believe you have violated these Terms, defrauded a Seller, or\n'
               '\tcreated risk for the Platform. You may also close your account at any\n'
               '\ttime by writing to <a href="mailto:support@sgtcart.com">support@sgtcart.com</a>;\n'
               '\tpending Orders and delivered-but-not-paid balances will be settled\n'
               '\tfirst.\n'
               '</p>\n'
               '\n'
               '<h2 id="liability">15. Disclaimers &amp; limitation of liability</h2>\n'
               '<p>\n'
               '\tThe Platform is provided <strong>"as is"</strong>. We make no warranties about\n'
               '\tuninterrupted availability, error-free operation, or that the Platform\n'
               '\tis free of viruses. To the maximum extent permitted by Bangladesh\n'
               '\tlaw:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>SGT Cart is not liable for indirect, incidental, special, punitive or consequential '
               'damages.</li>\n'
               '\t<li>Our total aggregate liability to you in connection with any Order is capped at the '
               'amount you actually paid for that Order.</li>\n'
               '\t<li>Nothing in these Terms excludes or limits liability for death, personal injury caused '
               'by our negligence, or fraud.</li>\n'
               '</ul>\n'
               '<blockquote>\n'
               '\tThis limitation does not apply to your statutory consumer-protection\n'
               '\trights under the Consumer Rights Protection Act 2009 ("CRPA"), which\n'
               '\tremain in force.\n'
               '</blockquote>\n'
               '\n'
               '<h2 id="changes">16. Changes to these terms</h2>\n'
               '<p>\n'
               '\tWe may revise these Terms from time to time. When we make a material\n'
               '\tchange, we will post the updated version with a new "Last reviewed"\n'
               '\tdate and notify registered users by email and in-app notification at\n'
               '\tleast <strong>14 days before</strong> the new version takes effect. Your\n'
               '\tcontinued use of the Platform after that date constitutes acceptance.\n'
               '\tPast versions are available on request from\n'
               '\t<a href="mailto:policy@sgtcart.com">policy@sgtcart.com</a>.\n'
               '</p>\n'
               '\n'
               '<h2 id="governing">17. Governing law &amp; jurisdiction</h2>\n'
               '<p>\n'
               '\tThese Terms are governed by the <strong>laws of Bangladesh</strong>. The\n'
               '\t<strong>courts of Dhaka</strong> have exclusive jurisdiction over any\n'
               '\tdispute arising from or connected with these Terms or your use of\n'
               '\tthe Platform.\n'
               '</p>\n'
               '<p>\n'
               '\tIf you are located outside Bangladesh, this clause does not deprive you\n'
               '\tof consumer-protection rights mandatorily granted by your local law.\n'
               '\tHowever, the primary forum remains the Dhaka courts, and the\n'
               '\tsubstantive law remains Bangladesh law.\n'
               '</p>\n'
               '\n'
               '<h2 id="disputes">18. Dispute resolution &amp; contact</h2>\n'
               '<p>\n'
               '\tBefore approaching a court, you agree to use our internal resolution\n'
               '\tsteps: direct chat with the Seller → Buyer Protection claim → SGT\n'
               '\tmediation → CRPA §76 redressal → arbitration under the Arbitration\n'
               '\tAct 2001. The full ladder is in our\n'
               '\t<a href="/dispute-resolution/">Dispute Resolution &amp; Arbitration</a> policy.\n'
               '</p>\n'
               '<p>\n'
               '\tFor any other questions about these Terms, write to\n'
               '\t<a href="mailto:policy@sgtcart.com">policy@sgtcart.com</a> or the\n'
               '\tgeneral support address <a href="mailto:support@sgtcart.com">support@sgtcart.com</a>.\n'
               '</p>',
  'toc': [{'anchor': 'definitions', 'label': '1. Definitions'},
          {'anchor': 'eligibility', 'label': '2. Eligibility & capacity'},
          {'anchor': 'account', 'label': '3. Your account'},
          {'anchor': 'marketplace-role', 'label': "4. SGT Cart's marketplace role"},
          {'anchor': 'listings', 'label': '5. Listings & accuracy'},
          {'anchor': 'pricing', 'label': '6. Pricing & currency'},
          {'anchor': 'orders', 'label': '7. Placing an order'},
          {'anchor': 'payment', 'label': '8. Payment'},
          {'anchor': 'delivery', 'label': '9. Delivery & risk of loss'},
          {'anchor': 'returns', 'label': '10. Returns & refunds'},
          {'anchor': 'rewards', 'label': '11. Rewards & promotions'},
          {'anchor': 'ugc', 'label': '12. Reviews, Q&A, user content'},
          {'anchor': 'prohibited', 'label': '13. Prohibited customer conduct'},
          {'anchor': 'suspension', 'label': '14. Suspension & termination'},
          {'anchor': 'liability', 'label': '15. Disclaimers & limitation of liability'},
          {'anchor': 'changes', 'label': '16. Changes to these terms'},
          {'anchor': 'governing', 'label': '17. Governing law & jurisdiction'},
          {'anchor': 'disputes', 'label': '18. Dispute resolution & contact'}],
  'faq': [{'q': 'Do I need an account to browse?',
           'a': 'No — you can browse freely. An account is required only when you place an Order, write a '
                'review or chat with a Seller.'},
          {'q': 'Are these terms different from the Seller Agreement?',
           'a': 'Yes. These Terms govern Customers. Sellers have a separate, more detailed agreement at '
                '/seller-terms/ that includes KYC, payouts, performance standards and commission.'},
          {'q': 'What happens to my reward points if I close my account?',
           'a': 'Unredeemed points lapse on account closure. We recommend you redeem them on a final Order '
                'before closing.'},
          {'q': 'Can SGT Cart change a price after I order?',
           'a': 'No. The price you confirmed at checkout is the price you pay. The only exception is the '
                'mistake-price clause in §6 — and even there we refund in full, never charge more.'},
          {'q': 'Do you operate outside Bangladesh?',
           'a': 'Currently sgtcart.com ships within Bangladesh only. International shipping will be opened '
                'in a later phase; until then, international users may browse but not place delivery '
                'Orders.'}],
  'related': [{'href': '/privacy/',
               'title': 'Privacy Policy',
               'desc': 'How we collect, use and protect your personal data.'},
              {'href': '/refund-policy/',
               'title': 'Refund Policy',
               'desc': 'Timelines and methods for getting your money back.'},
              {'href': '/dispute-resolution/',
               'title': 'Dispute Resolution',
               'desc': 'The full ladder from chat to arbitration.'},
              {'href': '/help/buyer-protection/',
               'title': 'Buyer Protection',
               'desc': 'What we cover and how to file a claim.'}]},
 {'slug': 'privacy',
  'title': 'Privacy Policy',
  'subtitle': 'How Smart Global Trade Cart collects, uses, shares and protects your personal data.',
  'section': 'Legal',
  'contact_email': 'privacy@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 110,
  'body_html': '<p class="lead small">\n'
               '\tYour privacy matters to us. This Privacy Policy explains how\n'
               '\t<strong>Smart Global Trade Cart</strong> ("SGT Cart", "we", "us") collects,\n'
               '\tuses, shares and safeguards your personal data when you use sgtcart.com,\n'
               '\tthe SGT Cart Customer app, the Seller Center app, our REST API, and any\n'
               '\tother service we operate (together, "the Platform").\n'
               '</p>\n'
               '<p class="small">\n'
               '\tIt applies to <strong>customers, sellers and visitors</strong>. Separate\n'
               '\tnotices may apply if you join SGT Cart as an employee or contractor.\n'
               '</p>\n'
               '\n'
               '<h2 id="who-we-are">1. Who we are</h2>\n'
               '<p>\n'
               '\tSGT Cart is operated by <strong>Smart Global Trade Cart</strong>, with\n'
               '\tits registered address at Mirpur, Dhaka 1216, Bangladesh. Our Data\n'
               '\tProtection contact is <a href="mailto:privacy@sgtcart.com">privacy@sgtcart.com</a>.\n'
               '</p>\n'
               '<p>\n'
               '\tFor the purposes of data protection — including the principles in the\n'
               '\tInformation &amp; Communication Technology Act 2006, the Digital\n'
               '\tSecurity Act 2018 and the Bangladesh Personal Data Protection\n'
               '\tframeworks under preparation — we act as a <strong>data controller</strong>\n'
               '\tfor the data we collect about you, and as a <strong>data processor</strong>\n'
               '\twhen we process customer data on behalf of a Seller for the limited\n'
               '\tpurpose of fulfilling that Order.\n'
               '</p>\n'
               '\n'
               '<h2 id="what-we-collect">2. What personal data we collect</h2>\n'
               '<p>We collect the following categories of personal data:</p>\n'
               '<table>\n'
               '\t<tr><th>Category</th><th>Examples</th></tr>\n'
               '\t<tr><td>Identity</td><td>Name, gender (if you provide it), date of birth (if you provide '
               'it), profile photo (optional).</td></tr>\n'
               '\t<tr><td>Contact</td><td>Email, mobile number, delivery addresses (street, city, district, '
               'postal code).</td></tr>\n'
               '\t<tr><td>Account &amp; credentials</td><td>Password hash, login-time one-time codes (OTP), '
               'session identifiers, mobile-app device tokens.</td></tr>\n'
               '\t<tr><td>Seller KYC <em>(sellers only)</em></td><td>NID number + scanned NID image, Trade '
               'Licence number + scanned licence, TIN, bank-account / bKash / Nagad numbers, shop '
               'address.</td></tr>\n'
               '\t<tr><td>Order &amp; payment</td><td>Cart contents, order history, payment method, payment '
               'tokens (we never see your full card number — SSLCommerz handles it), refund '
               'history.</td></tr>\n'
               '\t<tr><td>Behavioural / analytics</td><td>Product views, searches (text + image + voice '
               'transcripts), wishlist items, reviews you wrote, Q&amp;A you posted, chat '
               'messages.</td></tr>\n'
               '\t<tr><td>Device &amp; technical</td><td>IP address, browser type and version, operating '
               'system, mobile device identifier, approximate location (from IP), screen size, language, '
               'timezone.</td></tr>\n'
               '\t<tr><td>Marketing &amp; preferences</td><td>Email-notification preferences, language '
               'choice, currency choice (BDT only at present).</td></tr>\n'
               '</table>\n'
               '<p>\n'
               '\t<strong>We never ask for and never store:</strong> your full credit-card\n'
               '\tnumber, card CVV, internet-banking password, NID PIN, mobile-wallet PIN.\n'
               '\tThese either stay with the payment processor (SSLCommerz, bKash, Nagad)\n'
               '\tor are never asked for at all.\n'
               '</p>\n'
               '\n'
               '<h2 id="how-we-collect">3. How we collect it</h2>\n'
               '<ul>\n'
               '\t<li><strong>Directly from you</strong> — when you sign up, place an Order,\n'
               '\t\twrite a review, upload a profile image, complete seller KYC, or\n'
               '\t\tcontact our support team.</li>\n'
               '\t<li><strong>Automatically</strong> — via cookies, server logs,\n'
               '\t\tanalytics scripts (first-party only), socket events\n'
               '\t\t(chat-presence, viewer counts).</li>\n'
               '\t<li><strong>From third parties</strong> — payment processors confirm\n'
               '\t\tpayment status; delivery partners confirm delivery; the BFIU may\n'
               '\t\tcheck sanctioned lists for high-value sellers (AML / KYC).</li>\n'
               '</ul>\n'
               '\n'
               '<h2 id="lawful-basis">4. Lawful basis for processing</h2>\n'
               '<table>\n'
               '\t<tr><th>Purpose</th><th>Lawful basis</th></tr>\n'
               '\t<tr><td>Account creation, Order processing, customer support</td><td>Performance of the '
               'contract you entered into with us under the <a href="/terms/">Customer Terms</a>.</td></tr>\n'
               '\t<tr><td>Tax records, invoice retention, regulatory reporting</td><td>Compliance with '
               'Bangladesh tax (NBR), customs, and AML obligations.</td></tr>\n'
               '\t<tr><td>Fraud detection, dispute resolution, security monitoring</td><td>Our legitimate '
               'interest in keeping the Platform safe and fair.</td></tr>\n'
               '\t<tr><td>Marketing emails, push notifications</td><td>Your consent (you may withdraw it '
               'anytime in <a href="/profile-info/">Account → Notifications</a>).</td></tr>\n'
               '\t<tr><td>AI pros/cons summary from reviews</td><td>Our legitimate interest in helping '
               'buyers make informed decisions, with safeguards against personally identifying '
               'reviewers.</td></tr>\n'
               '</table>\n'
               '\n'
               '<h2 id="how-we-use">5. How we use your data</h2>\n'
               '<ul>\n'
               '\t<li>Operate your account, authenticate logins, deliver Orders to your address.</li>\n'
               '\t<li>Process payments and refunds through SSLCommerz, bKash, Nagad and Cash on '
               'Delivery.</li>\n'
               '\t<li>Provide customer service, mediate Buyer/Seller disputes, investigate complaints.</li>\n'
               '\t<li>Personalise the Platform — show "Similar products", "Customers Also Viewed",\n'
               '\t\t"Frequently Bought Together", reward-point balance, and AI-summarised\n'
               '\t\treview pros/cons.</li>\n'
               '\t<li>Send transactional emails / SMS (order placed, paid, shipped, delivered).</li>\n'
               '\t<li>Send promotional emails about flash sales, coupons and new categories (only with your '
               'consent).</li>\n'
               '\t<li>Detect and prevent fraud, abuse and counterfeit listings.</li>\n'
               '\t<li>Enforce our <a href="/sell/anti-disintermediation/">Anti-Disintermediation Policy</a> '
               '— automatically redact phone numbers and contact details from chat, reviews and '
               'Q&amp;A.</li>\n'
               '\t<li>Comply with legal orders, court summons, and tax/AML reporting.</li>\n'
               '\t<li>Improve the Platform — A/B test layouts, monitor performance, fix bugs.</li>\n'
               '</ul>\n'
               '\n'
               '<h2 id="sharing">6. Who we share your data with</h2>\n'
               '<p>We share strictly on a need-to-know basis with:</p>\n'
               '<ul>\n'
               '\t<li><strong>The Seller</strong> for an Order — your name, delivery address\n'
               '\t\tand mobile number, so the Seller can ship the right item.\n'
               '\t\tSellers are bound by the <a href="/seller-terms/">Seller Agreement</a>\n'
               '\t\tto use this data only for fulfilling and supporting the Order.</li>\n'
               '\t<li><strong>Payment processors</strong> — SSLCommerz (cards), bKash, Nagad — for\n'
               '\t\tpayment authorisation and reconciliation.</li>\n'
               '\t<li><strong>Delivery partners</strong> — your name, address and mobile,\n'
               '\t\tso they can deliver and reach you on the way.</li>\n'
               '\t<li><strong>Hosting and infrastructure providers</strong> — under written\n'
               '\t\tdata-processing agreements that cap them to operating our systems.</li>\n'
               '\t<li><strong>Government authorities</strong> — when ordered by Bangladesh\n'
               '\t\tlaw (court orders, tax inquiry, fraud investigation, BFIU notices,\n'
               '\t\tICT Act §28 / §57 takedown demands).</li>\n'
               '\t<li><strong>Professional advisers</strong> — auditors, lawyers — under\n'
               '\t\tconfidentiality obligations.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\t<strong>We do not sell your personal data.</strong> We do not share it\n'
               '\twith advertising networks. We do not allow third parties to track you\n'
               '\tacross other sites for marketing purposes.\n'
               '</p>\n'
               '\n'
               '<h2 id="international">7. International transfers</h2>\n'
               '<p>\n'
               '\tOur primary servers are hosted in data centres serving the Bangladesh\n'
               '\tregion. Some support tools (email delivery, error monitoring) operate\n'
               '\tfrom outside Bangladesh. When we transfer your data abroad, we use\n'
               '\tcontractual safeguards (Standard Contractual Clauses or equivalent)\n'
               '\tto maintain the same level of protection. When the Platform opens to\n'
               '\tinternational shipping in a later phase, we will publish a fuller\n'
               '\tcross-border transfer addendum.\n'
               '</p>\n'
               '\n'
               '<h2 id="retention">8. How long we keep it</h2>\n'
               '<table>\n'
               '\t<tr><th>Data</th><th>Retention period</th></tr>\n'
               '\t<tr><td>Account record (active)</td><td>For as long as your account is active.</td></tr>\n'
               '\t<tr><td>Account record (closed)</td><td>2 years after closure, then anonymised. Required '
               'to honour any pending disputes or chargebacks.</td></tr>\n'
               '\t<tr><td>Order &amp; invoice data</td><td>7 years (NBR / Income Tax retention '
               'rule).</td></tr>\n'
               '\t<tr><td>Seller KYC documents</td><td>5 years after the seller account is closed (BFIU / '
               'AML requirement).</td></tr>\n'
               '\t<tr><td>Marketing email logs</td><td>2 years after the last interaction.</td></tr>\n'
               '\t<tr><td>Chat messages</td><td>3 years (for dispute evidence), then deleted.</td></tr>\n'
               '\t<tr><td>Web-server access logs</td><td>90 days (for security and abuse '
               'investigation).</td></tr>\n'
               '</table>\n'
               '\n'
               '<h2 id="security">9. Security measures</h2>\n'
               '<p>\n'
               '\tWe protect your data with technical and organisational measures\n'
               '\tappropriate to the risk:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li><strong>Encryption in transit</strong> — TLS 1.2+ on every connection.</li>\n'
               '\t<li><strong>Encryption at rest</strong> — sensitive fields (KYC documents, payment tokens) '
               'encrypted on disk.</li>\n'
               '\t<li><strong>Password storage</strong> — only salted hashes (Werkzeug PBKDF2). We never '
               'store passwords in plaintext.</li>\n'
               '\t<li><strong>OTP for customer logins</strong> — codes valid for 10 minutes, single-use, '
               'rate-limited.</li>\n'
               '\t<li><strong>PCI-DSS scope reduction</strong> — card data goes directly to SSLCommerz; we '
               'never touch the PAN.</li>\n'
               '\t<li><strong>CSRF protection, rate limiting, HSTS, Content-Security-Policy</strong> on '
               'every page.</li>\n'
               '\t<li><strong>Audit log</strong> for all admin actions.</li>\n'
               '\t<li><strong>Least-privilege access</strong> — only on-call staff can access production '
               'databases, and every access is logged.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tIf we ever discover a personal-data breach affecting your account, we\n'
               '\twill notify you within <strong>72 hours</strong> by email and post a\n'
               '\tnotice on the Platform with the facts known to us, the likely impact\n'
               '\tand the steps to take.\n'
               '</p>\n'
               '\n'
               '<h2 id="your-rights">10. Your rights</h2>\n'
               '<p>You have the following rights over your personal data:</p>\n'
               '<ul>\n'
               '\t<li><strong>Access</strong> — request a copy of the data we hold about you.</li>\n'
               '\t<li><strong>Correction</strong> — fix anything inaccurate or incomplete (most fields are '
               'editable in <a href="/profile-info/">Account</a>).</li>\n'
               '\t<li><strong>Deletion</strong> — request closure of your account and erasure of personal '
               'data (subject to legal retention obligations above).</li>\n'
               '\t<li><strong>Portability</strong> — receive your data in a machine-readable JSON '
               'export.</li>\n'
               '\t<li><strong>Objection</strong> — opt out of marketing communications at any time.</li>\n'
               '\t<li><strong>Withdraw consent</strong> — where we relied on your consent, you can withdraw '
               'it without affecting past processing.</li>\n'
               '\t<li><strong>Complaint</strong> — lodge a complaint with the National Consumer Right '
               'Protection Department or any future Bangladesh data-protection authority.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tTo exercise any of these rights, write to <a '
               'href="mailto:privacy@sgtcart.com">privacy@sgtcart.com</a>.\n'
               '\tWe respond within <strong>30 days</strong>. There is no fee unless requests\n'
               '\tare clearly excessive or repeated.\n'
               '</p>\n'
               '\n'
               '<h2 id="children">11. Children\'s privacy</h2>\n'
               '<p>\n'
               '\tThe Platform is not directed at children under <strong>13</strong>. We do not\n'
               '\tknowingly collect personal data from children under 13. If we learn that\n'
               '\twe have collected such data, we delete it without delay. Customers\n'
               '\taged 13-17 may use the Platform only through the account of a parent\n'
               '\tor legal guardian (see <a href="/childrens-privacy/">Children\'s Privacy Policy</a>).\n'
               '</p>\n'
               '\n'
               '<h2 id="cookies">12. Cookies</h2>\n'
               '<p>\n'
               '\tWe use cookies and similar storage technologies to keep you signed in,\n'
               '\tremember your cart, store your language and cookie-consent preference,\n'
               '\tand measure aggregate site performance. The full list, including\n'
               '\tcategories (necessary, preferences, analytics) and how to manage them,\n'
               '\tlives in our <a href="/cookie-policy/">Cookie Policy</a>. You can also\n'
               '\trevisit your consent decision at any time by clearing\n'
               '\t<code>sgt_cookie_consent</code> from your browser storage.\n'
               '</p>\n'
               '\n'
               '<h2 id="updates">13. Changes to this policy</h2>\n'
               '<p>\n'
               '\tWe may update this Privacy Policy. Material changes are notified by\n'
               '\temail and in-app notification at least 14 days before the new version\n'
               '\ttakes effect. The "Last reviewed" date at the bottom of this page\n'
               '\talways reflects the current version. Past versions are available on\n'
               '\trequest from <a href="mailto:privacy@sgtcart.com">privacy@sgtcart.com</a>.\n'
               '</p>\n'
               '\n'
               '<h2 id="contact-dpo">14. Contact &amp; supervisory authority</h2>\n'
               '<p>\n'
               '\tFor any question about this Privacy Policy, your data, or to exercise\n'
               '\tyour rights, write to:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li><strong>Data Protection contact:</strong> <a '
               'href="mailto:privacy@sgtcart.com">privacy@sgtcart.com</a></li>\n'
               '\t<li><strong>Postal:</strong> Smart Global Trade Cart, Mirpur, Dhaka 1216, Bangladesh</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tIf you are not satisfied with our response, you may lodge a complaint with the\n'
               '\tNational Consumer Right Protection Department under the Consumer Rights\n'
               '\tProtection Act 2009, or any future data-protection authority established\n'
               '\tin Bangladesh.\n'
               '</p>',
  'toc': [{'anchor': 'who-we-are', 'label': '1. Who we are'},
          {'anchor': 'what-we-collect', 'label': '2. What personal data we collect'},
          {'anchor': 'how-we-collect', 'label': '3. How we collect it'},
          {'anchor': 'lawful-basis', 'label': '4. Lawful basis for processing'},
          {'anchor': 'how-we-use', 'label': '5. How we use your data'},
          {'anchor': 'sharing', 'label': '6. Who we share it with'},
          {'anchor': 'international', 'label': '7. International transfers'},
          {'anchor': 'retention', 'label': '8. How long we keep it'},
          {'anchor': 'security', 'label': '9. Security measures'},
          {'anchor': 'your-rights', 'label': '10. Your rights'},
          {'anchor': 'children', 'label': "11. Children's privacy"},
          {'anchor': 'cookies', 'label': '12. Cookies'},
          {'anchor': 'updates', 'label': '13. Changes to this policy'},
          {'anchor': 'contact-dpo', 'label': '14. Contact & supervisory authority'}],
  'faq': [{'q': 'Do you sell my data to advertisers?',
           'a': 'No. SGT Cart does not sell personal data to advertisers, brokers, or any third party. We '
                'share data only as listed in §6 — Sellers (for your Order), payment processors, delivery '
                'partners and as required by law.'},
          {'q': 'Can I delete my account permanently?',
           'a': 'Yes. Email privacy@sgtcart.com with your registered address. We close the account within 30 '
                'days and erase personal data, subject only to data we are legally required to retain (e.g. '
                'invoices for 7 years per NBR rules).'},
          {'q': 'How do I download my data?',
           'a': 'Request a JSON export from privacy@sgtcart.com. We deliver it within 30 days, free of '
                'charge, encrypted to your registered email.'},
          {'q': 'Is my chat with a seller private?',
           'a': 'Only you, the seller and our compliance team can see a vendor chat. Compliance access is '
                'logged and used only for enforcing the Anti-Disintermediation Policy and resolving '
                'disputes.'},
          {'q': 'What if my data is breached?',
           'a': "We notify affected users within 72 hours by email, explain what happened and what we're "
                'doing about it, and publish a public notice on the Platform.'}],
  'related': [{'href': '/cookie-policy/',
               'title': 'Cookie Policy',
               'desc': 'Which cookies we set and how to manage them.'},
              {'href': '/terms/', 'title': 'Customer Terms', 'desc': 'The main contract for using SGT Cart.'},
              {'href': '/childrens-privacy/',
               'title': "Children's Privacy",
               'desc': 'Protections for users under 18.'},
              {'href': '/security/', 'title': 'Security Practices', 'desc': 'How we keep your data safe.'}]},
 {'slug': 'seller-terms',
  'title': 'Seller Agreement',
  'subtitle': 'The legal agreement between Smart Global Trade Cart and every Seller listing on SGT Cart.',
  'section': 'Legal',
  'contact_email': 'policy@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 120,
  'body_html': '<p class="lead small">\n'
               '\tThis Seller Agreement ("<strong>Agreement</strong>") is the binding contract\n'
               '\tbetween <strong>Smart Global Trade Cart</strong> (operating SGT Cart at\n'
               '\tsgtcart.com — "SGT Cart", "we", "us") and every individual or legal\n'
               '\tentity that registers a Seller account on the Platform ("<strong>Seller</strong>",\n'
               '\t"you", "your"). It supplements — and where there is conflict, prevails over — the\n'
               '\tgeneral <a href="/terms/">Customer Terms of Service</a> for the limited\n'
               '\tpurpose of Seller-side obligations.\n'
               '</p>\n'
               '<blockquote class="small">\n'
               '\tBy submitting a Seller registration or by listing a product, you accept\n'
               '\tthis Agreement in full. If you do not agree, do not register as a Seller.\n'
               '</blockquote>\n'
               '\n'
               '<h2 id="defs">1. Definitions</h2>\n'
               '<p>\n'
               '\tCapitalised terms have the meaning given in the\n'
               '\t<a href="/terms/">Customer Terms</a>. In addition: "<strong>Sub-Order</strong>"\n'
               '\tis the portion of a customer Order placed with you; "<strong>Listing</strong>"\n'
               '\tis a single product page you create; "<strong>Commission</strong>" is\n'
               '\tSGT Cart\'s per-Sub-Order fee under §11; "<strong>Wallet Balance</strong>"\n'
               '\tis the net amount payable to you after Commission, refunds and adjustments,\n'
               '\theld in your in-app vendor wallet until payout.\n'
               '</p>\n'
               '\n'
               '<h2 id="eligibility">2. Eligibility</h2>\n'
               '<p>To register as a Seller you must:</p>\n'
               '<ul>\n'
               '\t<li>Be at least 18 years old.</li>\n'
               '\t<li>Be a <strong>Bangladesh resident</strong> (individual) or a legal entity registered in '
               'Bangladesh (proprietorship, partnership, company).</li>\n'
               '\t<li>Hold a valid <strong>National ID (NID)</strong>, a valid\n'
               '\t\t<strong>Trade Licence</strong> issued by the local City Corporation\n'
               '\t\tor Pourashava, and a current <strong>Taxpayer Identification Number\n'
               '\t\t(TIN)</strong> from the National Board of Revenue.</li>\n'
               '\t<li>Maintain a Bangladeshi bank account, bKash agent or Nagad account in\n'
               '\t\tthe name of the seller — for receiving payouts.</li>\n'
               '\t<li>Not be on any Bangladesh, OFAC, EU, UN or BFIU sanctioned-persons list.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tWhen international shipping launches in a later phase, this Agreement\n'
               '\twill be amended to include cross-border-seller eligibility.\n'
               '</p>\n'
               '\n'
               '<h2 id="kyc">3. KYC &amp; verification</h2>\n'
               '<p>Before your shop goes live, you must submit:</p>\n'
               '<table>\n'
               '\t<tr><th>Document</th><th>Required for</th></tr>\n'
               '\t<tr><td>NID front + back (or passport for foreigners) — clear scan / '
               'photo</td><td>Identity verification of the shop owner (individual or representative officer '
               'of a company).</td></tr>\n'
               '\t<tr><td>Trade Licence — clear scan</td><td>Right to do business in Bangladesh.</td></tr>\n'
               '\t<tr><td>TIN certificate (optional but recommended)</td><td>Tax records, automated VAT '
               'submission.</td></tr>\n'
               '\t<tr><td>Bank statement first page OR bKash/Nagad account screenshot</td><td>Confirming '
               'payout-account ownership.</td></tr>\n'
               '\t<tr><td>Shop address with a photo of the storefront (for physical stores)</td><td>Fraud '
               'prevention; helps customers trust the seller.</td></tr>\n'
               '</table>\n'
               '<p>\n'
               '\tAn SGT Cart admin reviews KYC within 1-2 business days. We may ask for\n'
               '\tclarifications or additional documents. Approval activates the shop and\n'
               '\tunlocks Listing creation. We may revoke approval if any document is\n'
               '\tlater found to be forged, expired or fraudulently obtained.\n'
               '</p>\n'
               '\n'
               '<h2 id="account">4. Seller account</h2>\n'
               '<p>\n'
               '\tYour Seller account gives you access to the Seller Center\n'
               '\t(<a href="/seller/">/seller/</a>) — dashboard, product management,\n'
               '\torder fulfilment, earnings, reviews, coupons, flash sales, analytics,\n'
               '\tstore promotion.\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>You are responsible for all activity from your account. Keep your password and OTPs '
               'confidential.</li>\n'
               '\t<li>You may not transfer, sell or lease your Seller account to anyone else.</li>\n'
               '\t<li>One natural person or registered entity may operate one Seller account, unless we '
               'explicitly authorise additional accounts (e.g., multi-brand groups).</li>\n'
               '</ul>\n'
               '\n'
               '<h2 id="listings">5. Listing requirements</h2>\n'
               '<p>\n'
               '\tEvery Listing must be accurate, complete and current. You promise that:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Titles describe the product truthfully — no keyword stuffing, no\n'
               '\t\tmisleading brand names.</li>\n'
               '\t<li>Descriptions are written by you (not copied from a competitor) and\n'
               '\t\tmatch the actual product.</li>\n'
               '\t<li>Images are clear, taken or owned by you (or used with the\n'
               "\t\trights-holder's permission), watermark-free, and free of contact\n"
               '\t\tinformation.</li>\n'
               '\t<li>Specifications (size, material, colour, voltage, ingredients) match\n'
               '\t\treality and any regulatory labelling requirement (e.g., BSTI for\n'
               '\t\tconsumer goods).</li>\n'
               '\t<li>The product is in stock at the quantity you set; you update the\n'
               '\t\tstock counter promptly when inventory changes.</li>\n'
               '\t<li>Variants (size, colour) accurately reflect what is available — no\n'
               '\t\tbait-and-switch where the displayed variant is gone but a different\n'
               '\t\tone is shipped.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tFull creative and editorial guidelines live in the\n'
               '\t<a href="/sell/listing-guidelines/">Product Listing Guidelines</a>. SGT\n'
               "\tCart's admin reviews and may reject a Listing that violates them.\n"
               '</p>\n'
               '\n'
               '<h2 id="pricing">6. Pricing autonomy &amp; limits</h2>\n'
               '<p>\n'
               '\tYou set your own prices in BDT. They must be:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li><strong>Inclusive of VAT</strong> at the applicable rate (commonly 5%, 7.5% or 15% '
               'depending on category — NBR Mushok rules).</li>\n'
               '\t<li><strong>Honest</strong> — no inflated "MRP" with a fake "discount" to manipulate '
               'consumers (CRPA §43 forbids deceptive pricing).</li>\n'
               '\t<li><strong>Stable</strong> — material price changes should not happen between order '
               'placement and shipment unless the order is cancelled.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tSGT Cart reserves the right to refuse Listings that show price-gouging\n'
               '\tduring emergencies (e.g., flood, pandemic) or that materially undercut\n'
               '\tthe market in a way suggesting counterfeit goods.\n'
               '</p>\n'
               '\n'
               '<h2 id="inventory">7. Inventory &amp; stock</h2>\n'
               '<p>\n'
               '\tYou must keep your declared stock accurate. Selling an item that is\n'
               '\tout of stock and cancelling the resulting Sub-Order counts as a\n'
               '\tperformance violation (§18).\n'
               '</p>\n'
               '<p>\n'
               '\tIf a Sub-Order is placed but you cannot fulfil it, you must cancel\n'
               '\tit through the Seller Center within <strong>24 hours</strong> and\n'
               '\tcontact the buyer with an explanation. SGT Cart will refund the\n'
               '\tbuyer in full.\n'
               '</p>\n'
               '\n'
               '<h2 id="order-acceptance">8. Order acceptance &amp; fulfilment SLA</h2>\n'
               '<table>\n'
               '\t<tr><th>Step</th><th>SLA</th></tr>\n'
               '\t<tr><td>Acknowledge (mark "Processing")</td><td>Within <strong>24 hours</strong> of order '
               'placement.</td></tr>\n'
               '\t<tr><td>Hand to courier (mark "Shipped")</td><td>Within <strong>72 hours</strong> of '
               'acknowledgement (electronics &amp; clothing); <strong>24 hours</strong> for fast-moving '
               'consumer goods.</td></tr>\n'
               '\t<tr><td>Update tracking number</td><td>Same day as shipment.</td></tr>\n'
               "\t<tr><td>Respond to buyer's chat / Q&amp;A</td><td>Within <strong>24 hours</strong> on "
               'weekdays.</td></tr>\n'
               '</table>\n'
               '<p>\n'
               '\tRepeated breaches of these SLAs trigger the performance ladder in §18.\n'
               '</p>\n'
               '\n'
               '<h2 id="packaging">9. Packaging &amp; branding</h2>\n'
               '<p>\n'
               '\tUse sturdy, tamper-evident packaging suitable to the product. Mark fragile\n'
               '\tor perishable items clearly. The outside of the package must show:\n'
               "\tthe customer's name, address, mobile number, the Order number, your\n"
               '\tSeller name, and a "Sold on SGT Cart" sticker (free SVG provided in\n'
               '\tthe Seller Center).\n'
               '</p>\n'
               '<p>\n'
               '\tYou may include your own shop card, thank-you note or product manual.\n'
               '\tYou may NOT include: leaflets pointing customers to off-platform\n'
               '\tstores, contact details with the intent to bypass SGT Cart on the\n'
               '\tnext purchase, counterfeit branding, or promotional material from a\n'
               '\trival marketplace. Violation triggers an Anti-Disintermediation strike (§16).\n'
               '</p>\n'
               '\n'
               '<h2 id="shipping">10. Shipping responsibilities</h2>\n'
               '<p>\n'
               '\tYou ship the product through a courier of your choice (Pathao, RedX,\n'
               "\tSundarban, Steadfast, etc.) or, when available, through SGT Cart's\n"
               '\tmanaged delivery. You bear the cost of forward shipping and reimburse\n'
               '\treturn-shipping costs for damaged-on-arrival, wrong-item or\n'
               '\tcounterfeit deliveries.\n'
               '</p>\n'
               '<p>\n'
               '\tRisk of loss in transit, until successful delivery, lies with the\n'
               '\tSeller. If a parcel is lost in transit, you refund the buyer and\n'
               '\tpursue recovery with the courier; SGT Cart will support the dispute\n'
               '\tbut does not indemnify the loss.\n'
               '</p>\n'
               '\n'
               '<h2 id="commission">11. Commission &amp; fees</h2>\n'
               '<p>\n'
               '\tSGT Cart charges a commission on every delivered Sub-Order. The\n'
               '\tstandard rate is <strong>10%</strong>, with category-specific\n'
               '\tadjustments listed in the <a href="/sell/fees/">Seller Fees</a> page.\n'
               '\tThe Commission is deducted from the gross order value before the\n'
               '\tnet is credited to your Wallet.\n'
               '</p>\n'
               '<p>\n'
               '\tPayment-processing fees (SSLCommerz card 2.5%, bKash 1.85%) are passed\n'
               '\tthrough at cost. Cash on Delivery has a flat handling fee of Tk 20 per\n'
               '\tSub-Order to cover collection costs.\n'
               '</p>\n'
               '<p>\n'
               '\tOptional services — flash-sale featuring, homepage banner placement,\n'
               '\tsponsored search position, ranking boost — are billed separately at\n'
               '\trates published in the Seller Center.\n'
               '</p>\n'
               '\n'
               '<h2 id="payouts">12. Payout schedule</h2>\n'
               '<p>\n'
               '\tThe earning lifecycle:\n'
               '</p>\n'
               '<ol>\n'
               '\t<li><strong>Pending</strong> — Sub-Order placed → net is held pending delivery.</li>\n'
               '\t<li><strong>Available</strong> — Sub-Order marked delivered → net moves to your available '
               'balance after a 3-day cooling-off window (allows Buyer Protection claims).</li>\n'
               '\t<li><strong>Settled</strong> — you request payout through the Seller Center → admin '
               'reviews → funds released to your nominated bank / bKash / Nagad.</li>\n'
               '</ol>\n'
               '<p>\n'
               '\tPayouts run on a <strong>weekly</strong> cycle (every Sunday). Minimum\n'
               '\twithdrawal Tk 500. SGT Cart reserves the right to hold a payout\n'
               '\tpending investigation of an unusually high refund rate, chargeback\n'
               '\tpattern or open dispute.\n'
               '</p>\n'
               '\n'
               '<h2 id="tax">13. Tax &amp; withholding</h2>\n'
               '<p>\n'
               '\tYou are responsible for filing your own income tax and VAT returns with\n'
               '\tthe NBR. SGT Cart will:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Withhold VAT at source where the NBR Mushok rules require it (currently 5% for '
               'online-marketplace operators).</li>\n'
               '\t<li>Issue you a monthly statement summarising gross sales, commission, withholding and net '
               'payouts.</li>\n'
               '\t<li>Provide an annual statement suitable for filing your income-tax return.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tYou agree to keep your TIN current and to notify us if your tax\n'
               '\tregistration changes.\n'
               '</p>\n'
               '\n'
               '<h2 id="returns-refunds">14. Returns, refunds &amp; chargebacks</h2>\n'
               '<p>\n'
               '\tYou honour SGT Cart\'s <a href="/refund-policy/">Refund Policy</a> and\n'
               '\tthe <a href="/help/buyer-protection/">Buyer Protection Program</a>.\n'
               '\tWhen a refund is granted:\n'
               '</p>\n'
               '<ul>\n'
               "\t<li>The buyer's refund is reversed from the original payment method.</li>\n"
               '\t<li>Your Wallet is debited by the gross amount minus the Commission portion (we waive the '
               'Commission on refunded sales).</li>\n'
               '\t<li>For COD orders, return-shipping cost is your responsibility if the return is due to '
               'seller fault (wrong, damaged, counterfeit); otherwise the buyer pays.</li>\n'
               '</ul>\n'
               '<p>\n'
               "\tChargebacks initiated by the buyer's card issuer follow the same\n"
               '\tlogic, with an additional Tk 200 processing fee passed through to you\n'
               '\tif the chargeback is upheld.\n'
               '</p>\n'
               '\n'
               '<h2 id="complaints">15. Complaint handling</h2>\n'
               '<p>\n'
               '\tWhen a customer raises a complaint:\n'
               '</p>\n'
               '<ol>\n'
               '\t<li>You receive a chat message + in-app notification.</li>\n'
               '\t<li>You must respond within <strong>48 hours</strong>.</li>\n'
               '\t<li>If unresolved within <strong>7 days</strong>, the buyer may escalate to SGT Cart '
               'mediation under <a href="/dispute-resolution/">Dispute Resolution</a>.</li>\n'
               '</ol>\n'
               '\n'
               '<h2 id="disintermediation">16. Anti-disintermediation</h2>\n'
               '<p>\n'
               '\tCustomers acquired on SGT Cart must remain on SGT Cart. You may not:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Share phone numbers, WhatsApp, email or off-platform URLs in chat, reviews, Q&amp;A or '
               'product images.</li>\n'
               '\t<li>Encourage buyers to order future items directly from you outside the Platform.</li>\n'
               '\t<li>Include leaflets, business cards or QR codes in shipments inviting off-platform '
               'purchase.</li>\n'
               '</ul>\n'
               '<p>\n'
               "\tThe Platform's <strong>phone-guard system</strong> automatically redacts\n"
               '\tdigit runs in your messages, reviews and Q&amp;A answers. Each\n'
               '\tredaction is logged. After <strong>2 logged violations</strong> your\n'
               '\tshop is auto-suspended and reviewed by admin. Repeat or wilful\n'
               '\tviolations after warning lead to permanent termination and forfeiture\n'
               '\tof unpaid Wallet balance pending dispute resolution.\n'
               '</p>\n'
               '\n'
               '<h2 id="prohibited">17. Counterfeit, IP &amp; prohibited items</h2>\n'
               '<p>\n'
               '\tYou promise:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Every product is authentic. No counterfeits, no replicas labelled as originals.</li>\n'
               '\t<li>You hold the IP rights to the product / brand or are an authorised reseller.</li>\n'
               '\t<li>You do not list anything on the <a href="/sell/prohibited-items/">Prohibited &amp; '
               'Restricted Items</a> list (firearms, drugs, hazardous chemicals, live animals, currency, '
               'etc.).</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tSGT Cart honours rights-holder takedown notices under the\n'
               '\t<a href="/ip-policy/">IP Policy</a>. A counterfeit confirmed at our\n'
               '\tlevel results in immediate de-listing, refund to the buyer, deduction\n'
               '\tfrom your Wallet, and a strike. Three counterfeit strikes leads to\n'
               '\tpermanent termination.\n'
               '</p>\n'
               '\n'
               '<h2 id="performance">18. Performance standards &amp; suspension</h2>\n'
               '<p>The Seller-performance dashboard tracks (60-day window):</p>\n'
               '<table>\n'
               '\t<tr><th>Metric</th><th>Threshold</th><th>Action</th></tr>\n'
               '\t<tr><td>Late-shipment rate</td><td>&gt; 10%</td><td>Email warning</td></tr>\n'
               '\t<tr><td>Cancellation rate</td><td>&gt; 5%</td><td>Email warning + ranking '
               'penalty</td></tr>\n'
               '\t<tr><td>Order-defect rate (return + dispute + chargeback)</td><td>&gt; '
               '5%</td><td>Suspension review</td></tr>\n'
               '\t<tr><td>Avg seller rating</td><td>&lt; 3.5★ over 50+ reviews</td><td>Auto-suspension '
               'review</td></tr>\n'
               '\t<tr><td>Counterfeit confirmation</td><td>1</td><td>Strike + immediate de-list</td></tr>\n'
               '\t<tr><td>Anti-disintermediation violations</td><td>2</td><td>Auto-suspension</td></tr>\n'
               '</table>\n'
               '<p>\n'
               '\tSuspended sellers may appeal within 14 days to\n'
               '\t<a href="mailto:seller-support@sgtcart.com">seller-support@sgtcart.com</a>.\n'
               '</p>\n'
               '\n'
               '<h2 id="data">19. Data use &amp; confidentiality</h2>\n'
               '<p>\n'
               '\tYou receive customer name, delivery address and mobile number for the\n'
               '\tlimited purpose of fulfilling and supporting an Order. You agree to:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Use the data only for that Order — no marketing, no third-party sharing, no '
               'on-sale.</li>\n'
               '\t<li>Delete it within 90 days of order completion (subject to NBR-mandated invoice '
               'retention).</li>\n'
               '\t<li>Not contact the buyer outside Platform channels (anti-disintermediation §16).</li>\n'
               '\t<li>Treat sales data, ranking signals and SGT Cart internal communications as '
               'confidential.</li>\n'
               '</ul>\n'
               '\n'
               '<h2 id="indemnity">20. Indemnity &amp; liability</h2>\n'
               '<p>\n'
               '\tYou indemnify SGT Cart, its officers, employees, contractors and\n'
               '\taffiliates against all losses, claims, damages, fines, regulatory\n'
               '\tpenalties and reasonable legal fees arising from:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Your breach of this Agreement;</li>\n'
               '\t<li>Your Listings (accuracy, IP, regulatory labelling);</li>\n'
               '\t<li>Your products (quality, safety, fitness, recall);</li>\n'
               '\t<li>Your conduct (complaints, fraud, anti-disintermediation, counterfeit).</li>\n'
               '</ul>\n'
               '<p>\n'
               "\tSGT Cart's aggregate liability to you under this Agreement is capped at\n"
               '\tthe total Commission revenue earned from your shop over the 6 months\n'
               '\tpreceding the event giving rise to the claim.\n'
               '</p>\n'
               '\n'
               '<h2 id="changes">21. Changes &amp; notice period</h2>\n'
               '<p>\n'
               '\tSGT Cart may amend this Agreement. Material changes (fees, payout\n'
               '\tschedule, performance thresholds) take effect <strong>30 days after</strong>\n'
               '\twe email and in-app-notify you. Non-material changes (typo fixes,\n'
               '\tclarifications) may take effect immediately on publication.\n'
               '</p>\n'
               '<p>\n'
               "\tYou may terminate by giving 30 days' written notice to\n"
               '\t<a href="mailto:seller-support@sgtcart.com">seller-support@sgtcart.com</a>.\n'
               '\tPending Sub-Orders must be fulfilled first; Wallet balance is settled\n'
               '\tafter the standard cooling-off window.\n'
               '</p>\n'
               '\n'
               '<h2 id="law">22. Governing law &amp; arbitration</h2>\n'
               '<p>\n'
               '\tThis Agreement is governed by the laws of Bangladesh. Disputes between\n'
               '\tyou and SGT Cart go through:\n'
               '</p>\n'
               '<ol>\n'
               '\t<li>Direct negotiation between the parties (30 days).</li>\n'
               '\t<li>Mediation through the Bangladesh Mediation &amp; Arbitration Centre.</li>\n'
               '\t<li>Final and binding arbitration under the <strong>Arbitration Act 2001 (BD)</strong>, '
               'sole arbitrator, seat in <strong>Dhaka</strong>, English or Bangla language.</li>\n'
               '</ol>\n'
               '<p>\n'
               '\tThe courts of Dhaka have exclusive jurisdiction over any matter not\n'
               '\tcovered by arbitration, including injunctive relief.\n'
               '</p>',
  'toc': [{'anchor': 'defs', 'label': '1. Definitions'},
          {'anchor': 'eligibility', 'label': '2. Eligibility'},
          {'anchor': 'kyc', 'label': '3. KYC & verification'},
          {'anchor': 'account', 'label': '4. Seller account'},
          {'anchor': 'listings', 'label': '5. Listing requirements'},
          {'anchor': 'pricing', 'label': '6. Pricing autonomy & limits'},
          {'anchor': 'inventory', 'label': '7. Inventory & stock'},
          {'anchor': 'order-acceptance', 'label': '8. Order acceptance & SLA'},
          {'anchor': 'packaging', 'label': '9. Packaging & branding'},
          {'anchor': 'shipping', 'label': '10. Shipping responsibilities'},
          {'anchor': 'commission', 'label': '11. Commission & fees'},
          {'anchor': 'payouts', 'label': '12. Payout schedule'},
          {'anchor': 'tax', 'label': '13. Tax & withholding'},
          {'anchor': 'returns-refunds', 'label': '14. Returns, refunds & chargebacks'},
          {'anchor': 'complaints', 'label': '15. Complaint handling'},
          {'anchor': 'disintermediation', 'label': '16. Anti-disintermediation'},
          {'anchor': 'prohibited', 'label': '17. Counterfeit, IP & prohibited items'},
          {'anchor': 'performance', 'label': '18. Performance standards & suspension'},
          {'anchor': 'data', 'label': '19. Data use & confidentiality'},
          {'anchor': 'indemnity', 'label': '20. Indemnity & liability'},
          {'anchor': 'changes', 'label': '21. Changes & notice period'},
          {'anchor': 'law', 'label': '22. Governing law & arbitration'}],
  'faq': [{'q': 'Can a foreigner sell on SGT Cart?',
           'a': 'Not at launch. Sellers must be Bangladesh-resident individuals or BD-registered legal '
                'entities. International sellers will be onboarded in a later phase under a separate '
                'agreement.'},
          {'q': 'How quickly are payouts processed?',
           'a': 'Weekly cycle every Sunday. From delivery confirmation: 3-day Buyer-Protection cooling-off → '
                'request payout → admin review → funds released. Minimum Tk 500.'},
          {'q': 'What happens to my balance if my shop is suspended?',
           'a': 'Available balance is paid out after pending disputes are resolved. If suspension is due to '
                'confirmed counterfeit or fraud, balance may be withheld to fund affected buyer refunds.'},
          {'q': 'Do I really have to ship in 72 hours?',
           'a': 'Yes for electronics and clothing. Some seller-managed categories (custom-made, '
                'made-to-order) have longer SLAs disclosed at Listing creation. Repeated lateness affects '
                'ranking.'},
          {'q': 'Can I sell my own brand on SGT Cart and on my own site at the same time?',
           'a': "Yes. We don't lock you to SGT Cart exclusively. We just require that customers acquired "
                'through SGT Cart stay on SGT Cart for repeat orders (anti-disintermediation, §16).'}],
  'related': [{'href': '/sell/onboarding/',
               'title': 'Seller Onboarding Guide',
               'desc': 'Step-by-step from signup to first sale.'},
              {'href': '/sell/fees/',
               'title': 'Fees & Commission',
               'desc': 'Exact commission rates by category.'},
              {'href': '/sell/listing-guidelines/',
               'title': 'Listing Guidelines',
               'desc': 'What makes a Listing approvable.'},
              {'href': '/sell/anti-disintermediation/',
               'title': 'Anti-Disintermediation',
               'desc': 'The phone-guard rules and 2-strike system.'},
              {'href': '/sell/code-of-conduct/',
               'title': 'Seller Code of Conduct',
               'desc': 'How we expect Sellers to behave on-platform.'},
              {'href': '/sell/prohibited-items/',
               'title': 'Prohibited Items',
               'desc': 'What you must never list.'}]},
 {'slug': 'cookie-policy',
  'title': 'Cookie Policy',
  'subtitle': 'What cookies and similar storage technologies SGT Cart uses, and how to control them.',
  'section': 'Legal',
  'contact_email': 'privacy@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 130,
  'body_html': '<p class="lead small">\n'
               '\tWhen you visit SGT Cart (sgtcart.com) or use one of our mobile apps,\n'
               '\twe and our partners store small pieces of data on your device — called\n'
               '\tcookies, local storage and similar technologies — to keep the site\n'
               '\tworking and to learn how it can be improved. This Cookie Policy lists\n'
               '\twhat we set, why, and how you can switch optional cookies on or off.\n'
               '</p>\n'
               '\n'
               '<h2 id="what">1. What is a cookie?</h2>\n'
               '<p>\n'
               '\tA <strong>cookie</strong> is a tiny text file that a website asks your\n'
               '\tbrowser to save and send back on subsequent visits. It typically\n'
               '\tcontains a session identifier, a preference setting or a consent flag —\n'
               '\tnever your password, never your card number.\n'
               '</p>\n'
               '<p>\n'
               '\tThe Platform also uses related technologies that behave similarly:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li><strong>Local Storage / Session Storage</strong> — key-value pairs your browser keeps '
               'for our pages (e.g., your <code>sgt_voice_lang</code>, <code>sgt_wishlist</code>, '
               '<code>sgt_cookie_consent</code>).</li>\n'
               '\t<li><strong>IndexedDB</strong> — used by the chat module for offline-message '
               'buffering.</li>\n'
               '\t<li><strong>Service Worker cache</strong> — when the mobile app is installed as a PWA, '
               'certain static files are kept locally so the app loads faster.</li>\n'
               '</ul>\n'
               '<p>Throughout this page, "cookie" refers to all of these collectively.</p>\n'
               '\n'
               '<h2 id="why">2. Why we use them</h2>\n'
               '<ul>\n'
               '\t<li><strong>Keep you signed in</strong> — without a session cookie you would have to log '
               'in on every page.</li>\n'
               '\t<li><strong>Remember your cart</strong> — items survive a browser restart.</li>\n'
               '\t<li><strong>Remember preferences</strong> — language (EN / BN), wishlist items, cookie '
               'consent choice, voice-search language, viewed-product history.</li>\n'
               '\t<li><strong>Protect against attacks</strong> — anti-CSRF token, rate-limit fingerprint, '
               'fraud-detection signals.</li>\n'
               '\t<li><strong>Measure performance</strong> — aggregate, first-party-only analytics: how many '
               'people view a product, where pages slow down, which features are used.</li>\n'
               '\t<li><strong>Personalise</strong> — "Recently viewed", "Customers Also Viewed", '
               'recommendations on the home page.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\t<strong>We do not run third-party advertising cookies on SGT Cart.</strong>\n'
               '\tWe do not allow ad networks (Google Ads, Facebook Pixel, TikTok Pixel)\n'
               '\tto track you across other websites. This is a deliberate choice — if it\n'
               '\tever changes, this page will be updated and a fresh consent banner\n'
               '\twill be shown.\n'
               '</p>\n'
               '\n'
               '<h2 id="categories">3. Categories &amp; full list</h2>\n'
               '\n'
               '<h3>3.1 Strictly necessary (always on)</h3>\n'
               '<p>\n'
               '\tThese cookies are essential for the Platform to function. Without them\n'
               '\tyou cannot log in, place an order, or use the cart. They cannot be\n'
               '\tturned off via consent — but you can block them in your browser\n'
               '\tsettings, at the cost of breaking the site.\n'
               '</p>\n'
               '<table>\n'
               '\t<tr><th>Name</th><th>Purpose</th><th>Lifetime</th></tr>\n'
               '\t<tr><td><code>session</code></td><td>Flask session identifier — holds your login '
               'state.</td><td>Browser session</td></tr>\n'
               '\t<tr><td><code>csrf_token</code></td><td>Anti-CSRF token to protect forms from cross-site '
               'request forgery.</td><td>Browser session</td></tr>\n'
               '\t<tr><td><code>remember_token</code></td><td>"Remember me" persistent login. Set only if '
               'you tick the box.</td><td>30 days</td></tr>\n'
               '\t<tr><td><code>sgt_cookie_consent</code> <em>(localStorage)</em></td><td>Records whether '
               'you chose "Accept all" or "Necessary only".</td><td>1 year</td></tr>\n'
               '</table>\n'
               '\n'
               '<h3>3.2 Preferences (always on; non-tracking)</h3>\n'
               '<p>These cookies remember choices you made for a better experience. They are not used for '
               'analytics or marketing.</p>\n'
               '<table>\n'
               '\t<tr><th>Name</th><th>Purpose</th><th>Lifetime</th></tr>\n'
               '\t<tr><td><code>locale</code></td><td>Your language choice (en / bn).</td><td>6 '
               'months</td></tr>\n'
               '\t<tr><td><code>sgt_voice_lang</code> <em>(localStorage)</em></td><td>Voice-search '
               'recognition language (en-US / bn-BD).</td><td>Until cleared</td></tr>\n'
               "\t<tr><td><code>sgt_wishlist</code> <em>(localStorage)</em></td><td>Product IDs you've added "
               'to your wishlist (until DB wishlist ships).</td><td>Until cleared</td></tr>\n'
               '\t<tr><td><code>sgt_doc_lang</code> <em>(localStorage)</em></td><td>Bilingual toggle '
               'preference on legal pages (EN / BN).</td><td>Until cleared</td></tr>\n'
               '\t<tr><td><code>sid</code></td><td>Anonymous viewer ID for the "X viewing now" '
               'badge.</td><td>Browser session</td></tr>\n'
               '</table>\n'
               '\n'
               '<h3>3.3 Analytics (set only after "Accept all")</h3>\n'
               '<p>\n'
               '\tFirst-party analytics help us understand which pages are popular,\n'
               "\twhich load slowly, and where users drop out — so we can fix what's\n"
               '\tbroken. Aggregated, not tied to your identity.\n'
               '</p>\n'
               '<table>\n'
               '\t<tr><th>Name</th><th>Purpose</th><th>Lifetime</th></tr>\n'
               '\t<tr><td><code>sgt_a</code></td><td>Anonymous analytics visitor identifier (random, not '
               'linked to your account).</td><td>2 years</td></tr>\n'
               '\t<tr><td><code>sgt_sess</code></td><td>Per-session bucket for "this visit" '
               'measurement.</td><td>30 minutes</td></tr>\n'
               '</table>\n'
               '<p>\n'
               '\tAnalytics cookies are <strong>off by default</strong>. They are set only\n'
               '\tif you tap "Accept all" on the consent banner. We do not currently use\n'
               '\tGoogle Analytics, Mixpanel, Adobe Analytics or any other third-party\n'
               '\tanalytics vendor — only first-party counters.\n'
               '</p>\n'
               '\n'
               '<h3>3.4 Marketing (none today)</h3>\n'
               '<p>\n'
               '\tWe do not currently set any marketing cookies. If this ever changes,\n'
               '\tthis section will list each cookie and we will trigger a fresh consent\n'
               '\tbanner before activation.\n'
               '</p>\n'
               '\n'
               '<h2 id="consent">4. Your consent</h2>\n'
               '<p>\n'
               '\tThe first time you visit SGT Cart from a new device or after clearing\n'
               '\tbrowser storage, you see a banner at the bottom of the page asking:\n'
               '</p>\n'
               '<blockquote class="small">\n'
               '\t"SGT Cart uses essential cookies to keep you signed in and your cart\n'
               "\tworking. We'd also like to set optional analytics cookies to help us\n"
               '\timprove the site."\n'
               '</blockquote>\n'
               '<p>You have two choices:</p>\n'
               '<ul>\n'
               '\t<li><strong>"Accept all"</strong> — necessary + preferences + analytics. Stored as '
               '<code>sgt_cookie_consent = "all"</code>.</li>\n'
               '\t<li><strong>"Necessary only"</strong> — only the cookies the site cannot work without. '
               'Stored as <code>sgt_cookie_consent = "necessary"</code>.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tThe banner does not re-appear on subsequent pages. To change your\n'
               '\tchoice later, see §5.\n'
               '</p>\n'
               '\n'
               '<h2 id="control">5. How to control cookies</h2>\n'
               '\n'
               '<h3>5.1 On SGT Cart</h3>\n'
               '<p>To revisit your cookie-consent choice on this device:</p>\n'
               '<ol>\n'
               "\t<li>Open your browser's developer tools (F12).</li>\n"
               '\t<li>Go to <strong>Application → Local Storage → https://sgtcart.com</strong>.</li>\n'
               '\t<li>Delete the key <code>sgt_cookie_consent</code>.</li>\n'
               '\t<li>Reload the page — the banner will re-appear.</li>\n'
               '</ol>\n'
               '<p>\n'
               '\tA friendlier user-facing toggle ("Cookie preferences" link in the\n'
               '\tfooter with a dialog) will land in a later release. Until then, the\n'
               '\tabove is the supported method.\n'
               '</p>\n'
               '\n'
               '<h3>5.2 In your browser</h3>\n'
               '<p>All major browsers let you block, view or delete cookies entirely:</p>\n'
               '<ul>\n'
               '\t<li><strong>Chrome:</strong> Settings → Privacy &amp; security → Cookies and other site '
               'data.</li>\n'
               '\t<li><strong>Firefox:</strong> Settings → Privacy &amp; Security → Cookies and Site '
               'Data.</li>\n'
               '\t<li><strong>Safari:</strong> Preferences → Privacy.</li>\n'
               '\t<li><strong>Edge:</strong> Settings → Cookies and site permissions.</li>\n'
               '\t<li><strong>Mobile:</strong> Settings of the respective browser app.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tIf you block all cookies — including strictly necessary ones — most of\n'
               "\tSGT Cart's features (login, cart, checkout, chat) will stop working.\n"
               "\tWe don't recommend this for normal use.\n"
               '</p>\n'
               '\n'
               '<h3>5.3 "Do Not Track" signals</h3>\n'
               '<p>\n'
               '\tModern browsers can send a "Do Not Track" header. Because there is no\n'
               '\tconsensus standard, we currently treat DNT signals as advisory rather\n'
               '\tthan as a blanket opt-out. We do not load any tracking cookies\n'
               '\tregardless of the DNT header — so the practical outcome is the same\n'
               '\tas if we honoured it.\n'
               '</p>\n'
               '\n'
               '<h2 id="changes">6. Changes &amp; contact</h2>\n'
               '<p>\n'
               '\tWhen we add a new cookie or category, we update this page and — if\n'
               '\tthe change is material — show a fresh consent banner. The\n'
               '\t"Last reviewed" date at the bottom of this page always reflects the\n'
               '\tcurrent state.\n'
               '</p>\n'
               '<p>\n'
               '\tFor questions about cookies, write to\n'
               '\t<a href="mailto:privacy@sgtcart.com">privacy@sgtcart.com</a>.\n'
               '</p>',
  'toc': [{'anchor': 'what', 'label': '1. What is a cookie?'},
          {'anchor': 'why', 'label': '2. Why we use them'},
          {'anchor': 'categories', 'label': '3. Categories & full list'},
          {'anchor': 'consent', 'label': '4. Your consent'},
          {'anchor': 'control', 'label': '5. How to control cookies'},
          {'anchor': 'changes', 'label': '6. Changes & contact'}],
  'faq': [{'q': 'Are you really not using Google Analytics?',
           'a': 'Correct — at launch we use only first-party counters (sgt_a, sgt_sess). If we ever add '
                'Google Analytics or similar, this Cookie Policy will be updated and a fresh consent prompt '
                'will be shown.'},
          {'q': "What happens if I click 'Necessary only'?",
           'a': 'Analytics cookies are skipped. Strictly-necessary and preference cookies still work, so '
                'login, cart, and language choice continue to function normally.'},
          {'q': 'Why do I need to consent to preferences cookies?',
           'a': "You don't. Preferences cookies (language, wishlist) are always set so the basic site works "
                "— they don't track you across sessions or share data with anyone."},
          {'q': 'Does the Cookie Policy apply to the mobile app?',
           'a': 'Yes — the SGT Cart mobile apps use equivalent local-storage and shared-preferences '
                'mechanisms that this Cookie Policy describes. The principles are the same.'},
          {'q': 'Can I be tracked by sellers via cookies?',
           'a': 'No. Sellers do not run their own scripts on SGT Cart pages. They see your name, address and '
                'mobile only for fulfilling an Order, not via cookies.'}],
  'related': [{'href': '/privacy/',
               'title': 'Privacy Policy',
               'desc': 'What personal data we collect and how we use it.'},
              {'href': '/terms/', 'title': 'Customer Terms', 'desc': 'The main contract for using SGT Cart.'},
              {'href': '/security/',
               'title': 'Security Practices',
               'desc': 'How we keep your data and session safe.'}]},
 {'slug': 'ip-policy',
  'title': 'Intellectual Property Policy',
  'subtitle': 'How SGT Cart handles trademark, copyright, design and patent infringement on listings and '
              'user content.',
  'section': 'Legal',
  'contact_email': 'ip-takedown@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 140,
  'body_html': '<p class="lead small">\n'
               '\tIntellectual-property rights are the cornerstone of fair commerce.\n'
               '\tThis policy explains how SGT Cart prevents and acts on IP infringement\n'
               '\ton listings created by Sellers, and on user-generated content (reviews,\n'
               '\tQ&amp;A, images) posted on the Platform.\n'
               '</p>\n'
               '\n'
               '<h2 id="our-role">1. Our role &amp; commitments</h2>\n'
               '<p>\n'
               '\tSGT Cart is a marketplace operator, not a publisher of Seller listings.\n'
               '\tSellers create their own product pages, set prices, upload images and\n'
               '\twrite descriptions. Customers post their own reviews and Q&amp;A. We\n'
               '\tdo not pre-approve every word, but we:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Provide a fast notice-and-takedown channel for rights-holders.</li>\n'
               '\t<li>Maintain an Anti-Counterfeit programme and a three-strike repeat-infringer policy '
               '(§6).</li>\n'
               "\t<li>Cooperate with Bangladesh's Department of Patents, Designs and Trademarks (DPDT) and "
               'the Copyright Office on enforcement.</li>\n'
               '\t<li>Honour the spirit of <strong>TRIPS Articles 41-49</strong> on IP enforcement and the '
               'DMCA-equivalent notice-and-counter-notice process.</li>\n'
               '\t<li>Provide rights-holders with a forthcoming Brand Registry (§7) to proactively monitor '
               'counterfeits.</li>\n'
               '</ul>\n'
               '\n'
               '<h2 id="what-infringes">2. What counts as infringement</h2>\n'
               '<p>The IP categories we act on:</p>\n'
               '<table>\n'
               '\t<tr><th>Category</th><th>Examples on the Platform</th></tr>\n'
               "\t<tr><td><strong>Trademark</strong></td><td>Using a brand's word mark or logo on a Listing "
               'for a product not made or authorised by that brand. Selling fake "Apple", "Nike", "Adidas", '
               'etc.</td></tr>\n'
               '\t<tr><td><strong>Copyright</strong></td><td>Uploading product photographs taken by someone '
               "else, copying a description from another retailer's site word-for-word, including "
               'copyrighted music in a product video.</td></tr>\n'
               "\t<tr><td><strong>Industrial design</strong></td><td>Reproducing a registered design's "
               'distinctive shape, surface ornamentation or packaging trade-dress.</td></tr>\n'
               '\t<tr><td><strong>Patent</strong></td><td>Selling a product that implements a patented '
               "invention without the patent-holder's authorisation.</td></tr>\n"
               '\t<tr><td><strong>Passing off</strong></td><td>Style of presentation or get-up that misleads '
               'consumers into thinking the product is from a different (usually well-known) '
               'seller.</td></tr>\n'
               '\t<tr><td><strong>Image / video copyright on UGC</strong></td><td>Reviews containing '
               'screenshots, ad images, or clips lifted from elsewhere.</td></tr>\n'
               '</table>\n'
               '<p>\n'
               '\tGeneric resemblance (e.g., a black running shoe that looks vaguely like\n'
               "\tan Adidas) is not by itself infringement. Use of the brand's word mark\n"
               '\tor logo without authorisation is.\n'
               '</p>\n'
               '\n'
               '<h2 id="takedown">3. Notice-and-takedown procedure</h2>\n'
               '<ol>\n'
               '\t<li><strong>Rights-holder sends a notice</strong> to\n'
               '\t\t<a href="mailto:ip-takedown@sgtcart.com">ip-takedown@sgtcart.com</a>\n'
               '\t\twith the information listed in §4.</li>\n'
               '\t<li><strong>SGT Cart confirms receipt</strong> within 2 business days.</li>\n'
               '\t<li><strong>Initial review</strong> within 5 business days. If the\n'
               '\t\tnotice is complete and the claim is prima facie valid, we\n'
               '\t\t<strong>de-list the affected URL</strong> from search and the\n'
               '\t\tcategory page, mark the Listing "Under review", and prevent new\n'
               '\t\torders.</li>\n'
               '\t<li><strong>Seller notification</strong> goes out with a copy of the\n'
               '\t\t(redacted) notice and a 10-day window to file a counter-notice (§5).</li>\n'
               '\t<li><strong>Decision</strong> — either reinstate the Listing (if a\n'
               "\t\tvalid counter-notice is filed and the rights-holder doesn't escalate\n"
               '\t\tto court), keep it down, or permanently remove it after a confirmed\n'
               '\t\tstrike (§6).</li>\n'
               '</ol>\n'
               '<p>\n'
               '\tFor obvious cases (counterfeit branding, identical copy of well-known\n'
               '\ttrademark) we may remove the Listing immediately on notice, pending\n'
               '\tthe rest of the review. The Seller is still entitled to a\n'
               '\tcounter-notice.\n'
               '</p>\n'
               '\n'
               '<h2 id="notice-content">4. What a takedown notice must contain</h2>\n'
               '<p>A valid notice must include all of the following:</p>\n'
               '<ol>\n'
               '\t<li>Your full name, organisation (if any), email and phone.</li>\n'
               '\t<li>The IP right you are asserting — trademark / copyright / design /\n'
               '\t\tpatent — with registration number, jurisdiction and a copy of the\n'
               '\t\tregistration certificate (or proof of ownership for unregistered\n'
               '\t\tcopyright).</li>\n'
               '\t<li>The exact SGT Cart URL(s) of the infringing Listing(s) and a\n'
               '\t\tscreenshot of the offending content.</li>\n'
               '\t<li>A statement that you have a good-faith belief the use is not\n'
               '\t\tauthorised by you, your agent or the law.</li>\n'
               '\t<li>A statement, under penalty of perjury, that the information in\n'
               '\t\tyour notice is accurate.</li>\n'
               '\t<li>Your physical or electronic signature.</li>\n'
               '</ol>\n'
               '<p>\n'
               '\tSubmissions that are incomplete will be returned with a request for\n'
               '\tthe missing information. False or bad-faith notices may be referred\n'
               '\tto law enforcement.\n'
               '</p>\n'
               '\n'
               '<h2 id="counter-notice">5. Counter-notice by the seller</h2>\n'
               '<p>\n'
               '\tIf you are a Seller whose Listing was taken down, you may submit a\n'
               '\tcounter-notice to <a href="mailto:ip-takedown@sgtcart.com">ip-takedown@sgtcart.com</a>\n'
               '\twithin 10 business days. The counter-notice must contain:\n'
               '</p>\n'
               '<ol>\n'
               '\t<li>Your full name, address, email, phone, and TIN.</li>\n'
               '\t<li>The URL(s) of the Listing(s) that were taken down.</li>\n'
               '\t<li>A statement, under penalty of perjury, that you have a good-faith\n'
               '\t\tbelief the Listing was taken down by mistake or misidentification\n'
               '\t\t— and the basis (you are the rights-holder, an authorised reseller,\n'
               '\t\tthe content is in the public domain, the use is fair use under\n'
               '\t\tBangladesh copyright law, etc.).</li>\n'
               '\t<li>Documentary evidence — distribution agreement, invoice from the\n'
               '\t\tbrand, licence, or proof that the IP claim is invalid.</li>\n'
               '\t<li>Consent to the jurisdiction of the courts of Dhaka.</li>\n'
               '\t<li>Your physical or electronic signature.</li>\n'
               '</ol>\n'
               '<p>\n'
               '\tIf the counter-notice is accepted, the Listing is restored within 10\n'
               '\tbusiness days unless the rights-holder confirms in writing that they\n'
               '\thave begun a court action against you.\n'
               '</p>\n'
               '\n'
               '<h2 id="repeat">6. Repeat-infringer policy</h2>\n'
               '<p>\n'
               '\tSellers who accumulate strikes (one strike = one confirmed IP-takedown\n'
               '\twithout successful counter-notice) face escalating consequences:\n'
               '</p>\n'
               '<table>\n'
               '\t<tr><th>Strike</th><th>Consequence</th></tr>\n'
               '\t<tr><td>1st</td><td>Listing removed, written warning, mandatory IP-policy refresher in '
               'Seller Center.</td></tr>\n'
               '\t<tr><td>2nd</td><td>Listing removed + sponsored / flash-sale promotional access suspended '
               'for 90 days.</td></tr>\n'
               '\t<tr><td>3rd</td><td>Seller account terminated. Wallet balance withheld pending settlement '
               'of any open buyer claims; remainder released to the seller.</td></tr>\n'
               '</table>\n'
               '<p>\n'
               '\tConfirmed counterfeit goods (different from generic IP infringement)\n'
               '\tfollow an accelerated path — see §8.\n'
               '</p>\n'
               '\n'
               '<h2 id="brand-registry">7. Brand Registry (coming in a later phase)</h2>\n'
               '<p>\n'
               '\tWe are designing a Brand Registry for rights-holders to:\n'
               '</p>\n'
               '<ul>\n'
               '\t<li>Submit a brand profile (logos, registered marks, common product variants).</li>\n'
               '\t<li>Receive automatic alerts on new Listings matching brand keywords or logos (image '
               'similarity).</li>\n'
               '\t<li>Use a fast-track takedown form pre-filled with their registration details.</li>\n'
               '\t<li>Designate authorised resellers who can list freely under the brand.</li>\n'
               '</ul>\n'
               '<p>\n'
               '\tRights-holders interested in early-access registration may email\n'
               '\t<a href="mailto:ip-takedown@sgtcart.com">ip-takedown@sgtcart.com</a>.\n'
               '</p>\n'
               '\n'
               '<h2 id="counterfeit">8. Counterfeit reporting</h2>\n'
               '<p>\n'
               '\tCounterfeits are products falsely bearing the trademark or trade-dress\n'
               '\tof an established brand. We treat them as a serious safety and consumer-\n'
               '\tdeception risk (often substandard materials, no warranty, no recall\n'
               '\tchannel).\n'
               '</p>\n'
               '<p>\n'
               '\tCustomers can report a suspected counterfeit through\n'
               '\t<a href="/help/counterfeit/">Report Counterfeit</a> or directly to\n'
               '\t<a href="mailto:ip-takedown@sgtcart.com">ip-takedown@sgtcart.com</a>.\n'
               '\tRights-holders can use the same channel.\n'
               '</p>\n'
               '<p>\n'
               '\tWhen confirmed: the Listing is removed, all orders of that SKU are\n'
               "\trefunded in full (no return required), the Seller's Wallet is debited\n"
               '\tfor the refunds, and a counterfeit strike is applied. <strong>Three\n'
               '\tcounterfeit strikes results in permanent termination.</strong>\n'
               '</p>\n'
               '\n'
               '<h2 id="contact-ip">9. Contact &amp; legal address</h2>\n'
               '<ul>\n'
               '\t<li><strong>IP Takedown desk:</strong> <a '
               'href="mailto:ip-takedown@sgtcart.com">ip-takedown@sgtcart.com</a></li>\n'
               '\t<li><strong>Postal:</strong> Smart Global Trade Cart — IP Desk, Mirpur, Dhaka 1216, '
               'Bangladesh</li>\n'
               '\t<li><strong>Acknowledgement SLA:</strong> 2 business days · <strong>Decision SLA:</strong> '
               '5 business days for clear cases, 15 days for complex.</li>\n'
               '</ul>',
  'toc': [{'anchor': 'our-role', 'label': '1. Our role & commitments'},
          {'anchor': 'what-infringes', 'label': '2. What counts as infringement'},
          {'anchor': 'takedown', 'label': '3. Notice-and-takedown procedure'},
          {'anchor': 'notice-content', 'label': '4. What a takedown notice must contain'},
          {'anchor': 'counter-notice', 'label': '5. Counter-notice by the seller'},
          {'anchor': 'repeat', 'label': '6. Repeat-infringer policy'},
          {'anchor': 'brand-registry', 'label': '7. Brand Registry (coming)'},
          {'anchor': 'counterfeit', 'label': '8. Counterfeit reporting'},
          {'anchor': 'contact-ip', 'label': '9. Contact & legal address'}],
  'faq': [{'q': "I'm a brand owner — do I need to register before reporting?",
           'a': 'No. You can file a takedown notice anytime via ip-takedown@sgtcart.com. Brand Registry (§7) '
                'is optional and will streamline future reports when it launches.'},
          {'q': 'Will my notice be shared with the seller?',
           'a': 'Yes — a redacted version (your address removed) is shared so the seller can file a '
                'counter-notice if they have rights. This is standard practice and required for a fair '
                'takedown process.'},
          {'q': "What if a customer review uses a competitor's brand name?",
           'a': 'Mentioning a brand in a review is fair comparison and not infringement by itself. Posting '
                'their logo, copyrighted images or trade-dress is. The same standards apply to UGC as to '
                'listings.'},
          {'q': 'Are parallel imports allowed?',
           'a': 'Yes — if a Seller legitimately imports authentic branded goods and resells in Bangladesh, '
                "that's not counterfeit. We will not act on a notice unless we see evidence the goods are "
                'fake or the seller is not authorised.'},
          {'q': 'How long does the whole process take?',
           'a': 'Most clear cases (obvious counterfeit, identical mark) are resolved within 7-10 days. '
                'Complex IP claims (e.g., design-trade-dress similarity) can take up to 30 days while we '
                'evaluate evidence from both sides.'}],
  'related': [{'href': '/anti-counterfeit/',
               'title': 'Anti-Counterfeit Policy',
               'desc': 'How we prevent fake goods at the catalogue level.'},
              {'href': '/seller-terms/',
               'title': 'Seller Agreement',
               'desc': "Sellers' contractual obligations on IP and authenticity."},
              {'href': '/help/counterfeit/',
               'title': 'Report Counterfeit',
               'desc': 'Customer-facing report form for fake products.'}]},
 {'slug': 'returns',
  'title': 'Returns & Refunds',
  'subtitle': "How to return a product on SGT Cart, what's eligible, and how long the refund takes.",
  'section': 'Customer Help',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 200,
  'body_html': '<p class="lead small">\n'
               "\t\tWe want every order on SGT Cart to delight you. When it doesn't, this\n"
               '\t\tpage tells you exactly how to send the item back and get your money or\n'
               '\t\ta replacement. Returns are powered by the\n'
               '\t\t<a href="/terms/">Customer Terms</a> and the statutory rights in the\n'
               '\t\t<strong>Consumer Rights Protection Act 2009</strong>.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="window">1. Return window</h2>\n'
               '\t<p>\n'
               '\t\tYou have <strong>7 days from the delivery date</strong> to start a\n'
               '\t\treturn for most items. The clock starts the moment the courier marks\n'
               '\t\tthe Sub-Order as "delivered" — this date is shown in\n'
               '\t\t<a href="/my-orders/">My Orders</a>.\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tSome categories have <strong>longer windows</strong>, set by the\n'
               '\t\tSeller and shown on the product page:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>Electronics &amp; appliances — up to <strong>15 days</strong> if marked "Extended '
               'Returns".</li>\n'
               '\t\t<li>Watches &amp; jewellery — up to <strong>10 days</strong>.</li>\n'
               '\t\t<li>SGT-Cart-managed inventory ("Sold by SGT Cart") — up to <strong>14 '
               'days</strong>.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tDamaged-on-arrival, wrong-item or counterfeit issues have a\n'
               '\t\t<strong>60-day Buyer Protection window</strong> regardless of category — see §6.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="eligible">2. Eligible vs. non-eligible items</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Generally eligible</th><th>Generally non-eligible</th></tr>\n'
               '\t\t<tr><td>Clothing, shoes, accessories</td><td>Innerwear, swimwear, socks '
               '(hygiene)</td></tr>\n'
               '\t\t<tr><td>Electronics in original packaging</td><td>Pre-paid mobile recharge, digital '
               'codes</td></tr>\n'
               '\t\t<tr><td>Home &amp; kitchen items unused</td><td>Perishables — food, fresh produce, '
               'flowers</td></tr>\n'
               '\t\t<tr><td>Books, stationery</td><td>Custom-made / personalised orders</td></tr>\n'
               '\t\t<tr><td>Toys (original sealed)</td><td>Cosmetics &amp; skincare once seal '
               'broken</td></tr>\n'
               '\t\t<tr><td>Watches, jewellery (with tag)</td><td>Software activated with a license '
               'key</td></tr>\n'
               '\t\t<tr><td>Sports goods unused</td><td>Pet food &amp; medicines</td></tr>\n'
               '\t</table>\n'
               '\t<p>\n'
               '\t\tEvery product page shows its category-specific return rule. If it\n'
               '\t\tsays <em>"Non-returnable for hygiene"</em>, the only path is the\n'
               '\t\tdamaged / wrong / counterfeit flow in §6.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="condition">3. Condition of returned items</h2>\n'
               '\t<p>To be accepted, the returned item must be:</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Unused / unworn</strong> — except for the kind of brief inspection a buyer '
               'in a physical shop would do.</li>\n'
               '\t\t<li><strong>In original packaging</strong> with all accessories (chargers, cables, '
               'manuals, free gifts), warranty card, and price tag.</li>\n'
               "\t\t<li><strong>Securely repacked</strong> in the outer carton SGT Cart's pickup partner "
               'provides.</li>\n'
               '\t\t<li><strong>With proof of purchase</strong> — SGT Cart invoice or order number written '
               'on the packaging slip.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tIf an item arrives back damaged because it was poorly repacked or\n'
               '\t\tmisused, the Seller may refuse the return and only offer a partial\n'
               '\t\trefund. The full criteria are in <a href="/refund-policy/">Refund Policy</a>.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="process">4. How to start a return</h2>\n'
               '\t<ol>\n'
               '\t\t<li>Open <a href="/my-orders/">My Orders</a> and locate the Sub-Order.</li>\n'
               '\t\t<li>Tap <strong>"Return / Refund"</strong> next to the item.</li>\n'
               "\t\t<li>Choose a reason from the list (didn't fit, changed mind, wrong colour, defective, "
               'etc.).</li>\n'
               '\t\t<li>Upload up to 4 photos and a short video if useful — this speeds up approval.</li>\n'
               '\t\t<li>Choose your refund method (see §5).</li>\n'
               "\t\t<li>Pick a pickup time slot. We'll arrange a courier to collect the parcel from your "
               'address.</li>\n'
               "\t\t<li>Hand the courier the repacked item along with the invoice slip. You'll get an in-app "
               'tracking ID.</li>\n'
               '\t\t<li>Once the Seller (or SGT QC) confirms receipt and the condition check, the refund is '
               'processed.</li>\n'
               '\t</ol>\n'
               '\t<p>\n'
               '\t\tNo printer at home? No worries — the courier brings a pre-printed\n'
               '\t\treturn label.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="refund-methods">5. Refund methods &amp; timelines</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>You paid by</th><th>Refund goes to</th><th>Timeline after receipt</th></tr>\n'
               '\t\t<tr><td>Cash on Delivery</td><td>Your bKash or Nagad (your choice)</td><td>2-3 business '
               'days</td></tr>\n'
               '\t\t<tr><td>bKash / Nagad</td><td>Same wallet</td><td>2-3 business days</td></tr>\n'
               '\t\t<tr><td>Card (Visa / MasterCard / AMEX)</td><td>Same card</td><td>7-10 business days '
               '(issuer-dependent)</td></tr>\n'
               '\t\t<tr><td>SGT Cart Wallet credit</td><td>Wallet</td><td>Instant</td></tr>\n'
               '\t\t<tr><td>Reward Points used in the order</td><td>Reverted to your Points '
               'balance</td><td>Instant</td></tr>\n'
               '\t</table>\n'
               '\t<p>\n'
               '\t\tYou can also choose <strong>"Wallet credit"</strong> for any refund —\n'
               '\t\tinstant, usable on your next Order, and never expires. The original\n'
               '\t\tmethod always remains available; Wallet credit is opt-in.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="damaged">6. Damaged, wrong or counterfeit items</h2>\n'
               '\t<p>\n'
               '\t\tIf the item arrives broken, looks different from what you ordered, or\n'
               '\t\tyou suspect it is a counterfeit, you have <strong>60 days</strong> to\n'
               '\t\treport it through the same Return flow. Mark the reason as\n'
               '\t\t<em>"Damaged on arrival"</em>, <em>"Wrong item"</em>, or\n'
               '\t\t<em>"Suspect counterfeit"</em>.\n'
               '\t</p>\n'
               '\t<p>In these cases:</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>You pay nothing for return shipping</strong> — covered by the Seller.</li>\n'
               "\t\t<li>Some damaged categories (large home appliances, fragile glass items) don't even "
               'require a return — a clear unboxing photo / video is enough.</li>\n'
               '\t\t<li>You may choose <strong>full refund</strong> or <strong>free '
               'replacement</strong>.</li>\n'
               '\t\t<li>A confirmed counterfeit triggers an investigation and a strike against the Seller '
               'under our <a href="/anti-counterfeit/">Anti-Counterfeit Policy</a>.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="seller-refusal">7. If the seller refuses or doesn\'t respond</h2>\n'
               '\t<p>\n'
               '\t\tIf the Seller does not approve your return within <strong>48 hours</strong>,\n'
               '\t\tthe system automatically escalates the case to the\n'
               '\t\t<strong>SGT mediation</strong> step (Buyer Protection §3 mediator). You\n'
               "\t\tdon't have to do anything — the case enters mediation with the\n"
               '\t\tevidence you already provided.\n'
               '\t</p>\n'
               '\t<p>\n'
               "\t\tIf you disagree with mediation's outcome, you can escalate further\n"
               '\t\tvia our <a href="/dispute-resolution/">Dispute Resolution</a> ladder\n'
               '\t\tall the way to CRPA §76 / arbitration.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="exchanges">8. Exchanges</h2>\n'
               '\t<p>\n'
               '\t\tExchanges (different size / colour of the same item) are handled as a\n'
               '\t\tstandard return followed by a new Order — that way both legs are\n'
               '\t\ttracked, refunded and shipped cleanly. Many Sellers offer a\n'
               '\t\t"Replacement" path on the same return form which combines the two\n'
               '\t\tinto a single ticket — look for the option next to the reason\n'
               '\t\tdropdown.\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tIf the new variant has a different price, you pay or receive the\n'
               '\t\tdifference at the time the replacement ships.\n'
               '\t</p>',
  'toc': [{'anchor': 'window', 'label': '1. Return window'},
          {'anchor': 'eligible', 'label': '2. Eligible vs. non-eligible items'},
          {'anchor': 'condition', 'label': '3. Condition of returned items'},
          {'anchor': 'process', 'label': '4. How to start a return'},
          {'anchor': 'refund-methods', 'label': '5. Refund methods & timelines'},
          {'anchor': 'damaged', 'label': '6. Damaged, wrong or counterfeit items'},
          {'anchor': 'seller-refusal', 'label': '7. If the seller refuses'},
          {'anchor': 'exchanges', 'label': '8. Exchanges'}],
  'faq': [{'q': 'Can I return an item just because I changed my mind?',
           'a': "Yes — within the 7-day window, for any change-of-mind reason, on items that aren't on the "
                'non-eligible list. The product must be unused and in original packaging.'},
          {'q': 'Does SGT Cart charge a restocking fee?',
           'a': 'No, never. The amount you paid (minus any deduction for missing items or damage you caused) '
                'is refunded in full.'},
          {'q': 'Who pays for return shipping?',
           'a': "If the return is buyer's choice (changed mind, didn't fit) you pay return shipping, "
                'typically Tk 60-150 depending on weight and district. If the item was damaged / wrong / '
                'counterfeit, the seller pays.'},
          {'q': "My order is still 'Pending' or 'Shipped' — can I cancel instead of return?",
           'a': 'Yes. See the Cancellation Policy at /help/cancellations/. Cancellation is faster and free.'},
          {'q': 'What about COD orders — can I get the refund in cash?',
           'a': 'We do not refund cash door-to-door (logistically unsafe). For COD orders the refund goes to '
                'your bKash or Nagad, instantly available. The mobile-wallet number is the one you confirmed '
                'at refund-method step.'}],
  'related': [{'href': '/refund-policy/',
               'title': 'Refund Policy',
               'desc': 'Detailed timelines and rules for each payment method.'},
              {'href': '/help/cancellations/',
               'title': 'Cancellations',
               'desc': 'Cancel before delivery — free and fast.'},
              {'href': '/help/buyer-protection/',
               'title': 'Buyer Protection',
               'desc': "What's covered if a seller doesn't cooperate."},
              {'href': '/help/damaged-item/',
               'title': 'Damaged Item Flow',
               'desc': 'Specific steps for damaged-on-arrival cases.'}]},
 {'slug': 'shipping',
  'title': 'Shipping & Delivery',
  'subtitle': 'How SGT Cart delivers, in how many days, at what cost — district by district.',
  'section': 'Customer Help',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 210,
  'body_html': '<p class="lead small">\n'
               '\t\tSGT Cart delivers across all 64 districts of Bangladesh through a\n'
               '\t\tmulti-courier network. This page lists where we deliver, how long it\n'
               '\t\ttakes, how shipping is priced, and what happens when something goes\n'
               '\t\twrong on the road.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="coverage">1. Where we deliver</h2>\n'
               '\t<p>\n'
               '\t\t<strong>Bangladesh — all 64 districts.</strong> Same-city delivery available in\n'
               '\t\tDhaka, Chittagong, Sylhet, Rajshahi, Khulna, Barishal, Mymensingh and\n'
               '\t\tRangpur metros. Upazila and Union-level addresses are served via\n'
               '\t\tregional hubs.\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tSome addresses are flagged "<em>Out of service area</em>" at checkout —\n'
               '\t\ttypically remote hill tracts, char lands and unmapped Union-level\n'
               '\t\taddresses. If you see this message, please add a nearby pickup point\n'
               '\t\t(post office, bazaar shop) in the address book.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="eta">2. Estimated delivery times</h2>\n'
               '\t<p>\n'
               '\t\tThe exact ETA shown on the product page is computed at the moment of\n'
               '\t\tdisplay, using:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>Your saved primary address (district) — anonymous users see Dhaka by default until '
               'they set a location.</li>\n'
               "\t\t<li>The Seller's historical <strong>average delivery time</strong>.</li>\n"
               "\t\t<li>The product's category (electronics often need warehouse inspection; clothing ships "
               'faster).</li>\n'
               '\t\t<li>Public holidays and known weather disruptions (Eid, monsoon, transport '
               'strikes).</li>\n'
               '\t</ul>\n'
               '\t<table>\n'
               '\t\t<tr><th>Destination</th><th>Typical ETA</th></tr>\n'
               '\t\t<tr><td>Dhaka (same city)</td><td>1-2 days</td></tr>\n'
               '\t\t<tr><td>Chittagong, Sylhet, Khulna metros</td><td>2-3 days</td></tr>\n'
               '\t\t<tr><td>Other district HQs</td><td>3-5 days</td></tr>\n'
               '\t\t<tr><td>Upazila / Union addresses</td><td>4-7 days</td></tr>\n'
               '\t\t<tr><td>Hill tracts &amp; remote islands</td><td>5-10 days</td></tr>\n'
               '\t</table>\n'
               '\t<p>\n'
               '\t\tThe product page shows a date range like <em>"Delivery: 26 May - 1 Jun"</em>.\n'
               '\t\tIf you do not receive the item within <strong>5 grace days after the\n'
               '\t\tupper bound</strong>, you may file a Buyer Protection claim.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="fees">3. Shipping fees</h2>\n'
               '\t<p>\n'
               '\t\tShipping is charged <strong>per Seller</strong> — if your Order has items\n'
               "\t\tfrom three different Sellers, you'll see three line items. Fees are\n"
               '\t\tconfigurable per-vendor; the platform default is Tk 60 per Sub-Order.\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Free shipping threshold</strong> — Sub-Order subtotal above\n'
               '\t\t\tTk 1,000 (default; admin-tunable) qualifies for free shipping from\n'
               '\t\t\tthat Seller.</li>\n'
               '\t\t<li><strong>Heavy / bulky items</strong> — Sellers may set a higher\n'
               '\t\t\tshipping rate for products above 5 kg or with awkward dimensions.\n'
               '\t\t\tThe rate is shown on the product page.</li>\n'
               '\t\t<li><strong>Same-city seller</strong> — products from a Seller in your\n'
               '\t\t\tbuyer city often have lower or zero shipping if the Seller offers it.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tThe exact fees for your address appear on the cart and checkout pages\n'
               '\t\tbefore payment. There are <strong>no hidden surcharges</strong> on\n'
               '\t\tdelivery — what you see at checkout is what you pay.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="partners">4. Delivery partners</h2>\n'
               '\t<p>\n'
               "\t\tWe don't operate our own fleet. Sellers choose from approved couriers:\n"
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Pathao Courier</strong> — strongest in Dhaka and Chittagong metros, '
               'including same-day on selected categories.</li>\n'
               '\t\t<li><strong>RedX</strong> — broad nationwide reach including upazila level.</li>\n'
               '\t\t<li><strong>Sundarban Courier Service</strong> — strong rural penetration.</li>\n'
               '\t\t<li><strong>Steadfast</strong> — competitive multi-district rate.</li>\n'
               '\t\t<li><strong>SA Paribahan</strong> — for bulky / heavy shipments.</li>\n'
               '\t\t<li><strong>Seller-managed local delivery</strong> — for same-city orders, some Sellers '
               'deliver via their own riders.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tThe courier name and tracking link appear on the Sub-Order page once\n'
               '\t\tthe Seller marks it Shipped.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="tracking">5. Tracking your parcel</h2>\n'
               '\t<ol>\n'
               '\t\t<li>Open <a href="/my-orders/">My Orders</a>.</li>\n'
               '\t\t<li>Tap the Sub-Order to expand it.</li>\n'
               '\t\t<li>Find the <strong>"Track parcel"</strong> link with the courier name and tracking '
               'ID.</li>\n'
               "\t\t<li>Click through to the courier's portal for the latest scan event, or stay on SGT Cart "
               'to see the integrated status timeline.</li>\n'
               '\t</ol>\n'
               '\t<p>\n'
               "\t\tYou'll also receive in-app and email notifications at each status\n"
               '\t\tchange — placed → processing → shipped → out for delivery → delivered.\n'
               '\t\tPush-notification preferences live in <a href="/profile-info/">Account</a>.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="failed">6. Failed delivery &amp; reattempts</h2>\n'
               "\t<p>If the courier can't deliver on the first attempt:</p>\n"
               '\t<ul>\n'
               '\t\t<li>They call the mobile number on file. Keep it available.</li>\n'
               '\t\t<li>You can ask for a same-day re-attempt at a different time, or schedule the next '
               'available day.</li>\n'
               '\t\t<li>Up to <strong>2 reattempts</strong> are made.</li>\n'
               '\t\t<li>After the 2nd failure, the parcel is returned to the Seller. The Sub-Order is '
               'cancelled and refunded per the <a href="/refund-policy/">Refund Policy</a>.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tFor COD Orders, repeated failed reattempts may incur a Tk 100 wasted-delivery\n'
               '\t\tfee deducted from any future refund or wallet credit — only if the\n'
               "\t\tfailure was clearly the buyer's fault (e.g., refused without reason,\n"
               '\t\tunreachable on every call).\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="international">7. International shipping</h2>\n'
               '\t<p>\n'
               '\t\tAt launch, SGT Cart ships <strong>within Bangladesh only</strong>.\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tInternational shipping will open in a later phase, with a separate\n'
               '\t\tcross-border addendum to these terms covering customs duties, import\n'
               "\t\tdeclarations, restricted-item lists, and currency conversion. We'll\n"
               '\t\tpublish a dedicated <em>International Shipping</em> page when that\n'
               '\t\tphase ships. Until then, international users may register and browse\n'
               '\t\tbut Orders cannot be placed for delivery outside Bangladesh.\n'
               '\t</p>',
  'toc': [{'anchor': 'coverage', 'label': '1. Where we deliver'},
          {'anchor': 'eta', 'label': '2. Estimated delivery times'},
          {'anchor': 'fees', 'label': '3. Shipping fees'},
          {'anchor': 'partners', 'label': '4. Delivery partners'},
          {'anchor': 'tracking', 'label': '5. Tracking your parcel'},
          {'anchor': 'failed', 'label': '6. Failed delivery & reattempts'},
          {'anchor': 'international', 'label': '7. International shipping'}],
  'faq': [{'q': 'Can I change my delivery address after placing an order?',
           'a': "Only before the Sub-Order is marked Shipped. Open the Order and tap 'Change address'. After "
                "shipping, the parcel is already with the courier and the address can't be updated — but you "
                "can usually still redirect at the courier's portal if their service supports it."},
          {'q': "My delivery is late — what's my recourse?",
           'a': "If you're past the upper ETA + 5 grace days, file a Buyer Protection claim. Earlier than "
                'that, the right step is to ping the Seller in chat or call the courier with the tracking '
                'ID.'},
          {'q': 'Do you deliver on Friday / Saturday?',
           'a': 'Most couriers operate Saturday-Thursday with Friday off. SGT Demo Store and a few Sellers '
                "explicitly offer Friday delivery within Dhaka — look for the 'Friday delivery' badge on the "
                'product page.'},
          {'q': 'Why are shipping fees higher in remote districts?',
           'a': 'Couriers charge by weight × distance × hub-handling. Remote districts add an extra hop '
                'through a regional hub, which adds to the rate. Free-shipping thresholds still apply — buy '
                'enough from one Seller and ship for Tk 0.'},
          {'q': 'Will the courier hand over the parcel to a neighbour?',
           'a': 'Standard practice is to deliver to you or someone at the address. If you authorise it via '
                "the courier's app, they can hand over to a neighbour or building security — but SGT Cart's "
                'risk-of-loss transfer point is the address, not a specific person, so we recommend only '
                'authorising trusted parties.'}],
  'related': [{'href': '/help/payment-methods/',
               'title': 'Payment Methods',
               'desc': 'How to pay — COD, wallet, card.'},
              {'href': '/help/order-tracking/',
               'title': 'Tracking Your Order',
               'desc': 'Where to find the live courier status.'},
              {'href': '/returns/', 'title': 'Returns', 'desc': 'Sending an item back after delivery.'},
              {'href': '/help/buyer-protection/',
               'title': 'Buyer Protection',
               'desc': 'Late or never-delivered orders.'}]},
 {'slug': 'refund-policy',
  'title': 'Refund Policy',
  'subtitle': 'Exact rules, timelines and amounts for every kind of refund on SGT Cart.',
  'section': 'Trust & Safety',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 220,
  'body_html': '<p class="lead small">\n'
               '\t\tThis Refund Policy explains exactly when SGT Cart issues a refund, how\n'
               "\t\tit's calculated, where the money goes, and how long it takes. It\n"
               '\t\tsupplements the <a href="/returns/">Returns</a> page (which deals\n'
               '\t\twith the physical act of sending items back) and the\n'
               '\t\t<a href="/help/buyer-protection/">Buyer Protection Program</a> (which\n'
               "\t\tcovers what happens if a Seller doesn't cooperate).\n"
               '\t</p>\n'
               '\n'
               '\t<h2 id="scope">1. Scope &amp; legal basis</h2>\n'
               '\t<p>\n'
               '\t\tThis policy applies to every Order placed on sgtcart.com or any SGT\n'
               '\t\tCart mobile app, paid in any supported method. It is shaped by:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>The <strong>Consumer Rights Protection Act 2009</strong> (BD) — especially §38 '
               '(right against deceptive supply), §41 (against defective goods) and §44 (against false '
               'price-marking).</li>\n'
               '\t\t<li>The <strong>Digital Commerce Operation Guidelines 2021</strong> (DCOG) — escrow / '
               'payment-handling expectations.</li>\n'
               '\t\t<li>Our <a href="/terms/">Customer Terms</a> and the\n'
               '\t\t\t<a href="/seller-terms/">Seller Agreement</a>.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="when">2. When you qualify for a refund</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Scenario</th><th>Refund eligibility</th></tr>\n'
               '\t\t<tr><td>You cancel before the Sub-Order is shipped</td><td>Full refund.</td></tr>\n'
               "\t\t<tr><td>Seller cancels (out of stock, can't fulfil)</td><td>Full refund + Tk 50 "
               'inconvenience credit if cancelled after 24h.</td></tr>\n'
               '\t\t<tr><td>Item not delivered within max ETA + 5 days</td><td>Full refund on '
               'request.</td></tr>\n'
               '\t\t<tr><td>Item arrives damaged / wrong / counterfeit</td><td>Full refund OR free '
               'replacement.</td></tr>\n'
               '\t\t<tr><td>Item materially different from Listing (size, colour, missing '
               'accessories)</td><td>Full refund OR partial refund (you keep it) OR replacement.</td></tr>\n'
               '\t\t<tr><td>You change your mind (return within 7 days)</td><td>Refund of item price; you '
               'pay return shipping.</td></tr>\n'
               '\t\t<tr><td>Failed prepaid payment, no Order placed</td><td>Authorisation reversed '
               'automatically within 5-7 days.</td></tr>\n'
               '\t\t<tr><td>Reward points / coupon misapplied</td><td>Reverted to your account.</td></tr>\n'
               '\t</table>\n'
               '\n'
               '\t<h2 id="methods">3. Refund methods by payment type</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>You paid by</th><th>Refund route</th><th>Notes</th></tr>\n'
               '\t\t<tr><td>Cash on Delivery</td><td>bKash / Nagad of your choice</td><td>We never refund '
               'cash door-to-door; mobile-wallet is the safe + traceable channel.</td></tr>\n'
               '\t\t<tr><td>bKash (mobile wallet)</td><td>Same bKash number</td><td>If your number changed, '
               'contact support to update.</td></tr>\n'
               '\t\t<tr><td>Nagad (mobile wallet)</td><td>Same Nagad number</td><td>Same as '
               'bKash.</td></tr>\n'
               '\t\t<tr><td>Visa / MasterCard / AMEX (via SSLCommerz)</td><td>Original '
               'card</td><td>Card-network rules mean we cannot redirect a card refund to another '
               'card.</td></tr>\n'
               '\t\t<tr><td>SGT Cart Wallet (in-app credit)</td><td>Wallet</td><td>Instant. Refunds via '
               'Wallet can be requested for any payment type.</td></tr>\n'
               '\t\t<tr><td>Reward Points used in the Order</td><td>Reverted to Points '
               'balance</td><td>Instant.</td></tr>\n'
               '\t</table>\n'
               '\n'
               '\t<h2 id="full-partial">4. Full vs. partial refund</h2>\n'
               '\t<p>\n'
               '\t\t<strong>Full refund</strong> means you get back 100% of the amount you\n'
               '\t\tpaid for that item — including any VAT and the Sub-Order shipping fee\n'
               "\t\twhen the issue was the Seller's fault (damaged, wrong, counterfeit).\n"
               '\t</p>\n'
               '\t<p>\n'
               '\t\t<strong>Partial refund</strong> is offered when:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>The product is usable but materially less than promised (e.g., 1-month battery '
               'instead of 1-year) — typical settlement 20-50%.</li>\n'
               '\t\t<li>You return an item with missing accessories (charger, manual, free gift) — the value '
               'of the missing items is deducted.</li>\n'
               '\t\t<li>The product is returned in a condition the Seller can no longer resell — up to 30% '
               'restocking discount may be deducted, with photo evidence.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tYou always have the option to refuse a partial offer and escalate via\n'
               '\t\t<a href="/dispute-resolution/">Dispute Resolution</a>.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="timelines">5. Timeline matrix</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Step</th><th>Standard timeline</th></tr>\n'
               '\t\t<tr><td>Approval of refund request</td><td>Instant for cancellation / Seller-cancel '
               'cases; up to 48 hours for return-based refunds.</td></tr>\n'
               '\t\t<tr><td>Item pickup (if return required)</td><td>1-3 business days after '
               'approval.</td></tr>\n'
               '\t\t<tr><td>Condition check by Seller / SGT QC</td><td>2-3 business days after Seller '
               'receives the item.</td></tr>\n'
               '\t\t<tr><td>Refund initiation</td><td>Same day as condition-check approval.</td></tr>\n'
               '\t\t<tr><td>Money lands — bKash / Nagad / Wallet</td><td>Instant to 24 hours after '
               'initiation.</td></tr>\n'
               '\t\t<tr><td>Money lands — Visa / MasterCard / AMEX</td><td>5-10 business days after '
               'initiation (issuer-dependent).</td></tr>\n'
               '\t\t<tr><td>Reward points reverted</td><td>Instant on initiation.</td></tr>\n'
               '\t</table>\n'
               '\t<p>\n'
               '\t\tIf a refund is "initiated" on our side but you don\'t see it in 10\n'
               '\t\tbusiness days for cards (3 days for wallets), contact\n'
               '\t\t<a href="mailto:support@sgtcart.com">support@sgtcart.com</a> with the\n'
               "\t\tOrder number — we'll give you the bank reference so you can chase your\n"
               '\t\tcard issuer.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="shipping-fee">6. Treatment of shipping fees</h2>\n'
               '\t<ul>\n'
               "\t\t<li><strong>Seller's fault (damaged / wrong / counterfeit / not delivered):</strong>\n"
               '\t\t\tForward shipping is refunded with the item. Return shipping is free\n'
               '\t\t\t(charged to the Seller).</li>\n'
               "\t\t<li><strong>Buyer's choice (changed mind, didn't fit):</strong> Forward\n"
               '\t\t\tshipping is <em>not</em> refunded. Buyer pays return shipping\n'
               '\t\t\t(Tk 60-150 depending on weight and district).</li>\n'
               '\t\t<li><strong>Multi-item Sub-Order returned partially:</strong> Forward\n'
               '\t\t\tshipping is refunded proportionally to the value returned — except\n'
               '\t\t\tif returning a single item leaves the cart below the free-shipping\n'
               "\t\t\tthreshold (we don't claw back the free-shipping benefit).</li>\n"
               '\t</ul>\n'
               '\n'
               '\t<h2 id="points-coupons">7. Reward points &amp; coupons</h2>\n'
               '\t<p>\n'
               '\t\tIf you used reward points to pay for an Order that is later refunded:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>The points are reverted to your balance instantly.</li>\n'
               '\t\t<li>The cash portion of the Order is refunded to your original payment method.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tIf a single-use coupon was used and the Order is refunded:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>If the entire Order is cancelled before shipping, the coupon is restored to your '
               'account.</li>\n'
               '\t\t<li>If the Order shipped and was later returned (full), the coupon is\n'
               '\t\t\t<strong>not</strong> restored. This prevents abuse where customers\n'
               '\t\t\torder, claim "changed mind", and farm the coupon repeatedly. You may\n'
               '\t\t\tinstead receive an equivalent value as Wallet credit if you prefer.</li>\n'
               '\t\t<li>Bulk-pricing tier discounts apply at order time — if a return drops\n'
               '\t\t\tthe quantity below the tier threshold, the per-unit price for the\n'
               '\t\t\tremaining items is recalculated, and the difference is debited from\n'
               '\t\t\tthe refund.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="escalation">8. Escalation when a refund is denied</h2>\n'
               '\t<p>\n'
               '\t\tIf a Seller refuses your refund or offers an amount you consider unfair:\n'
               '\t</p>\n'
               '\t<ol>\n'
               '\t\t<li>The case automatically enters <strong>SGT mediation</strong> after 48 hours of '
               'seller silence or upon your "I dispute this" tap. See <a '
               'href="/help/buyer-protection/">Buyer Protection</a> for the mediation procedure.</li>\n'
               "\t\t<li>Mediator's decision is binding for fund disbursement.</li>\n"
               '\t\t<li>If you remain unsatisfied, you may escalate via\n'
               '\t\t\t<a href="/dispute-resolution/">Dispute Resolution</a> all the way\n'
               '\t\t\tto CRPA §76 redressal or arbitration.</li>\n'
               '\t</ol>\n'
               '\n'
               '\t<h2 id="examples">9. Worked examples</h2>\n'
               '\n'
               "\t<h3>Example 1 — Damaged on arrival (Seller's fault)</h3>\n"
               '\t<p>\n'
               '\t\tYou order a glass jar set for Tk 850 + Tk 60 shipping = Tk 910 paid by\n'
               '\t\tbKash. The jar arrives broken. You upload photos and request a full\n'
               '\t\trefund.\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>Pickup arranged free of charge.</li>\n'
               '\t\t<li>Seller confirms damage within 2 days.</li>\n'
               '\t\t<li>You receive Tk 910 back on your bKash within 24 hours of confirmation.</li>\n'
               '\t\t<li>You pay nothing.</li>\n'
               '\t</ul>\n'
               '\n'
               "\t<h3>Example 2 — Changed mind on a shirt (buyer's choice)</h3>\n"
               '\t<p>\n'
               '\t\tYou buy a Tk 1,200 shirt + Tk 80 shipping = Tk 1,280, paid by Visa.\n'
               "\t\tThe colour doesn't suit you. You request a return on day 5.\n"
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>Pickup arranged. Return shipping Tk 90 charged at pickup (you pay the courier in '
               'cash).</li>\n'
               '\t\t<li>Seller confirms condition.</li>\n'
               '\t\t<li>You receive Tk 1,200 back on your card within 7-10 business days. Forward shipping '
               '(Tk 80) is not refunded.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h3>Example 3 — Partial refund for missing accessory</h3>\n'
               '\t<p>\n'
               '\t\tYou buy a Bluetooth speaker for Tk 3,500 (no shipping — free-shipping\n'
               '\t\tthreshold reached). It arrives without the USB-C cable that the\n'
               '\t\tListing showed. You request a partial refund and keep the speaker.\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>Seller agrees to a Tk 350 partial refund (10% of value).</li>\n'
               '\t\t<li>Refund routed to your SGT Cart Wallet instantly because you chose it.</li>\n'
               '\t</ul>',
  'toc': [{'anchor': 'scope', 'label': '1. Scope & legal basis'},
          {'anchor': 'when', 'label': '2. When you qualify for a refund'},
          {'anchor': 'methods', 'label': '3. Refund methods by payment type'},
          {'anchor': 'full-partial', 'label': '4. Full vs. partial refund'},
          {'anchor': 'timelines', 'label': '5. Timeline matrix'},
          {'anchor': 'shipping-fee', 'label': '6. Treatment of shipping fees'},
          {'anchor': 'points-coupons', 'label': '7. Reward points & coupons'},
          {'anchor': 'escalation', 'label': '8. Escalation when a refund is denied'},
          {'anchor': 'examples', 'label': '9. Worked examples'}],
  'faq': [{'q': 'Why does a card refund take 7-10 days but bKash is instant?',
           'a': 'Card refunds pass through three networks (us → SSLCommerz → card scheme → your issuing '
                'bank). Each step has its own clearing window. bKash and Nagad refunds are direct '
                'wallet-to-wallet within Bangladesh and complete much faster.'},
          {'q': 'Can I split the refund — half to bKash, half to wallet?',
           'a': "No, a single refund goes to one method. If you'd like Wallet credit but paid by COD, choose "
                'Wallet on the refund-method step — the original COD method is no longer available.'},
          {'q': 'What if I never see the money even after 10 days?',
           'a': "Email support@sgtcart.com with the Order number. We'll send you the gateway reference "
                'number and you can ask your card issuer to investigate. We are happy to coordinate.'},
          {'q': 'Is VAT refunded too?',
           'a': 'Yes. The amount you actually paid was VAT-inclusive, and the amount refunded is also '
                "VAT-inclusive. You don't have to track it separately."},
          {'q': 'Does this policy override what a seller writes on their product page?',
           'a': 'Yes. Sellers cannot publish refund terms more restrictive than this Policy or the CRPA. If '
                "a seller's listing contradicts this Policy, this Policy wins."}],
  'related': [{'href': '/returns/', 'title': 'Returns', 'desc': 'How to physically send items back.'},
              {'href': '/help/cancellations/',
               'title': 'Cancellations',
               'desc': 'Cancel before shipment for an instant refund.'},
              {'href': '/help/buyer-protection/',
               'title': 'Buyer Protection',
               'desc': '60-day claim window with full coverage.'},
              {'href': '/dispute-resolution/',
               'title': 'Dispute Resolution',
               'desc': 'Escalation ladder when a refund is denied.'}]},
 {'slug': 'help/payment-methods',
  'title': 'Payment Methods',
  'subtitle': 'Every way you can pay on SGT Cart — Cash on Delivery, mobile wallets, cards, reward points.',
  'section': 'Customer Help',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 230,
  'body_html': '<p class="lead small">\n'
               '\t\tSGT Cart supports every major payment channel used in Bangladesh.\n'
               '\t\tChoose the one that suits you at checkout — your selection is saved\n'
               '\t\tper Order, not stored as a card on file, unless you explicitly opt in.\n'
               '\t\tAll transactions are denominated in <strong>Bangladeshi Taka (BDT, Tk)</strong>.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="overview">1. Overview &amp; currency</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Method</th><th>Fee to customer</th><th>Best for</th></tr>\n'
               '\t\t<tr><td>Cash on Delivery</td><td>Tk 20 service fee (waived above Tk '
               '1,000)</td><td>First-time buyers, cash-preferring areas</td></tr>\n'
               '\t\t<tr><td>bKash</td><td>None (SGT absorbs the gateway fee)</td><td>Fast prepaid orders, '
               'instant refunds</td></tr>\n'
               '\t\t<tr><td>Nagad</td><td>None</td><td>Same as bKash</td></tr>\n'
               '\t\t<tr><td>Visa / MasterCard / AMEX / Discover</td><td>None for the '
               'buyer</td><td>Higher-value orders, frequent shoppers</td></tr>\n'
               '\t\t<tr><td>SGT Cart Wallet credit</td><td>None</td><td>Refunds, returning '
               'customers</td></tr>\n'
               '\t\t<tr><td>Reward Points</td><td>None</td><td>Stack with another method</td></tr>\n'
               '\t</table>\n'
               '\t<p>\n'
               '\t\tAll prices on the Platform are <strong>VAT-inclusive</strong>. The number\n'
               '\t\tyou see at checkout is what you pay — no hidden top-ups.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="cod">2. Cash on Delivery (COD)</h2>\n'
               '\t<p>\n'
               '\t\tPay in cash to the courier when the parcel arrives. Available in most\n'
               '\t\tdistricts in Bangladesh, subject to:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Maximum order value:</strong> Tk 25,000 per Order. Higher-value Orders '
               'require prepayment.</li>\n'
               '\t\t<li><strong>Service fee:</strong> Tk 20 per Sub-Order, waived for Orders ≥ Tk '
               '1,000.</li>\n'
               '\t\t<li><strong>Address eligibility:</strong> Some remote areas may be excluded; the COD '
               'option is hidden at checkout when unavailable.</li>\n'
               '\t\t<li><strong>First-time buyer review:</strong> For very new accounts, COD may be '
               'restricted on the first 1-2 Orders to reduce fraud risk.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tThe courier carries a printed invoice. You inspect the parcel for\n'
               "\t\tobvious damage, pay the exact amount (or use the courier's change\n"
               '\t\tfloat), and receive a receipt. <strong>Open the parcel only after payment</strong>\n'
               '\t\t— the courier cannot accept the parcel back at the door.\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tIf you find an issue after opening, follow the\n'
               '\t\t<a href="/returns/">Returns</a> flow for refund or replacement.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="bkash-nagad">3. bKash &amp; Nagad mobile wallets</h2>\n'
               '\t<p>The two biggest mobile-money providers in Bangladesh, both supported:</p>\n'
               '\t<ol>\n'
               '\t\t<li>At checkout, select <strong>bKash</strong> or <strong>Nagad</strong>.</li>\n'
               "\t\t<li>Click <em>Confirm &amp; pay</em>. You're redirected to the wallet's secure "
               'page.</li>\n'
               '\t\t<li>Enter your mobile number and one-time PIN sent to your phone (we never see your '
               'wallet PIN).</li>\n'
               '\t\t<li>On success you return to SGT Cart with the Order confirmation.</li>\n'
               '\t</ol>\n'
               '\t<p>\n'
               '\t\tIf you abandon the payment or it fails, the Order remains in\n'
               '\t\t<strong>"Payment pending"</strong> state for 30 minutes — you can retry\n'
               '\t\tfrom the Order page without losing your cart. After 30 minutes the\n'
               '\t\tOrder is cancelled and any reward points / coupon are restored.\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tRefunds to bKash / Nagad land in the <strong>same mobile-wallet\n'
               '\t\tnumber</strong>. If your number has changed, contact\n'
               '\t\t<a href="mailto:support@sgtcart.com">support@sgtcart.com</a> with proof\n'
               '\t\t(KYC screenshot) to update before the refund is initiated.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="card">4. Card payments (Visa, MasterCard, AMEX, Discover)</h2>\n'
               '\t<p>\n'
               '\t\tCard payments are processed by <strong>SSLCommerz</strong>, a PCI-DSS-certified\n'
               '\t\tgateway. SGT Cart <strong>never sees your full card number, CVV or 3D-Secure '
               'PIN</strong>.\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>Cards issued by any Bangladesh-licensed bank are accepted.</li>\n'
               '\t\t<li>International-issued cards: accepted for most product categories. A small set '
               '(high-value electronics, gold, gift cards) may be restricted by SSLCommerz risk rules.</li>\n'
               '\t\t<li><strong>Save card for next time:</strong> SSLCommerz can tokenise your card for '
               "one-tap subsequent payments. The token, not the number, is what's stored — and you can "
               'delete it from <a href="/profile-info/">Account → Payment Methods</a> any time.</li>\n'
               '\t\t<li><strong>3D-Secure (OTP):</strong> Most banks now require an OTP from your phone '
               'before the charge completes. Have your phone ready.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tFailed card payments do not place the Order. Card authorisations that\n'
               '\t\texpire after a failed checkout are released by your bank within 5-7 days.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="points-wallet">5. Reward Points &amp; SGT Wallet</h2>\n'
               '\t<p>\n'
               '\t\tBoth are SGT Cart-internal balances — no external transfer involved,\n'
               '\t\tno fee.\n'
               '\t</p>\n'
               '\t<h3>Reward Points</h3>\n'
               '\t<ul>\n'
               '\t\t<li>Earned when a Sub-Order is delivered, at the rate disclosed on the\n'
               '\t\t\t<a href="/help/rewards/">Rewards</a> page.</li>\n'
               '\t\t<li>Each point = Tk 1 at checkout. You can use up to your full balance\n'
               '\t\t\ton any Order, subject to a cap of <strong>30% of the cart subtotal</strong>\n'
               '\t\t\tso cash never goes to zero.</li>\n'
               '\t\t<li>Points and cash can be combined in the same checkout.</li>\n'
               '\t\t<li>Points have no cash-out value — they only redeem against Orders.</li>\n'
               '\t</ul>\n'
               '\t<h3>SGT Cart Wallet</h3>\n'
               '\t<ul>\n'
               '\t\t<li>Credit balance created when you accept a refund as Wallet credit (instant) or when '
               'SGT Cart issues a goodwill / promotional credit.</li>\n'
               '\t\t<li>Spends like cash — no 30% cap, no expiry.</li>\n'
               "\t\t<li>Not withdrawable to bank / bKash. It's purely Platform credit.</li>\n"
               '\t</ul>\n'
               '\n'
               '\t<h2 id="security">6. Security &amp; failed payments</h2>\n'
               '\t<ul>\n'
               '\t\t<li>The Platform is HTTPS-only (TLS 1.2+) on every page and every API call.</li>\n'
               "\t\t<li>Card data goes directly from your browser to SSLCommerz over an iframe. SGT Cart's "
               'servers never receive it.</li>\n'
               "\t\t<li>Mobile-wallet PINs are entered on the wallet's own page, not ours.</li>\n"
               '\t\t<li>All payment events are logged with an idempotency key, so a refresh or '
               'duplicate-submit cannot double-charge you.</li>\n'
               '\t\t<li>Any unusual activity (multiple failed cards, unrecognised device) may trigger a '
               'one-time email verification before checkout completes.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tIf you spot an unfamiliar charge from SGT Cart on your statement,\n'
               '\t\temail <a href="mailto:support@sgtcart.com">support@sgtcart.com</a>\n'
               '\t\twith the date, amount and last 4 digits of the card. We respond\n'
               '\t\twithin 24 hours, share the gateway reference, and refund any\n'
               '\t\tunauthorised charge after investigation.\n'
               '\t</p>',
  'toc': [{'anchor': 'overview', 'label': '1. Overview & currency'},
          {'anchor': 'cod', 'label': '2. Cash on Delivery'},
          {'anchor': 'bkash-nagad', 'label': '3. bKash & Nagad mobile wallets'},
          {'anchor': 'card', 'label': '4. Card payments (Visa, MasterCard, AMEX)'},
          {'anchor': 'points-wallet', 'label': '5. Reward Points & SGT Wallet'},
          {'anchor': 'security', 'label': '6. Security & failed payments'}],
  'faq': [{'q': 'Can I split one order across two payment methods?',
           'a': 'Yes within limits: you can combine reward points + one cash method (COD or wallet or card) '
                'in a single checkout. You cannot mix two cash methods (e.g., half COD half card).'},
          {'q': 'Is there a fee for paying by card?',
           'a': 'No fee for the buyer. SGT Cart absorbs the SSLCommerz processing fee. For COD, a Tk 20 '
                'service fee applies on Orders below Tk 1,000 to cover the courier-cash-handling cost.'},
          {'q': 'How do I save a card for next time?',
           'a': "On the SSLCommerz page during checkout, tick 'Save this card'. You'll see your saved cards "
                'listed at next checkout; pick one and only the CVV+OTP is needed. Manage saved cards under '
                'Account → Payment Methods.'},
          {'q': "My bKash payment showed 'success' but the order says 'pending' — what now?",
           'a': 'Wait 2-5 minutes (sometimes the IPN callback is delayed). If still pending, contact '
                "support@sgtcart.com with your bKash transaction ID — we'll reconcile within 24 hours."},
          {'q': 'Why was COD blocked on my account?',
           'a': 'Either the Order exceeded Tk 25,000, the address is outside the COD service area, or the '
                'account is new (first 1-2 Orders may need prepayment). Choose a prepaid method to '
                'proceed.'}],
  'related': [{'href': '/shipping/',
               'title': 'Shipping & Delivery',
               'desc': 'Where we deliver and how much it costs.'},
              {'href': '/help/rewards/', 'title': 'Reward Points', 'desc': 'How to earn and redeem points.'},
              {'href': '/refund-policy/',
               'title': 'Refund Policy',
               'desc': 'How money comes back to each payment method.'},
              {'href': '/security/',
               'title': 'Security Practices',
               'desc': 'How we keep card and wallet data safe.'}]},
 {'slug': 'help/cancellations',
  'title': 'Order Cancellation',
  'subtitle': 'How to cancel an SGT Cart order — by you, by the seller, or by SGT Cart — and what happens to '
              'your money.',
  'section': 'Customer Help',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 240,
  'body_html': '<p class="lead small">\n'
               '\t\tPlans change. SGT Cart makes it easy to cancel an Order before it\n'
               '\t\tships — no questions asked, no fee. This page explains exactly when\n'
               '\t\tyou can cancel, who else can cancel, and where the money goes.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="self">1. Cancel an order yourself</h2>\n'
               '\t<p>You can cancel a Sub-Order at any time before its status changes to '
               '<strong>Shipped</strong>:</p>\n'
               '\t<ol>\n'
               '\t\t<li>Open <a href="/my-orders/">My Orders</a> and tap the Order.</li>\n'
               '\t\t<li>Find the Sub-Order you want to cancel (one Order may have multiple, each from a '
               'different Seller).</li>\n'
               '\t\t<li>Tap <strong>"Cancel"</strong> next to the Sub-Order.</li>\n'
               '\t\t<li>Choose a reason (optional but useful for us). Common reasons:\n'
               '\t\t\t<em>changed my mind</em>, <em>found cheaper elsewhere</em>,\n'
               '\t\t\t<em>ordered by mistake</em>, <em>delivery taking too long</em>,\n'
               '\t\t\t<em>wrong address</em>.</li>\n'
               '\t\t<li>Confirm. The Sub-Order moves to <strong>Cancelled</strong> and the Seller is '
               'notified instantly.</li>\n'
               '\t</ol>\n'
               '\t<p>\n'
               '\t\tCancellation is <strong>instant</strong>. There is no waiting period\n'
               '\t\tand no fee. Your reward points and any coupon used are returned to\n'
               '\t\tyour account immediately.\n'
               '\t</p>\n'
               '\t<blockquote class="small">\n'
               '\t\tIf your Order has multiple Sub-Orders and you only want to cancel one\n'
               '\t\tof them, the rest continue normally — each Sub-Order is independent.\n'
               '\t</blockquote>\n'
               '\n'
               '\t<h2 id="seller">2. Seller-initiated cancellation</h2>\n'
               '\t<p>Sellers may cancel a Sub-Order in specific cases:</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Out of stock</strong> — the displayed stock was wrong; the Seller cannot '
               'fulfil.</li>\n'
               '\t\t<li><strong>Unreachable address</strong> — phone unreachable + the location is outside '
               "the Seller's serviceable zone, after at least one attempt to contact you.</li>\n"
               '\t\t<li><strong>Payment never cleared</strong> — for prepaid Orders that remained in '
               '"payment failed" state for more than 48 hours.</li>\n'
               '\t\t<li><strong>Suspected fraud</strong> — flagged by our risk engine; Seller may decline '
               'and escalate to SGT review.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tWhen a Seller cancels, you receive an in-app notification + email with\n'
               '\t\tthe reason. The Sub-Order is refunded in full per §4. If a Seller\n'
               '\t\tcancels within 24 hours of order placement, no penalty applies; later\n'
               '\t\tthan that, our <a href="/seller-terms/#performance">performance tracker</a>\n'
               '\t\tlogs it against the Seller, and you receive a <strong>Tk 50 inconvenience '
               'credit</strong>\n'
               '\t\tto your SGT Cart Wallet.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="platform">3. SGT Cart cancellations</h2>\n'
               '\t<p>SGT Cart itself may cancel an Order or Sub-Order when:</p>\n'
               '\t<ul>\n'
               '\t\t<li>The Listing turns out to violate our <a href="/sell/listing-guidelines/">Listing '
               'Guidelines</a> (counterfeit, prohibited item, mis-priced).</li>\n'
               '\t\t<li>A Seller is suspended (e.g., counterfeit confirmed, anti-disintermediation 2-strike, '
               'or fraud investigation).</li>\n'
               '\t\t<li>A clear pricing error is detected before the Sub-Order ships (e.g., Tk 50 for a Tk '
               '50,000 product).</li>\n'
               '\t\t<li>A government / court order requires it (rare).</li>\n'
               '\t\t<li>The Order is on the Bangladesh customs prohibited list (will only occur once '
               'international becomes relevant).</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               "\t\tAffected Orders are refunded in full per §4. You'll receive an email\n"
               '\t\twith the specific reason and (if appropriate) a discount voucher for\n'
               '\t\tyour next Order.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="refund">4. What happens to your payment</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>How you paid</th><th>What happens on cancellation</th></tr>\n'
               '\t\t<tr><td>Cash on Delivery (no cash collected yet)</td><td>Nothing to refund — the '
               "Sub-Order is just cancelled. The courier won't visit.</td></tr>\n"
               '\t\t<tr><td>bKash / Nagad</td><td>Refunded to the same wallet within 2-3 business '
               'days.</td></tr>\n'
               '\t\t<tr><td>Card via SSLCommerz</td><td>Authorisation reversed (often within minutes) or '
               'refunded to the card within 5-10 business days, depending on whether the bank had already '
               'captured the funds.</td></tr>\n'
               '\t\t<tr><td>SGT Cart Wallet credit</td><td>Returned to Wallet instantly.</td></tr>\n'
               '\t\t<tr><td>Reward Points used</td><td>Reverted to your Points balance instantly.</td></tr>\n'
               '\t\t<tr><td>Coupon used</td><td>Coupon restored to your account on a self-cancel; not '
               'restored on a Seller- or SGT-initiated cancel involving fraud.</td></tr>\n'
               '\t</table>\n'
               '\t<p>See the <a href="/refund-policy/">Refund Policy</a> for the full timeline matrix.</p>\n'
               '\n'
               '\t<h2 id="cant">5. When you can no longer cancel</h2>\n'
               '\t<p>Once the Sub-Order status is <strong>Shipped</strong>, the "Cancel" button disappears. '
               'At that point:</p>\n'
               '\t<ul>\n'
               '\t\t<li>If you refuse to accept delivery at the door, the parcel will be returned to the '
               'Seller — this counts as a return, see <a href="/returns/">Returns</a>.</li>\n'
               '\t\t<li>If the parcel is already in transit and you no longer want it, you can request the '
               'courier to "Return to sender" (a service fee may apply if the cancellation was on '
               'you).</li>\n'
               '\t\t<li>After delivery, the path is the <a href="/returns/">Returns</a> flow.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\t<strong>Custom-made or made-to-order items</strong> may have a\n'
               '\t\tcancellation cutoff earlier than "Shipped" because the Seller starts\n'
               '\t\twork immediately on order. The cutoff is shown on the Listing — once\n'
               '\t\tpassed, only the <a href="/dispute-resolution/">Dispute Resolution</a>\n'
               '\t\troute is available.\n'
               '\t</p>',
  'toc': [{'anchor': 'self', 'label': '1. Cancel an order yourself'},
          {'anchor': 'seller', 'label': '2. Seller-initiated cancellation'},
          {'anchor': 'platform', 'label': '3. SGT Cart cancellations'},
          {'anchor': 'refund', 'label': '4. What happens to your payment'},
          {'anchor': 'cant', 'label': '5. When you can no longer cancel'}],
  'faq': [{'q': 'Does it cost me anything to cancel?',
           'a': 'No. Cancellation before shipment is free for any reason. No restocking fee, no cancellation '
                'fee.'},
          {'q': "My order says 'Processing' — can I still cancel?",
           'a': "Yes. 'Processing' means the Seller has accepted but hasn't shipped. The Cancel button is "
                'available.'},
          {'q': 'Can I cancel just one item out of three?',
           'a': 'If the three items are from different Sellers (i.e., separate Sub-Orders), yes — each '
                "Sub-Order cancels independently. If they're from the same Seller in one Sub-Order, you "
                "cancel the whole Sub-Order; we don't yet support per-line-item cancellation within a single "
                'Sub-Order.'},
          {'q': 'The seller cancelled my order — do I lose my coupon?',
           'a': 'No. When the Seller cancels (out-of-stock, etc.), your coupon is restored to your account. '
                'If you used reward points, those are also returned.'},
          {'q': 'I missed the Cancel window — can SGT Cart force-cancel for me?',
           'a': 'Only in special cases (counterfeit, prohibited item, clear pricing error). For ordinary '
                "changes-of-mind after shipment, you'll need to refuse delivery or return per the Returns "
                'flow.'}],
  'related': [{'href': '/refund-policy/',
               'title': 'Refund Policy',
               'desc': 'Where the refund goes and how long it takes.'},
              {'href': '/returns/', 'title': 'Returns', 'desc': 'If the item already shipped or arrived.'},
              {'href': '/help/buyer-protection/',
               'title': 'Buyer Protection',
               'desc': "When the seller won't cancel and won't deliver."}]},
 {'slug': 'help/buyer-protection',
  'title': 'Buyer Protection Program',
  'subtitle': "The 60-day safety net for every order on SGT Cart — what's covered, what's not, and how to "
              'claim.',
  'section': 'Customer Help',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 250,
  'body_html': '<p class="lead small">\n'
               '\t\tEvery Order on SGT Cart comes with the <strong>Buyer Protection Program</strong>\n'
               '\t\tat no extra cost. Think of it as a 60-day safety net: if a Seller\n'
               "\t\tdisappears, ships the wrong item, sends a counterfeit, or simply won't\n"
               "\t\tcooperate, we step in, judge the case fairly and make sure you're not\n"
               '\t\tout of pocket.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="promise">1. The SGT Cart promise</h2>\n'
               '\t<p>If, within 60 days of placing an Order, any of the following happens:</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Non-delivery</strong> — the item never arrives within the maximum displayed '
               'ETA plus 5 grace days.</li>\n'
               '\t\t<li><strong>Wrong item</strong> — what you received is materially different from what '
               'was ordered.</li>\n'
               '\t\t<li><strong>Damaged on arrival</strong> — the item was broken or non-functional when the '
               'parcel was opened.</li>\n'
               '\t\t<li><strong>Counterfeit</strong> — the item is a fake of a branded original.</li>\n'
               '\t\t<li><strong>Materially not as described</strong> — capacity, size, colour, ingredients, '
               "warranty or other claim doesn't match the Listing.</li>\n"
               '\t</ul>\n'
               '\t<p>\n'
               '\t\t…you can file a Buyer Protection claim and we will, after review,\n'
               '\t\t<strong>refund, replace or credit</strong> you in line with the\n'
               '\t\t<a href="/refund-policy/">Refund Policy</a>.\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tThis protection sits on top of your statutory rights under the Consumer\n'
               '\t\tRights Protection Act 2009 — it never reduces them.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="covered">2. What\'s covered</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Issue</th><th>Coverage</th><th>Typical outcome</th></tr>\n'
               '\t\t<tr><td>Non-delivery</td><td>Full</td><td>Full refund</td></tr>\n'
               '\t\t<tr><td>Damaged on arrival</td><td>Full</td><td>Full refund OR free '
               'replacement</td></tr>\n'
               '\t\t<tr><td>Wrong item (size / colour / model)</td><td>Full</td><td>Full refund OR free '
               'replacement</td></tr>\n'
               '\t\t<tr><td>Counterfeit</td><td>Full</td><td>Full refund (keep or return); Seller '
               'strike</td></tr>\n'
               '\t\t<tr><td>Defective on use (within warranty)</td><td>Full</td><td>Repair, replace or '
               'refund per the manufacturer warranty</td></tr>\n'
               '\t\t<tr><td>Materially not as described</td><td>Full or Partial</td><td>Partial refund '
               '(keep), full refund, or replacement</td></tr>\n'
               '\t\t<tr><td>Late delivery beyond ETA + 5 days</td><td>Partial</td><td>Tk 100-300 '
               'inconvenience credit, OR cancellation + full refund if you no longer want it</td></tr>\n'
               '\t</table>\n'
               '\n'
               '\t<h2 id="window">3. Claim window</h2>\n'
               '\t<p>You have:</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>60 days</strong> from the date of Order placement to open a Buyer Protection '
               'claim.</li>\n'
               '\t\t<li><strong>7 days</strong> from delivery for ordinary "change of mind" returns '
               '(different process — see <a href="/returns/">Returns</a>).</li>\n'
               '\t\t<li><strong>Manufacturer warranty period</strong> (varies by product) for '
               'defective-on-use claims — Buyer Protection covers the path from you to SGT Cart; the '
               'warranty itself is honoured by the Seller or brand service centre.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="file">4. How to file a claim</h2>\n'
               '\t<ol>\n'
               '\t\t<li>Open <a href="/my-orders/">My Orders</a> and tap the affected Sub-Order.</li>\n'
               '\t\t<li>Tap <strong>"File Buyer Protection claim"</strong> (this appears once direct chat '
               'with the Seller has been open for 48+ hours or you choose to skip it).</li>\n'
               '\t\t<li>Select the issue category and describe the problem in your own words.</li>\n'
               '\t\t<li>Upload evidence (§5).</li>\n'
               '\t\t<li>Choose the outcome you want — refund, replacement, partial credit.</li>\n'
               '\t\t<li>Submit. You receive a claim ID and an in-app status tracker.</li>\n'
               '\t</ol>\n'
               '\t<p>\n'
               "\t\tFiling a claim <strong>freezes the Seller's Wallet</strong> for the\n"
               '\t\tamount of the Order so we can honour the eventual decision without\n'
               '\t\tchasing the Seller for money.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="evidence">5. Evidence we ask for</h2>\n'
               '\t<p>The more concrete the evidence, the faster the decision. Useful items:</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Photos of the unopened parcel</strong> — shows weight and seal in case the '
               'parcel was tampered with.</li>\n'
               '\t\t<li><strong>Unboxing video</strong> — single take, no cuts, showing the seal break, '
               'contents, item condition.</li>\n'
               '\t\t<li><strong>Photos of the item</strong> — close-ups of damage, serial number, '
               'manufacturing details.</li>\n'
               '\t\t<li><strong>Screenshots of chat</strong> — what the Seller said when you raised '
               'it.</li>\n'
               "\t\t<li><strong>For counterfeit:</strong> serial-number verification on the brand's site "
               '(where applicable), comparison photos with an authentic unit.</li>\n'
               '\t\t<li><strong>For non-delivery:</strong> the parcel-tracking page screenshot showing '
               '"delivered" or "stuck in transit".</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tWe never ask for the original packaging or warranty card to <em>open</em>\n'
               '\t\ta claim; we may ask for them later if the Seller offers a replacement.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="timeline">6. Resolution timeline &amp; outcomes</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Step</th><th>SLA</th></tr>\n'
               '\t\t<tr><td>Claim acknowledged + Seller notified</td><td>Within 24 hours</td></tr>\n'
               "\t\t<tr><td>Seller's response window</td><td>48 hours (after which the case "
               'auto-escalates)</td></tr>\n'
               '\t\t<tr><td>Mediator review &amp; decision</td><td>Within 7 business days</td></tr>\n'
               '\t\t<tr><td>Refund issued (post-decision)</td><td>Per <a '
               'href="/refund-policy/#timelines">timeline matrix</a> — minutes for Wallet, days for '
               'cards</td></tr>\n'
               '\t</table>\n'
               '\t<p>\n'
               '\t\tDecisions are written in plain language with the reason and the\n'
               "\t\tevidence weighed. They are recorded against the Seller's performance\n"
               '\t\tstats. Either party may escalate via <a href="/dispute-resolution/">Dispute '
               'Resolution</a>\n'
               '\t\tif substantively unsatisfied.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="not-covered">7. What\'s not covered</h2>\n'
               '\t<ul>\n'
               "\t\t<li><strong>Buyer's remorse on used items</strong> — once you've opened, used, washed or "
               "assembled a non-defective item, it cannot be returned just because you've changed your "
               'mind.</li>\n'
               '\t\t<li><strong>Claims filed after 60 days</strong> from Order date.</li>\n'
               '\t\t<li><strong>Items in the "Non-eligible" category</strong> per <a '
               'href="/returns/#eligible">Returns</a>, except for damaged / wrong / counterfeit.</li>\n'
               '\t\t<li><strong>Damage caused by the buyer</strong> after delivery (drops, water damage, '
               'modifications).</li>\n'
               '\t\t<li><strong>Items lost while in your possession</strong> — once successful delivery is '
               'confirmed, risk of loss is yours.</li>\n'
               '\t\t<li><strong>Off-platform purchases</strong> — if you contacted the Seller off SGT Cart '
               'and paid them directly (which violates the Anti-Disintermediation Policy), we cannot protect '
               'that transaction.</li>\n'
               '\t\t<li><strong>Indirect or consequential losses</strong> — e.g., you missed an event '
               'because a product arrived late; we cover the product, not the event.</li>\n'
               '\t</ul>',
  'toc': [{'anchor': 'promise', 'label': '1. The SGT Cart promise'},
          {'anchor': 'covered', 'label': "2. What's covered"},
          {'anchor': 'window', 'label': '3. Claim window'},
          {'anchor': 'file', 'label': '4. How to file a claim'},
          {'anchor': 'evidence', 'label': '5. Evidence we ask for'},
          {'anchor': 'timeline', 'label': '6. Resolution timeline & outcomes'},
          {'anchor': 'not-covered', 'label': "7. What's not covered"}],
  'faq': [{'q': 'Do I need to take an unboxing video for every order?',
           'a': 'Not for every order — only when you want to claim damaged-on-arrival or counterfeit. We '
                'strongly recommend filming the unboxing for orders above Tk 5,000 or for fragile items, so '
                'evidence is ready if needed.'},
          {'q': 'Will the seller see my unboxing video?',
           'a': 'Yes, a redacted copy. The Seller can respond with their own evidence. Both sides see what '
                'the mediator sees.'},
          {'q': 'What if I lose my parcel after delivery?',
           'a': 'Buyer Protection covers up to successful delivery to your address. After that, the risk of '
                "loss is yours. We recommend including a 'safe place' instruction at checkout if nobody is "
                'home.'},
          {'q': "Can a seller refuse the mediator's decision?",
           'a': "Not for purposes of refunding you — the funds come from the Seller's Wallet under the "
                'Seller Agreement. The Seller can escalate via the Dispute Resolution ladder if they '
                'disagree with the substance.'},
          {'q': 'Is Buyer Protection a separate insurance policy?',
           'a': "No — it's a contractual programme operated by SGT Cart at no extra cost. There is no "
                'premium, no waiting period, and no underwriter. It is built into every Order.'}],
  'related': [{'href': '/refund-policy/',
               'title': 'Refund Policy',
               'desc': 'Exact rules per payment method and scenario.'},
              {'href': '/returns/', 'title': 'Returns', 'desc': 'Sending an item back, regardless of fault.'},
              {'href': '/dispute-resolution/',
               'title': 'Dispute Resolution',
               'desc': 'Escalation ladder if mediation fails.'},
              {'href': '/help/counterfeit/',
               'title': 'Report Counterfeit',
               'desc': 'Fast track for fake-product reports.'}]},
 {'slug': 'dispute-resolution',
  'title': 'Dispute Resolution & Arbitration',
  'subtitle': 'The five-step ladder for resolving any dispute between you, a Seller, and SGT Cart — from '
              'chat to arbitration.',
  'section': 'Legal',
  'contact_email': 'disputes@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 260,
  'body_html': '<p class="lead small">\n'
               '\t\tMost issues on SGT Cart can be sorted out quickly between buyer and\n'
               "\t\tSeller through the in-app chat. When that doesn't work, this policy\n"
               '\t\tgives a clear escalation path so nobody is stuck. It applies to\n'
               '\t\tcustomers, Sellers, and any disputes about Orders, refunds, listings,\n'
               '\t\tchargebacks or platform-fee adjustments.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="scope">1. Who this policy covers</h2>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Customer ↔ Seller disputes</strong> about a specific Order — non-delivery, '
               'wrong item, damaged item, counterfeit, refund delays.</li>\n'
               '\t\t<li><strong>Customer ↔ SGT Cart</strong> disputes about the Platform itself — reward '
               'points, voucher denial, account closure.</li>\n'
               '\t\t<li><strong>Seller ↔ SGT Cart</strong> disputes about commission, payouts, performance '
               'suspensions, IP takedowns.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tYou agree to follow the steps below <strong>in order</strong> before\n'
               '\t\tapproaching a court. Going straight to court without exhausting these\n'
               '\t\tsteps may result in your case being stayed pending compliance.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="step1">2. Step 1 — Direct contact (up to 7 days)</h2>\n'
               '\t<p>\n'
               '\t\tMany issues can be resolved in a quick chat:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Buyers:</strong> open the Order in <a href="/my-orders/">My Orders</a>\n'
               '\t\t\tand tap "Chat with seller". Describe the issue, attach photos, give\n'
               '\t\t\tthe Seller 48 hours to reply.</li>\n'
               '\t\t<li><strong>Sellers:</strong> respond promptly within the\n'
               '\t\t\t<a href="/seller-terms/#order-acceptance">48-hour SLA</a>. Propose a\n'
               '\t\t\tsolution — refund, replacement, partial credit, free re-delivery.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tKeep the conversation civil and on-platform. Personal contact details,\n'
               '\t\tWhatsApp numbers, off-platform URLs are automatically redacted by our\n'
               '\t\t<a href="/sell/anti-disintermediation/">Anti-Disintermediation</a>\n'
               '\t\tguard and may trigger a violation for Sellers.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="step2">3. Step 2 — Protection claim (within 60 days of order)</h2>\n'
               '\t<p>\n'
               '\t\tIf direct contact does not resolve the issue, file a formal claim:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Customers</strong> file a Buyer Protection claim from\n'
               '\t\t\t<a href="/help/buyer-protection/">Buyer Protection</a>. You\'ll\n'
               '\t\t\tdescribe what went wrong, upload evidence (photos, video,\n'
               '\t\t\tscreenshots of chat) and choose the outcome you want — refund,\n'
               '\t\t\treplacement, or partial credit.</li>\n'
               '\t\t<li><strong>Sellers</strong> use the <a href="/sell/dispute-resolution/">Seller Dispute '
               'Resolution</a>\n'
               '\t\t\tform when they disagree with a refund decision, performance\n'
               '\t\t\tstrike, or commission deduction.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tFiling a claim freezes the relevant payment / Wallet transfer so SGT\n'
               '\t\tCart has funds available to enforce the eventual outcome.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="step3">4. Step 3 — SGT mediation (within 7 business days)</h2>\n'
               '\t<p>\n'
               '\t\tA dedicated mediator from the SGT Cart Trust &amp; Safety team reviews\n'
               "\t\tthe claim, the chat record, the evidence from both sides, the Seller's\n"
               '\t\tperformance history, and any prior strikes. The mediator may:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li>Request further information from either party (3 business days to respond).</li>\n'
               '\t\t<li>Inspect the product, when feasible, by asking the customer to courier it back.</li>\n'
               '\t\t<li>Consult our IP / counterfeit / safety specialists if the issue requires '
               'expertise.</li>\n'
               '\t</ul>\n'
               "\t<p>The mediator's decision will be one of:</p>\n"
               '\t<ul>\n'
               "\t\t<li><strong>Refund / replacement granted</strong> to the customer — Seller's Wallet is "
               'debited and the customer is refunded.</li>\n'
               "\t\t<li><strong>Refund denied</strong> — the Order is closed in the Seller's favour, Wallet "
               'released as normal.</li>\n'
               '\t\t<li><strong>Partial outcome</strong> — e.g., 50% refund without return, where the '
               'product was usable but materially less than promised.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tThe mediation decision is binding for purposes of disbursement of\n'
               '\t\tPlatform-held funds. Either party may still escalate to the steps\n'
               '\t\tbelow if they remain unsatisfied with the substantive outcome.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="step4">5. Step 4 — CRPA §76 redressal (statutory consumer right)</h2>\n'
               '\t<p>\n'
               '\t\tThe <strong>Consumer Rights Protection Act 2009</strong> ("CRPA") gives\n'
               '\t\tconsumers in Bangladesh the right to lodge a complaint with the\n'
               '\t\tNational Consumer Right Protection Department (NCRPD). Under §76 a\n'
               '\t\tconsumer may complain about any of the offences listed in §37-50\n'
               '\t\t(adulterated goods, deceptive pricing, false advertising, refusal to\n'
               '\t\tdeliver promised goods, etc.).\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tIf our mediation outcome did not resolve the dispute to your\n'
               '\t\tsatisfaction, you retain the right to lodge a CRPA complaint:\n'
               '\t</p>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Hotline:</strong> 16121 (NCRPD)</li>\n'
               '\t\t<li><strong>Online:</strong> dncrp.portal.gov.bd</li>\n'
               '\t\t<li><strong>Office:</strong> 1 Karwan Bazar, TCB Bhaban (8th floor), Dhaka 1215.</li>\n'
               '\t</ul>\n'
               '\t<p>\n'
               '\t\tSGT Cart will cooperate fully with any NCRPD inquiry, share relevant\n'
               '\t\ttransaction records, and abide by any direction or compensation order\n'
               '\t\tissued by the Director-General under §70.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="step5">6. Step 5 — Arbitration under the BD Arbitration Act 2001</h2>\n'
               '\t<p>\n'
               '\t\tFor matters that cannot be resolved by the steps above, you and SGT\n'
               '\t\tCart agree to submit the dispute to <strong>final and binding\n'
               '\t\tarbitration</strong> under the <em>Arbitration Act 2001 (Bangladesh)</em>.\n'
               '\t\tThe terms of the arbitration are:\n'
               '\t</p>\n'
               '\t<table>\n'
               '\t\t<tr><th>Item</th><th>Terms</th></tr>\n'
               '\t\t<tr><td>Number of arbitrators</td><td>One (sole arbitrator) — chosen by mutual '
               'agreement; if no agreement within 30 days, appointed by the Bangladesh International '
               'Arbitration Centre (BIAC).</td></tr>\n'
               '\t\t<tr><td>Seat</td><td>Dhaka</td></tr>\n'
               '\t\t<tr><td>Language</td><td>English or Bangla, by election of the claimant.</td></tr>\n'
               '\t\t<tr><td>Rules</td><td>BIAC Rules of Arbitration (current edition) — supplemented by the '
               'Arbitration Act 2001.</td></tr>\n'
               '\t\t<tr><td>Costs</td><td>Each party bears its own, unless the arbitrator orders '
               'otherwise.</td></tr>\n'
               '\t\t<tr><td>Class action / consolidation</td><td>Waived where lawful. Each claim proceeds '
               'individually.</td></tr>\n'
               '\t</table>\n'
               '\t<p>\n'
               '\t\tThe award of the arbitrator is final and binding, enforceable in any\n'
               '\t\tcompetent court. The <strong>courts of Dhaka</strong> retain exclusive\n'
               '\t\tjurisdiction for interim measures (injunctions) and for enforcement\n'
               '\t\tof the arbitration award.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="international">7. International users</h2>\n'
               '\t<p>\n'
               '\t\tIf you are using SGT Cart from outside Bangladesh, this policy does\n'
               '\t\tnot deprive you of consumer-protection rights mandatorily granted by\n'
               '\t\tthe law of the country where you have your habitual residence — for\n'
               '\t\texample, your right to a refund of a defective product under your\n'
               '\t\tlocal consumer-rights statute.\n'
               '\t</p>\n'
               '\t<p>\n'
               '\t\tHowever, the primary forum for any dispute remains the\n'
               '\t\t<strong>Dhaka courts</strong>, and the substantive law applicable to\n'
               '\t\tthe contract remains <strong>Bangladesh law</strong>. International\n'
               '\t\tusers are encouraged to use the mediation step (§4) to take advantage\n'
               '\t\tof the speed and free-of-charge nature of our internal process before\n'
               '\t\tturning to their local consumer authority.\n'
               '\t</p>',
  'toc': [{'anchor': 'scope', 'label': '1. Who this policy covers'},
          {'anchor': 'step1', 'label': '2. Step 1 — Direct contact'},
          {'anchor': 'step2', 'label': '3. Step 2 — Buyer / Seller Protection claim'},
          {'anchor': 'step3', 'label': '4. Step 3 — SGT mediation'},
          {'anchor': 'step4', 'label': '5. Step 4 — CRPA §76 redressal'},
          {'anchor': 'step5', 'label': '6. Step 5 — Arbitration under the BD Arbitration Act 2001'},
          {'anchor': 'international', 'label': '7. International users'}],
  'faq': [{'q': 'How long does the whole ladder take in the worst case?',
           'a': 'Direct contact: up to 7 days. Protection claim review: up to 14 days. Mediation: 7 business '
                'days. CRPA §76 complaint at NCRPD: varies (often 30-60 days). Arbitration: 3-6 months. Most '
                'disputes are resolved at step 1 or step 3.'},
          {'q': 'Do I have to pay anything to file a claim?',
           'a': 'No — Buyer Protection claims and SGT mediation are free. CRPA §76 complaints are free at '
                'the NCRPD. Arbitration involves filing fees, but small claims are usually settled before '
                'reaching that stage.'},
          {'q': 'Can I just sue SGT Cart in court instead?',
           'a': 'By accepting our Terms you agree to follow the ladder before going to court. Courts in '
                'Bangladesh routinely stay proceedings to enforce a pre-litigation contract clause like this '
                'one. The exception is statutory remedies under CRPA — those remain available.'},
          {'q': 'Will the mediator hear me before deciding?',
           'a': 'Yes. Both sides are asked for their version, evidence, and any further information the '
                'mediator wants. The decision includes a short written reasoning so you can see how it was '
                'reached.'},
          {'q': 'If I win at mediation but the seller refuses to refund, what happens?',
           'a': "SGT Cart pays the refund from the Seller's Wallet directly — you do not chase the Seller "
                "for the money. That's why protection claims freeze the Wallet at step 2."}],
  'related': [{'href': '/help/buyer-protection/',
               'title': 'Buyer Protection Program',
               'desc': 'Coverage and claim process for customers.'},
              {'href': '/refund-policy/',
               'title': 'Refund Policy',
               'desc': 'When and how money is returned.'},
              {'href': '/sell/dispute-resolution/',
               'title': 'Seller Dispute Resolution',
               'desc': 'Escalation path for sellers.'},
              {'href': '/terms/',
               'title': 'Customer Terms',
               'desc': 'Master agreement with the dispute clauses.'}]},
 {'slug': 'sell',
  'title': 'Sell on SGT Cart',
  'subtitle': 'Open a shop on SGT Cart and start selling to customers across Bangladesh — bilingual '
              'storefront, multi-payment checkout, real-time chat with buyers, and a mobile-friendly seller '
              'dashboard.',
  'section': 'Seller Resources',
  'contact_email': 'seller-support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 300,
  'body_html': '<p class="lead">\n'
               '\t\tOpen a shop on SGT Cart and start selling to customers across\n'
               '\t\tBangladesh — bilingual storefront, multi-payment checkout, real-time\n'
               '\t\tchat with buyers, and a mobile-friendly seller dashboard.\n'
               '\t</p>\n'
               '\n'
               '\t<div class="row g-2 mt-3">\n'
               '\t\t<div class="col-lg-4 col-md-6">\n'
               '\t\t\t<div class="border rounded p-2 d-flex gap-2 align-items-start">\n'
               '\t\t\t\t<i class="lni lni-checkmark-circle fs-5 theme-cl mt-1"></i>\n'
               '\t\t\t\t<div>\n'
               '\t\t\t\t\t<h6 class="ft-bold mb-1 small">Easy setup</h6>\n'
               '\t\t\t\t\t<p class="text-muted small mb-0">\n'
               '\t\t\t\t\t\tSign up, upload trade licence + NID, admin approves in\n'
               '\t\t\t\t\t\t1-2 days. Store goes live immediately.\n'
               '\t\t\t\t\t</p>\n'
               '\t\t\t\t</div>\n'
               '\t\t\t</div>\n'
               '\t\t</div>\n'
               '\t\t<div class="col-lg-4 col-md-6">\n'
               '\t\t\t<div class="border rounded p-2 d-flex gap-2 align-items-start">\n'
               '\t\t\t\t<i class="lni lni-wallet fs-5 theme-cl mt-1"></i>\n'
               '\t\t\t\t<div>\n'
               '\t\t\t\t\t<h6 class="ft-bold mb-1 small">Fair commission</h6>\n'
               '\t\t\t\t\t<p class="text-muted small mb-0">\n'
               '\t\t\t\t\t\tA small platform commission per delivered sale — no\n'
               '\t\t\t\t\t\tmonthly or listing fees.\n'
               '\t\t\t\t\t</p>\n'
               '\t\t\t\t</div>\n'
               '\t\t\t</div>\n'
               '\t\t</div>\n'
               '\t\t<div class="col-lg-4 col-md-6">\n'
               '\t\t\t<div class="border rounded p-2 d-flex gap-2 align-items-start">\n'
               '\t\t\t\t<i class="lni lni-bar-chart fs-5 theme-cl mt-1"></i>\n'
               '\t\t\t\t<div>\n'
               '\t\t\t\t\t<h6 class="ft-bold mb-1 small">Full analytics</h6>\n'
               '\t\t\t\t\t<p class="text-muted small mb-0">\n'
               '\t\t\t\t\t\tSales dashboard, top products, revenue, reviews,\n'
               '\t\t\t\t\t\tlow-stock alerts — built in.\n'
               '\t\t\t\t\t</p>\n'
               '\t\t\t\t</div>\n'
               '\t\t\t</div>\n'
               '\t\t</div>\n'
               '\t\t<div class="col-lg-4 col-md-6">\n'
               '\t\t\t<div class="border rounded p-2 d-flex gap-2 align-items-start">\n'
               '\t\t\t\t<i class="lni lni-tag fs-5 theme-cl mt-1"></i>\n'
               '\t\t\t\t<div>\n'
               '\t\t\t\t\t<h6 class="ft-bold mb-1 small">Your promotions</h6>\n'
               '\t\t\t\t\t<p class="text-muted small mb-0">\n'
               '\t\t\t\t\t\tCreate store coupons, set discount prices and run flash\n'
               '\t\t\t\t\t\tsales on your own products.\n'
               '\t\t\t\t\t</p>\n'
               '\t\t\t\t</div>\n'
               '\t\t\t</div>\n'
               '\t\t</div>\n'
               '\t\t<div class="col-lg-4 col-md-6">\n'
               '\t\t\t<div class="border rounded p-2 d-flex gap-2 align-items-start">\n'
               '\t\t\t\t<i class="lni lni-comments fs-5 theme-cl mt-1"></i>\n'
               '\t\t\t\t<div>\n'
               '\t\t\t\t\t<h6 class="ft-bold mb-1 small">Direct chat</h6>\n'
               '\t\t\t\t\t<p class="text-muted small mb-0">\n'
               '\t\t\t\t\t\tReply to product questions live; delivery / refund\n'
               '\t\t\t\t\t\tissues go to SGT Support.\n'
               '\t\t\t\t\t</p>\n'
               '\t\t\t\t</div>\n'
               '\t\t\t</div>\n'
               '\t\t</div>\n'
               '\t\t<div class="col-lg-4 col-md-6">\n'
               '\t\t\t<div class="border rounded p-2 d-flex gap-2 align-items-start">\n'
               '\t\t\t\t<i class="lni lni-money-protection fs-5 theme-cl mt-1"></i>\n'
               '\t\t\t\t<div>\n'
               '\t\t\t\t\t<h6 class="ft-bold mb-1 small">Flexible payouts</h6>\n'
               '\t\t\t\t\t<p class="text-muted small mb-0">\n'
               '\t\t\t\t\t\tWithdraw to bKash, Nagad or bank. Scheduled auto-payouts\n'
               '\t\t\t\t\t\tavailable.\n'
               '\t\t\t\t\t</p>\n'
               '\t\t\t\t</div>\n'
               '\t\t\t</div>\n'
               '\t\t</div>\n'
               '\t</div>\n'
               '\n'
               '\t<div class="text-center mt-4">\n'
               '\t\t<a href="/signup/?role=seller" class="btn btn-primary px-4">\n'
               '\t\t\tBecome a seller</a>\n'
               '\t\t<div class="text-muted small mt-2">\n'
               '\t\t\tAlready have a seller account?\n'
               '\t\t\t<a href="/login/">Sign in</a>.\n'
               '\t\t</div>\n'
               '\t</div>',
  'toc': [],
  'faq': [],
  'related': []},
 {'slug': 'sell/onboarding',
  'title': 'Seller Onboarding Guide',
  'subtitle': 'From signup to your first sale on SGT Cart — a step-by-step walkthrough for new sellers.',
  'section': 'Seller Resources',
  'contact_email': 'seller-support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 310,
  'body_html': '<p class="lead small">\n'
               '\t\tOpening a shop on SGT Cart takes about <strong>30 minutes</strong> for\n'
               '\t\tform-filling, plus 1-2 business days for admin verification. This\n'
               '\t\tguide takes you from zero to live store and your first sale.\n'
               '\t</p>\n'
               '\t<p class="small">\n'
               '\t\tRead the <a href="/seller-terms/">Seller Agreement</a> and\n'
               '\t\t<a href="/sell/listing-guidelines/">Listing Guidelines</a> before you\n'
               '\t\tstart — they define the rules you accept by listing.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="eligibility">1. Who can sell on SGT Cart</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>You qualify if you are…</th><th>Required</th></tr>\n'
               '\t\t<tr><td>An individual sole trader resident in Bangladesh</td><td>Aged 18+, valid NID, '
               'Trade Licence, TIN.</td></tr>\n'
               '\t\t<tr><td>A registered company / partnership / proprietorship in Bangladesh</td><td>RJSC '
               "certificate, Trade Licence, TIN, BIN (VAT) if applicable, authorised representative's "
               'NID.</td></tr>\n'
               '\t\t<tr><td>A non-resident Bangladeshi (NRB) with a registered local entity</td><td>Same as '
               'company, plus operating address inside Bangladesh.</td></tr>\n'
               '\t</table>\n'
               '\n'
               '\t<h2 id="documents">2. Documents you\'ll need</h2>\n'
               '\t<ul>\n'
               '\t\t<li><strong>NID</strong> — front + back, clear scan or photo.</li>\n'
               '\t\t<li><strong>Trade Licence</strong> — clear scan (PDF/JPG).</li>\n'
               '\t\t<li><strong>TIN certificate</strong> — issued by the National Board of Revenue.</li>\n'
               '\t\t<li><strong>BIN / VAT registration</strong> — if your annual turnover is above the NBR '
               'threshold.</li>\n'
               '\t\t<li><strong>Bank statement first page</strong> OR <strong>bKash / Nagad merchant account '
               'screenshot</strong>.</li>\n'
               '\t\t<li><strong>Shop logo</strong> (PNG, transparent background, ≥ 256×256 px).</li>\n'
               '\t\t<li><strong>Shop banner</strong> (JPG, 1920×600 px recommended).</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="step1-account">3. Step 1 — Create your account</h2>\n'
               '\t<ol>\n'
               '\t\t<li>Visit <a href="/signup/?role=seller">/signup/?role=seller</a>.</li>\n'
               '\t\t<li>Enter your business email, mobile number, and choose a password.</li>\n'
               '\t\t<li>Verify the email with the one-time code sent to your inbox.</li>\n'
               '\t\t<li>You\'re logged into the <strong>Seller Center</strong> in "<em>Pending '
               'Verification</em>" state.</li>\n'
               '\t</ol>\n'
               '\n'
               '\t<h2 id="step2-kyc">4. Step 2 — Submit KYC for verification</h2>\n'
               '\t<ol>\n'
               '\t\t<li>From <a href="/seller/">/seller/</a>, tap <strong>Shop Verification '
               '(KYC)</strong>.</li>\n'
               '\t\t<li>Choose your business type (individual / company / partnership).</li>\n'
               '\t\t<li>Upload your NID front + back; enter your NID number exactly as printed.</li>\n'
               '\t\t<li>Upload Trade Licence; enter the licence number.</li>\n'
               '\t\t<li>Upload TIN certificate; enter the TIN.</li>\n'
               '\t\t<li>Enter your full shop address.</li>\n'
               '\t\t<li>Submit.</li>\n'
               '\t</ol>\n'
               '\t<p>\n'
               '\t\tAn SGT Cart admin reviews your submission within <strong>1-2 business days</strong>.\n'
               "\t\tYou'll receive an email when the decision is made.\n"
               '\t</p>\n'
               '\n'
               '\t<h2 id="step3-store">5. Step 3 — Build your store profile</h2>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Shop name (English + Bangla)</strong> — bilingual is strongly '
               'recommended.</li>\n'
               '\t\t<li><strong>Shop slug</strong> — used in the URL <code>/store/your-slug/</code>.</li>\n'
               '\t\t<li><strong>Description</strong> — a 2-3 paragraph introduction.</li>\n'
               '\t\t<li><strong>Logo</strong> — square, transparent PNG looks best.</li>\n'
               '\t\t<li><strong>Banner</strong> — wide cover image for your store page.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="step4-products">6. Step 4 — List your first products</h2>\n'
               '\t<ol>\n'
               '\t\t<li>From the Seller Center, tap <strong>My Products → Create</strong>.</li>\n'
               '\t\t<li>Fill in the title (EN + BN), category, base price, stock, SKU, description.</li>\n'
               '\t\t<li>Upload 1-8 product images. The first one becomes the cover.</li>\n'
               '\t\t<li>Add variants if applicable — colour, size, each with its own price and stock.</li>\n'
               '\t\t<li>Tap <strong>Submit for review</strong>.</li>\n'
               '\t</ol>\n'
               '\n'
               '\t<h2 id="step5-payout">7. Step 5 — Set up payouts &amp; tax</h2>\n'
               '\t<ol>\n'
               '\t\t<li>From the Seller Center, open <strong>Payout Settings</strong>.</li>\n'
               '\t\t<li>Choose your primary payout method (Bank / bKash / Nagad).</li>\n'
               '\t\t<li>Confirm your TIN.</li>\n'
               '\t\t<li>Read and accept the <a href="/seller-terms/">Seller Agreement</a>.</li>\n'
               '\t</ol>',
  'toc': [{'anchor': 'eligibility', 'label': '1. Who can sell on SGT Cart'},
          {'anchor': 'documents', 'label': "2. Documents you'll need"},
          {'anchor': 'step1-account', 'label': '3. Step 1 — Create your account'},
          {'anchor': 'step2-kyc', 'label': '4. Step 2 — Submit KYC for verification'},
          {'anchor': 'step3-store', 'label': '5. Step 3 — Build your store profile'},
          {'anchor': 'step4-products', 'label': '6. Step 4 — List your first products'},
          {'anchor': 'step5-payout', 'label': '7. Step 5 — Set up payouts & tax'}],
  'faq': [{'q': 'How quickly can my shop go live?',
           'a': 'Often the same day. If your KYC documents are clear and complete, admin review takes 1-2 '
                'business days.'},
          {'q': 'Do I need a physical shop?',
           'a': 'No. Home-based sellers, importers, dropshippers and craftspeople all qualify.'},
          {'q': 'Can I sell across multiple categories?',
           'a': 'Yes. There is no category restriction. Many of our top sellers operate in 3-5 categories.'}],
  'related': [{'href': '/seller-terms/',
               'title': 'Seller Agreement',
               'desc': 'The contract that governs your shop.'},
              {'href': '/sell/fees/',
               'title': 'Fees & Commission',
               'desc': 'What SGT Cart charges per delivered sale.'},
              {'href': '/sell/listing-guidelines/',
               'title': 'Listing Guidelines',
               'desc': 'How to write Listings that get approved.'}]},
 {'slug': 'sell/fees',
  'title': 'Seller Fees & Commission',
  'subtitle': 'Exactly what SGT Cart charges sellers — commission by category, payment-processing '
              'pass-through, VAT, optional services.',
  'section': 'Seller Resources',
  'contact_email': 'seller-support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 320,
  'body_html': '<p class="lead small">\n'
               "\t\tSGT Cart's pricing is simple: a flat platform commission per delivered\n"
               '\t\tsale, no monthly subscription, no listing fee. Optional promotional\n'
               '\t\tservices are billed separately and only when you opt in.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="commission">1. Platform commission</h2>\n'
               '\t<p>\n'
               '\t\tCommission is charged <strong>only on delivered Sub-Orders</strong>. Cancelled\n'
               '\t\tor refunded Sub-Orders incur no commission.\n'
               '\t</p>\n'
               '\t<table>\n'
               '\t\t<tr><th>Category</th><th>Commission rate</th></tr>\n'
               '\t\t<tr><td>Default (most categories)</td><td>10.0%</td></tr>\n'
               '\t\t<tr><td>Electronics &amp; mobiles</td><td>8.0%</td></tr>\n'
               '\t\t<tr><td>Books &amp; stationery</td><td>5.0%</td></tr>\n'
               '\t\t<tr><td>Fashion (clothing, shoes, accessories)</td><td>12.0%</td></tr>\n'
               '\t\t<tr><td>Health &amp; beauty</td><td>12.0%</td></tr>\n'
               '\t\t<tr><td>Home &amp; living</td><td>10.0%</td></tr>\n'
               '\t\t<tr><td>Grocery (FMCG)</td><td>6.0%</td></tr>\n'
               '\t\t<tr><td>Watches &amp; jewellery</td><td>8.0%</td></tr>\n'
               '\t\t<tr><td>Toys &amp; baby</td><td>10.0%</td></tr>\n'
               '\t</table>\n'
               '\n'
               '\t<h2 id="payment">2. Payment-processing fees</h2>\n'
               "\t<p>Payment-network fees are <strong>passed through at cost</strong> — SGT Cart doesn't "
               'mark them up:</p>\n'
               '\t<table>\n'
               '\t\t<tr><th>Method</th><th>Fee</th></tr>\n'
               '\t\t<tr><td>SSLCommerz card (Visa / MasterCard / AMEX)</td><td>2.5% of order '
               'amount</td></tr>\n'
               '\t\t<tr><td>bKash</td><td>1.85% of order amount</td></tr>\n'
               '\t\t<tr><td>Nagad</td><td>1.5% of order amount</td></tr>\n'
               '\t\t<tr><td>Cash on Delivery</td><td>Tk 20 flat per Sub-Order</td></tr>\n'
               '\t\t<tr><td>SGT Cart Wallet credit / Reward Points</td><td>0%</td></tr>\n'
               '\t</table>\n'
               '\n'
               '\t<h2 id="promotion">3. Optional promotional services</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Service</th><th>Rate</th></tr>\n'
               '\t\t<tr><td>Sponsored search position</td><td>Tk 3-15 per click (CPC, your bid)</td></tr>\n'
               '\t\t<tr><td>Homepage hero banner</td><td>Tk 5,000 / week (admin-curated)</td></tr>\n'
               '\t\t<tr><td>Homepage strip banner</td><td>Tk 2,500 / week</td></tr>\n'
               '\t\t<tr><td>Flash-sale feature</td><td>Free for the Seller</td></tr>\n'
               '\t</table>\n'
               '\n'
               '\t<h2 id="refund">4. Refunded-order commission reversal</h2>\n'
               '\t<p>\n'
               "\t\tWhen a delivered Sub-Order is refunded later, <strong>SGT Cart's commission is refunded "
               'too</strong>\n'
               '\t\tin proportion to the refund.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="vat">5. VAT collection &amp; deposit</h2>\n'
               '\t<p>\n'
               '\t\tUnder NBR rules for online marketplaces, SGT Cart withholds VAT at\n'
               '\t\tsource on certain category sales (currently 5% for most categories)\n'
               '\t\tand deposits it to NBR.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="worked-example">6. Worked example — a Tk 1,000 sale</h2>\n'
               '\t<p>Customer pays Tk 1,000 (incl. VAT) for a fashion item, by bKash.</p>\n'
               '\t<table>\n'
               '\t\t<tr><td>Gross order amount</td><td><strong>Tk 1,000.00</strong></td></tr>\n'
               '\t\t<tr><td>Item subtotal</td><td>Tk 952.38</td></tr>\n'
               '\t\t<tr><td>VAT portion (5%)</td><td>Tk 47.62</td></tr>\n'
               '\t\t<tr><td>Commission @ 12%</td><td>− Tk 114.29</td></tr>\n'
               '\t\t<tr><td>bKash gateway fee @ 1.85%</td><td>− Tk 18.50</td></tr>\n'
               '\t\t<tr><td>VAT withheld</td><td>− Tk 47.62</td></tr>\n'
               '\t\t<tr><td><strong>Net to your Wallet</strong></td><td><strong>Tk '
               '819.59</strong></td></tr>\n'
               '\t</table>',
  'toc': [{'anchor': 'commission', 'label': '1. Platform commission'},
          {'anchor': 'payment', 'label': '2. Payment-processing fees'},
          {'anchor': 'promotion', 'label': '3. Optional promotional services'},
          {'anchor': 'refund', 'label': '4. Refunded-order commission reversal'},
          {'anchor': 'vat', 'label': '5. VAT collection & deposit'},
          {'anchor': 'worked-example', 'label': '6. Worked example — a Tk 1,000 sale'}],
  'faq': [{'q': 'Is there a monthly subscription fee?',
           'a': 'No. SGT Cart has no monthly subscription, no listing fee, no enrollment fee. You pay only '
                'commission on delivered sales.'},
          {'q': 'Can I negotiate a lower commission?',
           'a': 'High-volume sellers (Tk 5 lakh+ monthly GMV consistently) may negotiate a custom rate via '
                'seller-support@sgtcart.com.'},
          {'q': 'Does SGT Cart deposit my income tax for me?',
           'a': 'We do not withhold income tax — only VAT where the law requires.'}],
  'related': [{'href': '/sell/onboarding/', 'title': 'Onboarding Guide', 'desc': 'How to open your shop.'},
              {'href': '/seller-terms/', 'title': 'Seller Agreement', 'desc': 'Full contractual terms.'},
              {'href': '/sell/payouts/',
               'title': 'Payouts',
               'desc': 'When and how money lands in your account.'}]},
 {'slug': 'sell/listing-guidelines',
  'title': 'Product Listing Guidelines',
  'subtitle': 'What makes a product Listing approvable on SGT Cart — and why common mistakes get rejected.',
  'section': 'Seller Resources',
  'contact_email': 'seller-support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 330,
  'body_html': '<p class="lead small">\n'
               '\t\tA good Listing brings clicks, conversions and repeat customers. A bad\n'
               '\t\tListing gets rejected, wastes time, and hurts your search rank.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="title">1. Title rules</h2>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Length</strong>: 30-90 characters.</li>\n'
               '\t\t<li><strong>Structure</strong>: <em>Brand — Model — Key Spec — Variant</em>.</li>\n'
               '\t\t<li><strong>No keyword stuffing</strong>: Repeating the same word or comma-stuffing '
               'brand names will be rejected.</li>\n'
               '\t\t<li><strong>No brand misuse</strong>: Do not put a famous brand name in your title if '
               'the product is not made by that brand.</li>\n'
               '\t\t<li><strong>No emojis, ALL CAPS, exclamation marks</strong>.</li>\n'
               '\t\t<li><strong>No contact info</strong>: No phone numbers, WhatsApp, Telegram, email '
               'addresses in the title.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="description">2. Description quality</h2>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Original text</strong> — write your own description. Copy-pasting is '
               'rejection-worthy.</li>\n'
               '\t\t<li><strong>Lead with the use case</strong> — who is this for, what problem does it '
               'solve?</li>\n'
               '\t\t<li><strong>List the specifications</strong> — use the structured Spec rows '
               'feature.</li>\n'
               "\t\t<li><strong>Mention what's in the box</strong> — main item + accessories + warranty "
               'card.</li>\n'
               '\t\t<li><strong>Mention warranty / return terms</strong>.</li>\n'
               '\t\t<li><strong>Anti-disintermediation</strong> — no phone numbers, no off-platform '
               'URLs.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="images">3. Image standards</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Rule</th><th>Detail</th></tr>\n'
               '\t\t<tr><td>Resolution</td><td>Minimum 1000×1000 px. Square (1:1) recommended.</td></tr>\n'
               '\t\t<tr><td>Format</td><td>JPG or PNG.</td></tr>\n'
               '\t\t<tr><td>File size</td><td>Each image under 4 MB.</td></tr>\n'
               '\t\t<tr><td>Background</td><td>White or near-white for the cover.</td></tr>\n'
               '\t\t<tr><td>Number</td><td>1-8 images per Listing.</td></tr>\n'
               '\t\t<tr><td>Watermarks</td><td>Do not add your shop logo / phone / URL as a '
               'watermark.</td></tr>\n'
               '\t\t<tr><td>Stolen images</td><td>Only use images you took yourself or have the right to '
               'use.</td></tr>\n'
               '\t</table>\n'
               '\n'
               '\t<h2 id="bilingual">4. Bilingual encouragement</h2>\n'
               '\t<p>\n'
               '\t\tBilingual Listings (Bangla + English) rank visibly higher in search.\n'
               '\t\tThe Seller form has parallel fields (<code>title_en</code> + <code>title_bn</code>); '
               'fill both.\n'
               '\t</p>\n'
               '\n'
               '\t<h2 id="pricing">5. Pricing &amp; MRP rules</h2>\n'
               '\t<ul>\n'
               '\t\t<li><strong>Price in BDT, VAT-inclusive</strong>.</li>\n'
               '\t\t<li><strong>No inflated "MRP"</strong> to fake a discount.</li>\n'
               '\t\t<li><strong>Honour the listed price</strong> for the duration of the Listing.</li>\n'
               '\t\t<li><strong>No bait-and-switch</strong>.</li>\n'
               '\t</ul>\n'
               '\n'
               '\t<h2 id="variants">6. Variants &amp; bulk tiers</h2>\n'
               '\t<p>Variants (size, colour) and bulk-pricing tiers are tools that improve conversion when '
               'used honestly.</p>\n'
               '\n'
               '\t<h2 id="category">7. Category selection</h2>\n'
               '\t<p>Choose the deepest accurate sub-category.</p>\n'
               '\n'
               '\t<h2 id="rejections">8. Common rejections &amp; how to fix them</h2>\n'
               '\t<table>\n'
               '\t\t<tr><th>Rejection reason</th><th>Fix</th></tr>\n'
               '\t\t<tr><td>Description copied from another site</td><td>Rewrite in your own '
               'words.</td></tr>\n'
               '\t\t<tr><td>Images have watermarks or contact info</td><td>Re-export without '
               'watermarks.</td></tr>\n'
               '\t\t<tr><td>Brand name misused</td><td>Replace with a generic descriptor.</td></tr>\n'
               '\t\t<tr><td>Inflated MRP / fake discount</td><td>Set the real prior price as MRP.</td></tr>\n'
               '\t\t<tr><td>Phone number in the description</td><td>Remove.</td></tr>\n'
               '\t</table>',
  'toc': [{'anchor': 'title', 'label': '1. Title rules'},
          {'anchor': 'description', 'label': '2. Description quality'},
          {'anchor': 'images', 'label': '3. Image standards'},
          {'anchor': 'bilingual', 'label': '4. Bilingual encouragement'},
          {'anchor': 'pricing', 'label': '5. Pricing & MRP rules'},
          {'anchor': 'variants', 'label': '6. Variants & bulk tiers'},
          {'anchor': 'category', 'label': '7. Category selection'},
          {'anchor': 'rejections', 'label': '8. Common rejections & how to fix them'}],
  'faq': [{'q': 'How long does Listing review take?',
           'a': 'Typically same day, often within 2-4 hours during business hours.'},
          {'q': 'Can I edit a published Listing without triggering re-review?',
           'a': 'Yes — price, stock, discount-price changes go through immediately.'},
          {'q': "How do I get the 'Verified by SGT' badge on my Listings?",
           'a': 'Submit complete KYC. The badge is awarded automatically to all approved sellers.'}],
  'related': [{'href': '/sell/prohibited-items/',
               'title': 'Prohibited Items',
               'desc': 'What you must never list.'},
              {'href': '/sell/onboarding/',
               'title': 'Onboarding Guide',
               'desc': 'Get your shop live in 30 minutes.'},
              {'href': '/seller-terms/',
               'title': 'Seller Agreement',
               'desc': 'The contract behind these rules.'}]},
 {'slug': 'about',
  'title': 'About SGT Cart',
  'subtitle': None,
  'section': 'Company',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 400,
  'body_html': '<p class="lead">\n'
               '\t<strong>SGT Cart</strong> (legal name: <em>Smart Global Trade Cart</em>)\n'
               '\tis a Bangladesh-first multi-vendor marketplace that connects customers\n'
               '\twith verified local sellers — fashion, electronics, home, beauty,\n'
               '\tgroceries and more, all in one place at\n'
               '\t<a href="https://sgtcart.com">sgtcart.com</a>.\n'
               '</p>\n'
               '\n'
               '<h5 class="ft-bold mt-4">Our mission</h5>\n'
               '<p>\n'
               '\tMake selling online accessible to every small shop in Bangladesh, and give\n'
               '\tcustomers a trustworthy place to discover and buy from them — with bilingual\n'
               '\tsupport, fast delivery, and Cash-on-Delivery from day one.\n'
               '</p>\n'
               '\n'
               '<h5 class="ft-bold mt-4">What sets us apart</h5>\n'
               '<ul>\n'
               '\t<li><strong>Bilingual</strong> — every page works in Bangla and English.</li>\n'
               '\t<li><strong>Verified sellers</strong> — each shop submits trade-licence + NID before going '
               'live.</li>\n'
               '\t<li><strong>Fair ranking</strong> — search results lead with the highest-rated sellers, '
               'not paid placements.</li>\n'
               '\t<li><strong>Flexible payment</strong> — Cash on Delivery, bKash, Nagad and card via '
               'SSLCommerz.</li>\n'
               '\t<li><strong>Real reviews</strong> — only customers who actually received the product can '
               'review it.</li>\n'
               '</ul>\n'
               '\n'
               '<h5 class="ft-bold mt-4">Get in touch</h5>\n'
               '<p>\n'
               '\t<strong>Email:</strong> <a href="mailto:support@sgtcart.com">support@sgtcart.com</a><br>\n'
               '\t<strong>Address:</strong> Mirpur, Dhaka 1216, Bangladesh\n'
               '</p>',
  'toc': [],
  'faq': [],
  'related': []},
 {'slug': 'contact',
  'title': 'Contact Us',
  'subtitle': 'Every way to reach SGT Cart — each with a dedicated team and an SLA so you know when to '
              'expect a reply.',
  'section': 'Company',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 410,
  'body_html': '<p class="lead small">\n'
               '\tSGT Cart is operated by <strong>Smart Global Trade Cart</strong> from\n'
               '\tMirpur, Dhaka 1216, Bangladesh.\n'
               '</p>\n'
               '\n'
               '<h2 id="general">1. General customer support</h2>\n'
               '<table>\n'
               '\t<tr><th>What for</th><th>Channel</th><th>SLA</th></tr>\n'
               '\t<tr><td>Order issues (status, delivery, refund)</td><td>In-app — <a '
               'href="/messages/new">Support chat</a></td><td>Within 4 hours (business days)</td></tr>\n'
               '\t<tr><td>Account / login / password</td><td>Email <a '
               'href="mailto:support@sgtcart.com">support@sgtcart.com</a></td><td>Within 24 hours</td></tr>\n'
               '\t<tr><td>Hotline</td><td>+880-2-XXXXXXX (10:00 – 18:00, Sat-Thu)</td><td>Same '
               'call</td></tr>\n'
               '</table>\n'
               '\n'
               '<h2 id="seller">2. Seller support</h2>\n'
               '<table>\n'
               '\t<tr><th>What for</th><th>Channel</th><th>SLA</th></tr>\n'
               '\t<tr><td>Onboarding questions, KYC issues</td><td>Email <a '
               'href="mailto:seller-support@sgtcart.com">seller-support@sgtcart.com</a></td><td>Within 24 '
               'hours</td></tr>\n'
               '\t<tr><td>Payout discrepancies</td><td>Email <a '
               'href="mailto:seller-support@sgtcart.com">seller-support@sgtcart.com</a></td><td>Within 48 '
               'hours</td></tr>\n'
               '\t<tr><td>Suspension appeals</td><td>Email <a '
               'href="mailto:seller-support@sgtcart.com">seller-support@sgtcart.com</a></td><td>Within 5 '
               'business days</td></tr>\n'
               '</table>\n'
               '\n'
               '<h2 id="legal">3. Legal &amp; compliance</h2>\n'
               '<table>\n'
               '\t<tr><th>What for</th><th>Channel</th></tr>\n'
               '\t<tr><td>Privacy, data-rights requests</td><td><a '
               'href="mailto:privacy@sgtcart.com">privacy@sgtcart.com</a></td></tr>\n'
               '\t<tr><td>Terms-of-service questions</td><td><a '
               'href="mailto:policy@sgtcart.com">policy@sgtcart.com</a></td></tr>\n'
               '\t<tr><td>IP takedown</td><td><a '
               'href="mailto:ip-takedown@sgtcart.com">ip-takedown@sgtcart.com</a></td></tr>\n'
               '\t<tr><td>Dispute escalation</td><td><a '
               'href="mailto:disputes@sgtcart.com">disputes@sgtcart.com</a></td></tr>\n'
               '</table>\n'
               '\n'
               '<h2 id="press">4. Press &amp; partnerships</h2>\n'
               '<table>\n'
               '\t<tr><td>Press / interviews</td><td><a '
               'href="mailto:press@sgtcart.com">press@sgtcart.com</a></td></tr>\n'
               '\t<tr><td>Marketing</td><td><a '
               'href="mailto:partners@sgtcart.com">partners@sgtcart.com</a></td></tr>\n'
               '\t<tr><td>Careers</td><td><a '
               'href="mailto:careers@sgtcart.com">careers@sgtcart.com</a></td></tr>\n'
               '</table>\n'
               '\n'
               '<h2 id="emergency">5. Emergency / fraud reporting</h2>\n'
               '<ul>\n'
               '\t<li><strong>Account takeover:</strong> Email <a '
               'href="mailto:security@sgtcart.com">security@sgtcart.com</a> immediately.</li>\n'
               '\t<li><strong>Counterfeit / dangerous product:</strong> <a '
               'href="mailto:ip-takedown@sgtcart.com">ip-takedown@sgtcart.com</a>.</li>\n'
               '\t<li><strong>Threats, harassment via chat:</strong> Use in-chat "Report" + email <a '
               'href="mailto:trust@sgtcart.com">trust@sgtcart.com</a>.</li>\n'
               '</ul>\n'
               '\n'
               '<h2>Postal address &amp; office</h2>\n'
               '<address class="small">\n'
               '\t<strong>Smart Global Trade Cart</strong> (operating SGT Cart)<br>\n'
               '\tMirpur, Dhaka 1216<br>\n'
               '\tBangladesh<br><br>\n'
               '\tOffice hours: Saturday – Thursday, 10:00 – 18:00.<br>\n'
               '\tClosed on Friday and government holidays.<br><br>\n'
               '\tWebsite: <a href="https://sgtcart.com">sgtcart.com</a><br>\n'
               '\tGeneral email: <a href="mailto:support@sgtcart.com">support@sgtcart.com</a>\n'
               '</address>',
  'toc': [{'anchor': 'general', 'label': '1. General customer support'},
          {'anchor': 'seller', 'label': '2. Seller support'},
          {'anchor': 'legal', 'label': '3. Legal & compliance'},
          {'anchor': 'press', 'label': '4. Press & partnerships'},
          {'anchor': 'emergency', 'label': '5. Emergency / fraud reporting'}],
  'faq': [{'q': 'Why do you have so many email addresses?',
           'a': 'Each address routes to a specific desk so your message reaches the right specialist.'},
          {'q': 'Can I just call you?',
           'a': 'The hotline (+880-2-XXXXXXX) runs Saturday-Thursday 10:00-18:00.'},
          {'q': 'How quickly will I really get a reply?',
           'a': 'Most order-related queries get a first response within 4 business hours during weekdays.'}],
  'related': [{'href': '/help/', 'title': 'Help Center', 'desc': 'Self-serve articles for common questions.'},
              {'href': '/messages/new',
               'title': 'Open Support Chat',
               'desc': 'Real-time chat for order issues.'},
              {'href': '/about/', 'title': 'About SGT Cart', 'desc': 'Who we are.'}]},
 {'slug': 'faq',
  'title': 'Frequently Asked Questions',
  'subtitle': None,
  'section': 'Customer Help',
  'contact_email': 'support@sgtcart.com',
  'version': 'v1.0',
  'sort_order': 420,
  'body_html': '<p class="lead small">\n'
               "\tQuick answers to the questions customers ask most often. Can't find what\n"
               '\tyou need? <a href="/contact/">Contact us</a> and we\'ll get back to you.\n'
               '</p>',
  'toc': [],
  'faq': [{'q': 'How do I place an order?',
           'a': 'Add items to your cart, go to Checkout, choose a delivery address and payment method (Cash '
                'on Delivery or online via SSLCommerz), and place your order. You will receive a '
                'confirmation in your account and via email.'},
          {'q': 'What payment methods are accepted?',
           'a': 'Cash on Delivery is available everywhere. Online payment (card, bKash, Nagad) goes through '
                'SSLCommerz — your card details never touch our servers.'},
          {'q': 'How long does delivery take?',
           'a': 'Most orders inside Dhaka are delivered within 24-48 hours. Outside Dhaka usually takes 2-5 '
                'business days, depending on the seller and the courier.'},
          {'q': 'Can I cancel or return an order?',
           'a': 'Yes — see our Return Policy. You can usually cancel before the seller marks the order as '
                'shipped, and request a return within 7 days of delivery for most items.'},
          {'q': 'How do I become a seller?',
           'a': 'Click "Sell on SGT" in the top menu (or go to /sell/) and register with the Seller tab on '
                'the signup page. Upload your trade licence and NID for verification; an admin will approve '
                'your shop within 1-2 business days.'},
          {'q': 'Do I have to give my phone number to sellers?',
           'a': 'No. Use the in-platform chat for any product questions. Sharing phone numbers in chat is '
                'automatically blocked to keep your information safe.'},
          {'q': 'How are reward points earned and used?',
           'a': 'You earn 1 reward point for every Tk 100 of a delivered order. Each point is worth Tk 1 at '
                'checkout, and you can apply them with a single click on the checkout page.'}],
  'related': [{'href': '/contact/', 'title': 'Contact Us', 'desc': 'Other ways to reach us.'},
              {'href': '/help/', 'title': 'Help Center', 'desc': 'Self-service articles.'}]}]
