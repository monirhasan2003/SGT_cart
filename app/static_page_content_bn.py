"""Bangla translations for the 16 footer pages seeded by
`flask seed-static-pages`. Loaded by the same command when `--lang bn`
or by `flask seed-static-pages-bn`.

Keys must match `slug` values in `static_page_content.FOOTER_PAGES`.
Each value provides Bangla strings for the bilingual columns: title,
subtitle, section, body_html, toc, faq, related.
"""

FOOTER_PAGES_BN = {
    # ----------------------------------------------------------------
    "help": {
        "title": "সাহায্য কেন্দ্র",
        "subtitle": "আপনার SGT Cart অভিজ্ঞতার প্রতিটি বিষয়ে দ্রুত উত্তর ও যোগাযোগের পথ এখানে পাবেন।",
        "section": "Customer Help",
        "toc": [
            {"anchor": "ordering", "label": "Order করা"},
            {"anchor": "payments", "label": "Payments"},
            {"anchor": "delivery", "label": "Delivery"},
            {"anchor": "returns",  "label": "ফেরত ও Refund"},
            {"anchor": "account",  "label": "Account ও নিরাপত্তা"},
        ],
        "body_html": """
<p class="lead small">সবচেয়ে প্রচলিত প্রশ্নগুলো নিচে দেখুন, বা পুরো
self-service library ঘুরে দেখুন। যা খুঁজছেন না পেলে আমাদের team
১ business day-এর মধ্যে Email-এ উত্তর দেয়।</p>

<h2 id="ordering">Order করা</h2>
<ul>
  <li><a href="/help/how-to-order/">কীভাবে order place করবেন</a></li>
  <li><a href="/help/cancellations/">Order বাতিল করা</a></li>
  <li><a href="/shipping/">Delivery সময় ও চার্জ</a></li>
</ul>

<h2 id="payments">Payments</h2>
<ul>
  <li><a href="/help/payment-methods/">গৃহীত payment পদ্ধতি</a></li>
  <li><a href="/help/buyer-protection/">Buyer Protection Program</a></li>
  <li><a href="/refund-policy/">Refund policy</a></li>
</ul>

<h2 id="delivery">Delivery</h2>
<ul>
  <li><a href="/shipping/">Shipping zone ও ETA</a></li>
  <li><a href="/returns/">ফেরতের shipment</a></li>
</ul>

<h2 id="returns">ফেরত ও Refund</h2>
<p>বেশিরভাগ পণ্য delivery-র ৭ দিনের মধ্যে ফেরত দেওয়া যায়।
বিস্তারিত নীতিমালা <a href="/returns/">ফেরত ও Refund</a> পেজে দেখুন।</p>

<h2 id="account">Account ও নিরাপত্তা</h2>
<p>Password ভুলে গেছেন? <a href="/auth/login">Sign-in পেজে</a>
"Password ভুলে গেছেন" link ব্যবহার করুন। অন্য যেকোনো সাহায্যের জন্য
<a href="mailto:support@sgtcart.com">support@sgtcart.com</a>-এ যোগাযোগ করুন।</p>
""",
        "faq": [
            {"q": "আমার order কীভাবে track করব?",
             "a": "Sign in করে <a href='/account/orders/'>আমার Orders</a> খুলুন। প্রতিটি পণ্যের বর্তমান status দেখাবে — Processing, Shipped, বা Delivered।"},
            {"q": "পণ্য ক্ষতিগ্রস্ত অবস্থায় পৌঁছালে কী করব?",
             "a": "Account-এ order খুলে 'Request return' ক্লিক করুন। Courier পণ্য seller-এর কাছে ফেরত পৌঁছানোর ২ business day-র মধ্যে আমরা refund অনুমোদন করি।"},
        ],
        "related": [
            {"href": "/help/how-to-order/", "title": "Order করার নিয়ম",
             "desc": "নতুন buyer-দের জন্য ধাপে ধাপে নির্দেশিকা।"},
            {"href": "/help/payment-methods/", "title": "Payment পদ্ধতি",
             "desc": "Card, COD, mobile wallet, bank transfer।"},
            {"href": "/contact/", "title": "যোগাযোগ করুন",
             "desc": "ফোন, WhatsApp, Email — সব channel।"},
        ],
    },

    # ----------------------------------------------------------------
    "help/how-to-order": {
        "title": "Order করার নিয়ম",
        "subtitle": "Browse থেকে delivery পর্যন্ত — পাঁচ মিনিটের সম্পূর্ণ guide।",
        "section": "Customer Help",
        "toc": [
            {"anchor": "find",     "label": "১. পণ্য খুঁজুন"},
            {"anchor": "cart",     "label": "২. Cart-এ যোগ করুন"},
            {"anchor": "checkout", "label": "৩. Checkout"},
            {"anchor": "pay",      "label": "৪. Pay করুন বা COD বেছে নিন"},
            {"anchor": "track",    "label": "৫. Order track করুন"},
        ],
        "body_html": """
<h2 id="find">১. পণ্য খুঁজুন</h2>
<p>উপরের search bar ব্যবহার করুন, category menu দেখুন, বা homepage
carousel খুলুন। যেকোনো product card-এ ক্লিক করলে পণ্যের ছবি, specs,
seller, reviews ও stock indicator দেখতে পাবেন।</p>

<h2 id="cart">২. Cart-এ যোগ করুন</h2>
<p>প্রয়োজনে variant বেছে নিন (size, রং ইত্যাদি), পরিমাণ ঠিক করুন এবং
<strong>Add to Cart</strong> ক্লিক করুন। আপনি shopping চালিয়ে যেতে
পারেন; উপরের ডান কোণায় cart icon-এ মোট দেখাবে।</p>

<h2 id="checkout">৩. Checkout</h2>
<p>Cart খুলে পণ্যগুলো একবার দেখে নিন এবং
<strong>Proceed to Checkout</strong> ক্লিক করুন। Account না থাকলে
sign in বা signup করতে বলা হবে। Delivery ঠিকানা দিন — আমরা
বাংলাদেশের প্রতিটি জেলায় delivery দিই।</p>

<h2 id="pay">৪. Pay করুন বা Cash on Delivery বেছে নিন</h2>
<p>Checkout পেজে payment পদ্ধতি বেছে নিন। আমরা Visa, Mastercard,
bKash, Nagad, Rocket এবং Cash on Delivery গ্রহণ করি
(<a href="/help/payment-methods/">বিস্তারিত তালিকা</a>)।</p>

<h2 id="track">৫. Order track করুন</h2>
<p>প্রতিটি status পরিবর্তনে Email confirmation ও SMS update পাবেন।
যেকোনো সময়ে <a href="/account/orders/">আমার Orders</a> খুলে live
status দেখতে পারেন।</p>

<blockquote>Tip: <a href="/help/">/help/</a> bookmark করে রাখুন —
সব customer policy ও how-to article সেখান থেকে এক click দূরে।</blockquote>
""",
        "faq": [
            {"q": "Order দিতে কি account দরকার?",
             "a": "হ্যাঁ — account থাকলে আমরা tracking update পাঠাতে পারি ও যেকোনো সমস্যা সমাধান করতে পারি। Sign-up মাত্র ৩০ সেকেন্ডের কাজ।"},
            {"q": "একসাথে বিভিন্ন seller-এর কাছ থেকে পণ্য order করা যায়?",
             "a": "অবশ্যই। প্রতিটি seller তাদের পণ্য আলাদাভাবে ship করবে — প্রতিটি sub-order-এর জন্য আলাদা tracking পাবেন।"},
        ],
        "related": [
            {"href": "/help/payment-methods/", "title": "Payment পদ্ধতি", "desc": "Card, COD, mobile wallet।"},
            {"href": "/help/cancellations/", "title": "Order বাতিল", "desc": "Dispatch-এর আগে ও পরে।"},
            {"href": "/help/buyer-protection/", "title": "Buyer Protection", "desc": "আপনার ক্রয় কীভাবে সুরক্ষিত।"},
        ],
    },

    # ----------------------------------------------------------------
    "sell/payouts": {
        "title": "Seller Payouts",
        "subtitle": "SGT Cart কীভাবে ও কখন আপনার আয় settle করে।",
        "section": "Seller Resources",
        "toc": [
            {"anchor": "cycle",   "label": "Settlement cycle"},
            {"anchor": "methods", "label": "Payout পদ্ধতি"},
            {"anchor": "fees",    "label": "Deduct হওয়া fee"},
            {"anchor": "hold",    "label": "Hold ও reserve"},
            {"anchor": "issues",  "label": "Payout সমস্যা"},
        ],
        "body_html": """
<h2 id="cycle">Settlement cycle</h2>
<p>SGT Cart সাপ্তাহিক <strong>weekly cycle</strong>-এ seller payout
settle করে। যে orders <em>Delivered</em> এবং ৭ দিনের return window
পেরিয়ে গেছে, সেগুলো পরবর্তী সোমবার payout-এর জন্য eligible হয়।
আপনার registered payout account-এ Wednesday end-of-day পর্যন্ত
single transfer হিসেবে fund release হয়।</p>

<h2 id="methods">Payout পদ্ধতি</h2>
<ul>
  <li><strong>Bank transfer (BEFTN)</strong> — বাংলাদেশের যেকোনো licensed bank।</li>
  <li><strong>bKash Merchant</strong> — ৳২৫,০০০-এর কম amount-এ instant।</li>
  <li><strong>Nagad Business</strong> — daily settlement।</li>
</ul>
<p>Admin approval-এর পর <a href="/seller/wallet/">Seller Wallet</a>
পেজে আপনার payout detail যোগ বা update করুন।</p>

<h2 id="fees">Deduct হওয়া fee</h2>
<p>আপনার payout হিসাব করা হয়:</p>
<p><code>(পণ্যের মোট + buyer-এর shipping fee) − category commission −
payment-gateway fee − যেকোনো refund বা chargeback</code></p>
<p>Category অনুযায়ী commission percent <a href="/sell/fees/">Seller Fees
ও Commission</a> পেজে দেখুন।</p>

<h2 id="hold">Hold ও reserve</h2>
<p>নতুন shop-এর প্রথম ৩০ দিন, বা যেকোনো disputed transaction-এর পর
SGT Cart সাপ্তাহিক settlement-এর ১০% পর্যন্ত সাময়িকভাবে reserve
রাখতে পারে — সম্ভাব্য buyer refund cover করতে। বকেয়া সমস্যা সমাধান
হলে reserve automatically release হয়।</p>

<h2 id="issues">Payout সমস্যা</h2>
<p>Payout বিলম্বিত হলে আপনার shop name ও settlement week উল্লেখ করে
<a href="mailto:seller-support@sgtcart.com">seller-support@sgtcart.com</a>-এ
Email করুন। আমরা ১ business day-র মধ্যে উত্তর দিই।</p>
""",
        "faq": [
            {"q": "আমার প্রথম payout কেন delay হচ্ছে?",
             "a": "নতুন seller-রা ১৪ দিনের verification period পার করেন — payout শুরু হয় সেই window শেষ হওয়ার পরের সোমবার থেকে।"},
            {"q": "Payout bank account পরিবর্তন করতে পারি?",
             "a": "হ্যাঁ, তবে fraud protection-এর জন্য নতুন account active হতে ৪৮ ঘণ্টার cool-off প্রযোজ্য।"},
        ],
        "related": [
            {"href": "/sell/fees/", "title": "Fees ও commission", "desc": "Category-wise commission rate।"},
            {"href": "/sell/onboarding/", "title": "Seller onboarding", "desc": "১-২ দিনে আপনার shop খুলুন।"},
            {"href": "/seller-terms/", "title": "Seller Agreement", "desc": "আপনি যে legal framework গ্রহণ করেন।"},
        ],
    },

    # ----------------------------------------------------------------
    "sell/prohibited-items": {
        "title": "নিষিদ্ধ পণ্য",
        "subtitle": "SGT Cart-এ যে ধরনের পণ্য আপনি list করতে পারবেন না।",
        "section": "Seller Resources",
        "toc": [
            {"anchor": "illegal",    "label": "অবৈধ পণ্য"},
            {"anchor": "regulated",  "label": "Regulated items"},
            {"anchor": "restricted", "label": "Restricted categories"},
            {"anchor": "ip",         "label": "IP লঙ্ঘনকারী পণ্য"},
            {"anchor": "enforcement","label": "Enforcement"},
        ],
        "body_html": """
<h2 id="illegal">অবৈধ পণ্য</h2>
<p>SGT Cart-এ কখনো অনুমোদিত নয়:</p>
<ul>
  <li>মাদক, controlled drugs ও drug paraphernalia।</li>
  <li>আগ্নেয়াস্ত্র, গোলাবারুদ, বিস্ফোরক ও replica weapon।</li>
  <li>চোরাই পণ্য, jaali মুদ্রা বা ভুয়া document।</li>
  <li>মানব দেহাবশেষ, body part, বা trafficked wildlife।</li>
  <li>শিশু-যৌনতা বা সন্ত্রাসবাদ-সংক্রান্ত content।</li>
</ul>

<h2 id="regulated">Regulated items</h2>
<p>List করার আগে অবশ্যই
<a href="mailto:policy@sgtcart.com">policy@sgtcart.com</a>-এ যোগাযোগ
করুন — special license প্রয়োজন:</p>
<ul>
  <li>Prescription medicine ও medical device।</li>
  <li>Alcohol ও tobacco।</li>
  <li>Pesticide ও industrial chemical।</li>
  <li>Live animal (শুধু registered breeder/seller)।</li>
</ul>

<h2 id="restricted">Restricted categories</h2>
<ul>
  <li>ব্যবহৃত cosmetics, undergarments বা intimate item।</li>
  <li>ব্যবহৃত child car seat বা infant safety equipment।</li>
  <li>Foreign currency exchange।</li>
  <li>যেকোনো ধরনের adult content।</li>
  <li>Cold-chain shipping প্রয়োজন এমন পণ্য (approved courier ছাড়া)।</li>
</ul>

<h2 id="ip">IP লঙ্ঘনকারী পণ্য</h2>
<p>Counterfeit branded পণ্য, unauthorized replica ও bootleg media
প্রথম detection-এই সরিয়ে ফেলা হয়। বিস্তারিত
<a href="/ip-policy/">Intellectual Property Policy</a>।</p>

<h2 id="enforcement">Enforcement</h2>
<p>লঙ্ঘন হলে: listing সরানো, account-এ strike, এবং repeat বা গুরুতর
অপরাধে — permanent shop closure ও wallet balance buyer refund cover-এ
forfeit। প্রয়োজনে আমরা বাংলাদেশের law enforcement-এর সঙ্গে সহযোগিতা
করি।</p>
""",
        "faq": [
            {"q": "আমি herbal supplement বিক্রি করি — সেগুলো কি অনুমোদিত?",
             "a": "হ্যাঁ, যদি DGDA-registered হয়। List করার আগে seller dashboard-এ registration certificate upload করুন।"},
            {"q": "Second-hand electronics-এর কী হবে?",
             "a": "অনুমোদিত, তবে 'Used / Refurbished' badge অবশ্যই দিতে হবে। Used পণ্যকে new বলে list করা fraud হিসেবে গণ্য।"},
        ],
        "related": [
            {"href": "/ip-policy/", "title": "IP policy", "desc": "Trademark ও copyright takedown।"},
            {"href": "/seller-terms/", "title": "Seller Agreement", "desc": "সম্পূর্ণ legal terms।"},
            {"href": "/sell/code-of-conduct/", "title": "আচরণবিধি", "desc": "Seller-দের জন্য আচরণের মান।"},
        ],
    },

    # ----------------------------------------------------------------
    "sell/seller-protection": {
        "title": "Seller Protection",
        "subtitle": "Chargeback ও bad-faith claim থেকে সৎ seller-দের কীভাবে SGT Cart সুরক্ষা দেয়।",
        "section": "Seller Resources",
        "toc": [
            {"anchor": "what",        "label": "কী সুরক্ষিত"},
            {"anchor": "requirements","label": "Eligibility"},
            {"anchor": "process",     "label": "Claim প্রক্রিয়া"},
            {"anchor": "excluded",    "label": "যা অন্তর্ভুক্ত নয়"},
        ],
        "body_html": """
<h2 id="what">কী সুরক্ষিত</h2>
<p>Buyer dispute করলে এবং আপনি নিচের প্রতিটি ধাপ মানলে, SGT Cart
আপনার পরিবর্তে loss cover করে:</p>
<ul>
  <li>"Item not received" — courier proof-of-delivery file-এ থাকলে।</li>
  <li>"Item significantly not as described" — যেখানে আপনার listing
  (ছবি, specs, dimensions) দাবিটি objectively খণ্ডন করে।</li>
  <li>Cash-on-Delivery package dispatch-এর পর buyer refuse করলে
  (return-leg shipping charge মাসে দু'বার পর্যন্ত waive)।</li>
</ul>

<h2 id="requirements">Eligibility</h2>
<ol>
  <li>Shop <em>Active</em> status-এ থাকতে হবে, কোনো open policy violation নেই।</li>
  <li>Order SGT-approved courier-এ ship হয়েছে (signed POD সংরক্ষিত)।</li>
  <li>Listing delivered পণ্যের সঙ্গে সঠিকভাবে মিলেছে — ছবি, specs, condition।</li>
  <li>Dispute open হওয়ার ২৪ ঘণ্টার মধ্যে আপনি reply করেছেন।</li>
</ol>

<h2 id="process">Claim প্রক্রিয়া</h2>
<p>Dispute automatically <a href="/seller/disputes/">Disputes</a>
tab-এ open হয়। Evidence সহ reply করুন (courier slip, packaging photo,
chat history)। আমাদের team
<a href="/dispute-resolution/">dispute-resolution policy</a> অনুসরণ
করে ৫ business day-র মধ্যে adjudicate করে।</p>

<h2 id="excluded">যা অন্তর্ভুক্ত নয়</h2>
<ul>
  <li>IP infringement বা counterfeit goods-এর জন্য flagged listings।</li>
  <li>তিন বা তার বেশি open policy strike আছে এমন shop।</li>
  <li>SGT-approved courier bypass করে self-shipped order।</li>
  <li>Custom / made-to-order পণ্য — যদি না explicitly insure করা থাকে।</li>
</ul>
""",
        "faq": [
            {"q": "Dispatch-এর পর কতদিন পর্যন্ত protection কাজ করে?",
             "a": "Courier scan-out date থেকে ৩০ দিন, বা delivery-র পর ৭ দিন — যেটি আগে আসে।"},
            {"q": "Enroll-এর জন্য কি পেমেন্ট দিতে হবে?",
             "a": "না। Seller Protection প্রতিটি active SGT Cart shop-এর সঙ্গে অতিরিক্ত খরচ ছাড়াই অন্তর্ভুক্ত।"},
        ],
        "related": [
            {"href": "/dispute-resolution/", "title": "বিরোধ নিষ্পত্তি", "desc": "Buyer-seller conflict adjudication।"},
            {"href": "/sell/code-of-conduct/", "title": "আচরণবিধি", "desc": "Seller আচরণের প্রত্যাশা।"},
            {"href": "/sell/payouts/", "title": "Payouts", "desc": "Win হলে যেভাবে credit হয়।"},
        ],
    },

    # ----------------------------------------------------------------
    "sell/code-of-conduct": {
        "title": "Seller আচরণবিধি",
        "subtitle": "প্রতিটি SGT Cart seller যে professional মান গ্রহণ করেন।",
        "section": "Seller Resources",
        "toc": [
            {"anchor": "honesty",    "label": "Listing-এ সততা"},
            {"anchor": "service",    "label": "Service মান"},
            {"anchor": "behaviour",  "label": "যোগাযোগ"},
            {"anchor": "competition","label": "Fair competition"},
            {"anchor": "consequences","label": "ফলাফল"},
        ],
        "body_html": """
<h2 id="honesty">Listing-এ সততা</h2>
<ul>
  <li>নিজের পণ্যের ছবি বা সঠিক licensing-সহ ছবি ব্যবহার করুন।</li>
  <li>Condition সঠিকভাবে বলুন (new, refurbished, used)।</li>
  <li>Fake discount দেখাতে original price বাড়িয়ে দেখাবেন না।</li>
  <li>সব variant, fee ও lead-time আগে থেকেই উল্লেখ করুন।</li>
</ul>

<h2 id="service">Service মান</h2>
<ul>
  <li>আপনি যে lead-time commit করেছেন তার মধ্যে dispatch করুন
  (সাধারণত ২৪-৪৮ ঘণ্টা)।</li>
  <li>On-time-delivery ৯০%-এর উপরে এবং order-defect rate ২%-এর নিচে রাখুন।</li>
  <li>Buyer chat-এ এক business day-র মধ্যে reply করুন।</li>
  <li>প্রকাশিত return policy harassment ছাড়াই সম্মান করুন।</li>
</ul>

<h2 id="behaviour">যোগাযোগ</h2>
<p>সব communication SGT Cart-এর মধ্যেই হতে হবে। Phone number,
external link share করা, বা off-platform transaction-এ buyer-কে আহ্বান
করা — উভয়ই violation। এটি safety এবং buyer-protection programme
কার্যকর রাখার জন্য।</p>

<h2 id="competition">Fair competition</h2>
<ul>
  <li>নিজের বা প্রতিযোগী listing-এ review manipulate করবেন না।</li>
  <li>Strike বা ban এড়াতে একাধিক shop চালাবেন না।</li>
  <li>নিজের পণ্য bid up করা বা fake-order scheme নিষিদ্ধ।</li>
</ul>

<h2 id="consequences">ফলাফল</h2>
<p>১২ মাসে তিন strike → ৩০ দিন suspension। গুরুতর violation (IP চুরি,
fraud, repeated buyer harassment) → permanent shop closure। Appeal
process আমাদের <a href="/dispute-resolution/">বিরোধ নিষ্পত্তি</a>
পেজে বর্ণিত।</p>
""",
        "related": [
            {"href": "/seller-terms/", "title": "Seller Agreement", "desc": "Binding legal terms।"},
            {"href": "/sell/prohibited-items/", "title": "নিষিদ্ধ পণ্য", "desc": "যা list করা যাবে না।"},
            {"href": "/sell/seller-protection/", "title": "Seller Protection", "desc": "কখন SGT Cart loss absorb করে।"},
        ],
    },

    # ----------------------------------------------------------------
    "accessibility": {
        "title": "Accessibility বিবৃতি",
        "subtitle": "SGT Cart সবাইকে — assistive technology user-সহ — সহজে ব্যবহারযোগ্য রাখার প্রতিশ্রুতি।",
        "section": "Company",
        "toc": [
            {"anchor": "commitment", "label": "আমাদের প্রতিশ্রুতি"},
            {"anchor": "standards",  "label": "যে standards মেনে চলি"},
            {"anchor": "features",   "label": "Accessibility features"},
            {"anchor": "feedback",   "label": "Feedback ও সাহায্য"},
        ],
        "body_html": """
<h2 id="commitment">আমাদের প্রতিশ্রুতি</h2>
<p>SGT Cart এমনভাবে তৈরি ও maintain করা হয় যাতে বাংলাদেশের সবাই —
assistive technology ব্যবহারকারী বা low-bandwidth connection-এর
user-ও — ব্যবহার করতে পারেন। Accessibility আমাদের কাছে একটি ongoing
engineering priority, এক-বারের audit নয়।</p>

<h2 id="standards">যে standards মেনে চলি</h2>
<p>আমরা web storefront ও seller dashboard-এর জন্য <strong>WCAG 2.1
Level AA</strong> target করি। যেখানে কোনো পেজ পিছিয়ে আছে, সেখানে
user impact অনুযায়ী fix priority দিই।</p>

<h2 id="features">Accessibility features</h2>
<ul>
  <li>প্রতিটি interactive control-এ keyboard navigation।</li>
  <li>Link, button ও form field-এ visible focus indicator।</li>
  <li>Product photo-তে alt-text (seller-দের কাছেও আমরা সেটি চাই)।</li>
  <li>Body copy ও primary action-এ পর্যাপ্ত colour contrast।</li>
  <li>প্রতিটি পেজে বাংলা ও English language toggle।</li>
  <li>৩২০px wide পর্যন্ত reflow করে mobile-first responsive layout।</li>
</ul>

<h2 id="feedback">Feedback ও সাহায্য</h2>
<p>কোনো পেজে barrier পেলে পেজের URL ও যে সমস্যা হয়েছে তা উল্লেখ করে
<a href="mailto:accessibility@sgtcart.com">accessibility@sgtcart.com</a>-এ
Email করুন। আমরা ২ business day-র মধ্যে acknowledge করি ও use blocking
issue-গুলো ৩০ দিনের মধ্যে fix-এর target রাখি।</p>
""",
        "related": [
            {"href": "/contact/", "title": "যোগাযোগ করুন", "desc": "সব support channel।"},
            {"href": "/privacy/", "title": "Privacy", "desc": "আপনার data কীভাবে handle করা হয়।"},
            {"href": "/help/", "title": "সাহায্য কেন্দ্র", "desc": "Self-service article।"},
        ],
    },

    # ----------------------------------------------------------------
    "governing-law": {
        "title": "প্রযোজ্য আইন ও Jurisdiction",
        "subtitle": "SGT Cart-সম্পর্কিত বিরোধে কোন আইন প্রযোজ্য।",
        "section": "Legal",
        "toc": [
            {"anchor": "law",      "label": "প্রযোজ্য আইন"},
            {"anchor": "venue",    "label": "Exclusive venue"},
            {"anchor": "currency", "label": "Currency"},
            {"anchor": "consumer", "label": "Consumer অধিকার"},
        ],
        "body_html": """
<h2 id="law">প্রযোজ্য আইন</h2>
<p>SGT Cart-এ সমস্ত transaction এবং buyer, seller ও SGT Cart-এর
মধ্যকার সম্পর্ক <strong>গণপ্রজাতন্ত্রী বাংলাদেশের</strong> আইন
দ্বারা পরিচালিত — কোনো conflict-of-law নীতি বিবেচনা না করেই।</p>

<h2 id="venue">Exclusive venue</h2>
<p>আমাদের <a href="/dispute-resolution/">বিরোধ নিষ্পত্তি</a> পেজে
উল্লিখিত binding arbitration clause-এর সাপেক্ষে, SGT Cart সংক্রান্ত
যেকোনো court proceeding শুধুমাত্র <strong>ঢাকা, বাংলাদেশের</strong>
সক্ষম আদালতে আনতে হবে। উভয় পক্ষ সেখানে personal jurisdiction
স্বীকার করে।</p>

<h2 id="currency">Currency</h2>
<p>SGT Cart-এর সমস্ত price, fee ও settlement
<strong>বাংলাদেশি টাকা (BDT, ৳)</strong>-তে denominate। আমরা বর্তমানে
multi-currency pricing বা international settlement প্রস্তাব করি না।</p>

<h2 id="consumer">Consumer অধিকার</h2>
<p>আমাদের কোনো terms-ই বাংলাদেশ Consumer Rights Protection Act, 2009
বা তার successor legislation-এর অধীনে আপনার non-waivable statutory
অধিকার সীমিত করে না।</p>
""",
        "related": [
            {"href": "/terms/", "title": "Customer Terms", "desc": "Buyer-side contract।"},
            {"href": "/seller-terms/", "title": "Seller Agreement", "desc": "Seller-side contract।"},
            {"href": "/dispute-resolution/", "title": "বিরোধ নিষ্পত্তি", "desc": "Arbitration framework।"},
        ],
    },

    # ----------------------------------------------------------------
    "careers": {
        "title": "SGT Cart-এ ক্যারিয়ার",
        "subtitle": "বাংলাদেশের সবচেয়ে নির্ভরযোগ্য marketplace গড়তে আমাদের সঙ্গে যোগ দিন।",
        "section": "Company",
        "toc": [
            {"anchor": "why",      "label": "কেন SGT Cart"},
            {"anchor": "openings", "label": "বর্তমান openings"},
            {"anchor": "apply",    "label": "কীভাবে apply করবেন"},
            {"anchor": "internships","label": "Internships"},
        ],
        "body_html": """
<h2 id="why">কেন SGT Cart</h2>
<p>SGT Cart Smart Global Trade group-এর অংশ — একটি বাংলাদেশি
technology group যা আমাদের home market-এ online commerce-এর digital
backbone গড়ে তুলছে। আমরা ছোট, senior একটি team — যেখানে
craftsmanship, fast iteration ও outcome ownership-এর গুরুত্ব দেওয়া
হয়।</p>

<h2 id="openings">বর্তমান openings</h2>
<p>নিচের function-গুলোতে আমরা ধারাবাহিকভাবে hire করি। নির্দিষ্ট role
list-এ না থাকলেও strong CV পাঠান — ভালো application আমরা file-এ
রাখি।</p>
<ul>
  <li><strong>Engineering</strong> — Python / Flask, Flutter (mobile), DevOps।</li>
  <li><strong>Operations</strong> — Seller success, logistics, courier coordination।</li>
  <li><strong>Customer support</strong> — Bilingual (বাংলা + English) chat ও voice।</li>
  <li><strong>Trust ও Safety</strong> — Policy enforcement ও dispute analyst।</li>
  <li><strong>Marketing</strong> — Performance, content ও brand।</li>
</ul>

<h2 id="apply">কীভাবে apply করবেন</h2>
<p>আপনার CV, কী কাজে দক্ষ তার সংক্ষিপ্ত note, ও আপনি গর্ববোধ করেন
এমন কিছু link-সহ
<a href="mailto:careers@sgtcart.com">careers@sgtcart.com</a>-এ Email
করুন। আমরা প্রতিটি Email-এর উত্তর দিই — সাধারণত ৫ business day-র
মধ্যে।</p>

<h2 id="internships">Internships</h2>
<p>বাংলাদেশি বিশ্ববিদ্যালয়ের final-year undergraduate-রা আমাদের ৩-মাসের
paid internship-এ (engineering ও operations) apply করতে পারেন। Subject
line-এ <em>"Internship"</em> লিখুন।</p>
""",
        "related": [
            {"href": "/about/", "title": "আমাদের সম্পর্কে", "desc": "Mission ও founder।"},
            {"href": "/newsroom/", "title": "Newsroom", "desc": "সর্বশেষ ঘোষণা।"},
            {"href": "/contact/", "title": "যোগাযোগ", "desc": "আমাদের কাছে পৌঁছানোর অন্য উপায়।"},
        ],
    },

    # ----------------------------------------------------------------
    "newsroom": {
        "title": "Newsroom",
        "subtitle": "Press release, milestone ও media resource।",
        "section": "Company",
        "toc": [
            {"anchor": "press",    "label": "Press release"},
            {"anchor": "kit",      "label": "Media kit"},
            {"anchor": "contact",  "label": "Press contact"},
        ],
        "body_html": """
<h2 id="press">Press release</h2>
<p>আমরা formal ঘোষণা publish করি যখন বড় company milestone হয় —
funding round, regulatory approval, seller-count record, নতুন product
launch। Newsroom RSS feed-এ subscribe করুন বা আমাদের distribution
list-এ যুক্ত হতে
<a href="mailto:press@sgtcart.com">press@sgtcart.com</a>-এ Email করুন।</p>

<p><em>এখনো কোনো public release নেই — site-এর এই version-এর সঙ্গেই
আমরা launch করছি। Update-এর জন্য এখানে দেখুন।</em></p>

<h2 id="kit">Media kit</h2>
<p>আমাদের logo, brand colour বা executive photography দরকার?
<a href="mailto:press@sgtcart.com">press@sgtcart.com</a>-এ Email করুন,
asset bundle (PNG/SVG logo, brand-style PDF, high-resolution photo)
share করব।</p>

<h2 id="contact">Press contact</h2>
<p>Interview, podcast guest বা off-the-record briefing-এর জন্য
<strong>SGT Cart Communications</strong>-এ
<a href="mailto:press@sgtcart.com">press@sgtcart.com</a>-এ যোগাযোগ
করুন। Journalist-দের আমরা weekday-এ ২৪ ঘণ্টার মধ্যে reply করি।</p>
""",
        "related": [
            {"href": "/about/", "title": "আমাদের সম্পর্কে", "desc": "Company background।"},
            {"href": "/careers/", "title": "ক্যারিয়ার", "desc": "Team-এ যোগ দিন।"},
            {"href": "/sustainability/", "title": "টেকসইতা", "desc": "পরিবেশগত প্রতিশ্রুতি।"},
        ],
    },

    # ----------------------------------------------------------------
    "sustainability": {
        "title": "টেকসইতা",
        "subtitle": "Marketplace গড়া যা পৃথিবীর জন্য ক্ষতিকর নয়।",
        "section": "Company",
        "toc": [
            {"anchor": "packaging", "label": "Packaging"},
            {"anchor": "logistics", "label": "Logistics"},
            {"anchor": "supply",    "label": "Supply chain"},
            {"anchor": "future",    "label": "ভবিষ্যৎ পরিকল্পনা"},
        ],
        "body_html": """
<h2 id="packaging">Packaging</h2>
<p>আমরা courier partner-দের সঙ্গে single-use plastic mailer ছেড়ে
recycled-paper alternative-এ যাওয়ার কাজ করছি। আমাদের <em>Green Pack</em>
programme-এ যোগ দেওয়া seller-রা subsidised compostable packaging
এবং তাদের listing-এ "Green Pack" badge পান।</p>

<h2 id="logistics">Logistics</h2>
<p>যেখানে সম্ভব আমরা একই জেলামুখী order একত্রে consolidated run-এ
ship করি। ঢাকার ভেতরে আমরা দুটি courier partner-এর সঙ্গে short-distance
last-mile delivery-র জন্য electric two-wheeler pilot করছি।</p>

<h2 id="supply">Supply chain</h2>
<p>উচ্চ environmental risk আছে এমন পণ্যের জন্য platform support
আমরা সক্রিয়ভাবে কমাচ্ছি — single-use vape kit, microplastic-যুক্ত
glitter craft kit, এবং disposable thin-film fashion item। এসব
category-র seller-দের আমরা refillable বা higher-quality alternative
দেওয়ার জন্য উৎসাহিত করি।</p>

<h2 id="future">ভবিষ্যৎ পরিকল্পনা</h2>
<p>২০২৮ সালের মধ্যে আমাদের লক্ষ্য:</p>
<ul>
  <li>SGT Cart-পরিচালিত সব warehouse-এ rooftop solar (target: ৬০%
  on-site generation)।</li>
  <li>আমাদের top ১০ courier ও warehousing partner-এর সঙ্গে co-signed
  বার্ষিক sustainability report publish।</li>
  <li>প্রতিটি order-এ default হিসেবে carbon-neutral checkout।</li>
</ul>
<p>এটি একটি honest "in-progress" পেজ — আমরা greenwash করব না।
Real number হাতে এলে এখানে publish করব।</p>
""",
        "related": [
            {"href": "/about/", "title": "আমাদের সম্পর্কে", "desc": "Company background।"},
            {"href": "/trust-safety/", "title": "Trust ও Safety", "desc": "Marketplace integrity।"},
            {"href": "/transparency/", "title": "স্বচ্ছতা", "desc": "Reporting commitment।"},
        ],
    },

    # ----------------------------------------------------------------
    "trust-safety": {
        "title": "Trust ও Safety",
        "subtitle": "Buyer, seller ও platform-কে আমরা কীভাবে নিরাপদ রাখি।",
        "section": "Trust & Safety",
        "toc": [
            {"anchor": "pillars",     "label": "চারটি ভিত্তি"},
            {"anchor": "moderation",  "label": "Content moderation"},
            {"anchor": "fraud",       "label": "Fraud prevention"},
            {"anchor": "report",      "label": "Concern রিপোর্ট করুন"},
        ],
        "body_html": """
<h2 id="pillars">চারটি ভিত্তি</h2>
<ol>
  <li><strong>Genuine seller।</strong> প্রকাশের আগে প্রতিটি shop
  verified — National ID, trade license ও bank account check।</li>
  <li><strong>সৎ listing।</strong> Automated check + high-risk
  category-তে human review, এবং counterfeit goods-এর instant takedown।</li>
  <li><strong>Safe transaction।</strong> Encrypted payment, escrowed
  COD reconciliation, ৭ দিনের return window।</li>
  <li><strong>Respectful community।</strong> Review, Q&amp;A ও chat সবই
  আমাদের <a href="/sell/code-of-conduct/">আচরণবিধি</a>-র সঙ্গে
  সামঞ্জস্যপূর্ণ।</li>
</ol>

<h2 id="moderation">Content moderation</h2>
<p>আমরা ML classifier, keyword filter ও human review একত্রে ব্যবহার
করি। নিষিদ্ধ পণ্যের flag করা listing ৪ ঘণ্টার মধ্যে offline করা হয়;
appeal ৪৮ ঘণ্টায় review করা হয়।</p>

<h2 id="fraud">Fraud prevention</h2>
<p>SGT Cart-এর risk engine সন্দেহজনক payment pattern, repeat-chargeback
buyer ও wash-trading-এর মতো seller activity-র দিকে নজর রাখে।
সিদ্ধান্ত explainable — buyer ও seller উভয়েই restriction-এর কারণ
জানতে পারেন।</p>

<h2 id="report">Concern রিপোর্ট করুন</h2>
<p>কিছু দেখেছেন? <a href="/report-illegal/">/report-illegal/</a>-এ
দ্রুত report ফাইল করুন বা
<a href="mailto:trust@sgtcart.com">trust@sgtcart.com</a>-এ Email
করুন। Critical safety report ১ ঘণ্টার মধ্যে triage হয়।</p>
""",
        "related": [
            {"href": "/transparency/", "title": "স্বচ্ছতা", "desc": "Report ও disclosure।"},
            {"href": "/anti-counterfeit/", "title": "নকল পণ্য প্রতিরোধ", "desc": "Brand protection programme।"},
            {"href": "/report-illegal/", "title": "অবৈধ content রিপোর্ট", "desc": "Safety report খুলুন।"},
        ],
    },

    # ----------------------------------------------------------------
    "transparency": {
        "title": "স্বচ্ছতা",
        "subtitle": "বার্ষিক disclosure, take-down statistics ও government request log।",
        "section": "Trust & Safety",
        "toc": [
            {"anchor": "principle",  "label": "আমাদের নীতি"},
            {"anchor": "takedowns",  "label": "Take-down reporting"},
            {"anchor": "requests",   "label": "Government request"},
            {"anchor": "data",       "label": "Data access log"},
        ],
        "body_html": """
<h2 id="principle">আমাদের নীতি</h2>
<p>SGT Cart একটি তরুণ company, কিন্তু আমরা প্রতিষ্ঠিত global
marketplace-এর সমান transparency standard publicly commit করছি:</p>
<ul>
  <li>বার্ষিক transparency report (প্রথম edition Q1 2027-এ আসবে)।</li>
  <li>প্রাপ্ত প্রতিটি government / law-enforcement request-এর aggregate
  disclosure।</li>
  <li>Platform decision-এ ক্ষতিগ্রস্ত যেকোনো seller বা buyer-এর জন্য
  স্পষ্ট appeal path।</li>
</ul>

<h2 id="takedowns">Take-down reporting</h2>
<p>আমরা ত্রৈমাসিক number publish করি:</p>
<ul>
  <li>IP infringement-এর জন্য সরানো listing (reporter type অনুযায়ী)।</li>
  <li>Fraud, harassment বা নিষিদ্ধ পণ্যের জন্য suspended account।</li>
  <li>Fake-review rule লঙ্ঘনের জন্য সরানো review।</li>
</ul>
<p>প্রথম quarter-এর reportable data <strong>এপ্রিল-জুন ২০২৬</strong>
cover করে এবং ১ আগস্ট ২০২৬-এর মধ্যে এখানে প্রকাশিত হবে।</p>

<h2 id="requests">Government request</h2>
<p>SGT Cart বৈধ warrant বা court order পেলে বাংলাদেশের law enforcement-এর
সঙ্গে সহযোগিতা করে। Disclosure আইনত প্রয়োজনীয় সর্বনিম্ন data-তে
সীমাবদ্ধ রাখি, অনুমোদিত হলে user-কে জানাই, এবং বার্ষিক report-এর
জন্য প্রতিটি request log করি।</p>

<h2 id="data">Data access log</h2>
<p>User data-এর internal access ক্ষুদ্রতম সম্ভাব্য team-এ সীমিত এবং
review-এর জন্য logged। Log ত্রৈমাসিকভাবে স্বাধীন reviewer দ্বারা
audit হয়।</p>
""",
        "related": [
            {"href": "/trust-safety/", "title": "Trust ও Safety", "desc": "Marketplace integrity overview।"},
            {"href": "/privacy/", "title": "Privacy Policy", "desc": "আপনার data কীভাবে ব্যবহৃত হয়।"},
            {"href": "/governing-law/", "title": "প্রযোজ্য আইন", "desc": "Applicable jurisdiction।"},
        ],
    },

    # ----------------------------------------------------------------
    "report-illegal": {
        "title": "অবৈধ content রিপোর্ট",
        "subtitle": "SGT Cart-কে আইন লঙ্ঘনকারী listing, content বা আচরণ সম্পর্কে কীভাবে জানাবেন।",
        "section": "Trust & Safety",
        "toc": [
            {"anchor": "what",     "label": "কী illegal বলে গণ্য"},
            {"anchor": "how",      "label": "কীভাবে রিপোর্ট করবেন"},
            {"anchor": "anonymous","label": "Anonymous tip"},
            {"anchor": "emergency","label": "জরুরি"},
        ],
        "body_html": """
<h2 id="what">কী illegal বলে গণ্য</h2>
<p>কোনো listing, review, message বা seller নিচের কিছু সম্পর্কিত মনে
হলে অনুগ্রহ করে রিপোর্ট করুন:</p>
<ul>
  <li>Counterfeit branded goods বা pirated digital content।</li>
  <li>অস্ত্র, গোলাবারুদ, বিস্ফোরক বা related parts।</li>
  <li>Drug (recreational, controlled বা unlicensed prescription)।</li>
  <li>Child sexual abuse material বা grooming behaviour।</li>
  <li>Trafficked goods (wildlife, antique, চোরাই গাড়ি ইত্যাদি)।</li>
  <li>Terrorism financing বা extremist content।</li>
  <li>হুমকি, harassment বা doxxing।</li>
</ul>

<h2 id="how">কীভাবে রিপোর্ট করবেন</h2>
<ol>
  <li>URL, screenshot ও সংক্ষিপ্ত বিবরণ-সহ
  <a href="mailto:trust@sgtcart.com">trust@sgtcart.com</a>-এ Email
  করুন।</li>
  <li>আপনি rights-holder হলে IP infringement রিপোর্টের জন্য
  <a href="/ip-policy/">IP Policy</a>-র notice format অনুসরণ করুন।</li>
  <li>আমরা Severity-1 report ৪ ঘণ্টায় acknowledge ও ২৪ ঘণ্টায় action নিই।</li>
</ol>

<h2 id="anonymous">Anonymous tip</h2>
<p>Anonymous report গ্রহণযোগ্য, তবে তদন্তের জন্য যথেষ্ট detail দিন
(screenshot, URL, তারিখ)। আপনি contact information না দিলে আমরা
follow-up করতে পারব না।</p>

<h2 id="emergency">জরুরি</h2>
<p>কেউ immediate physical danger-এ আছেন মনে হলে প্রথমে বাংলাদেশ
emergency service-এ <strong>৯৯৯</strong>-এ যোগাযোগ করুন, তারপর
আমাদের জানান।</p>
""",
        "related": [
            {"href": "/trust-safety/", "title": "Trust ও Safety", "desc": "Marketplace নিরাপত্তা।"},
            {"href": "/anti-counterfeit/", "title": "নকল পণ্য প্রতিরোধ", "desc": "Brand protection।"},
            {"href": "/ip-policy/", "title": "IP Policy", "desc": "Trademark ও copyright প্রক্রিয়া।"},
        ],
    },

    # ----------------------------------------------------------------
    "anti-counterfeit": {
        "title": "নকল পণ্য প্রতিরোধ programme",
        "subtitle": "Brand owner-রা SGT Cart-এ তাদের IP কীভাবে সুরক্ষিত রাখেন।",
        "section": "Trust & Safety",
        "toc": [
            {"anchor": "commitment", "label": "আমাদের প্রতিশ্রুতি"},
            {"anchor": "enrol",      "label": "Brand enrolment"},
            {"anchor": "process",    "label": "Take-down প্রক্রিয়া"},
            {"anchor": "penalties",  "label": "Seller penalty"},
        ],
        "body_html": """
<h2 id="commitment">আমাদের প্রতিশ্রুতি</h2>
<p>SGT Cart counterfeit listing সহ্য করে না। Verified brand owner-রা
আমাদের Anti-Counterfeit Programme-এ register করে expedited takedown,
proactive listing screening ও direct account manager পেতে পারেন।</p>

<h2 id="enrol">Brand enrolment</h2>
<p>Enroll করতে নিচেরগুলো
<a href="mailto:brand-protect@sgtcart.com">brand-protect@sgtcart.com</a>-এ
পাঠান:</p>
<ul>
  <li>Registered trademark certificate (বাংলাদেশ বা international,
  WIPO designation-সহ)।</li>
  <li>Brand-এর পক্ষে কাজ করার অনুমোদনের proof।</li>
  <li>একজন primary contact ও authorised escalation list।</li>
</ul>
<p>আমরা ৫ business day-র মধ্যে enrolment confirm করি।</p>

<h2 id="process">Take-down প্রক্রিয়া</h2>
<ol>
  <li>Enrolled brand-রা brand portal-এর মাধ্যমে (বা portal launch
  পর্যন্ত Email-এ) takedown request file করেন।</li>
  <li>Enrolled brand-এর request আমরা <strong>২৪ ঘণ্টায়</strong>,
  non-enrolled rights-holder-এর <strong>৭২ ঘণ্টায়</strong> action নিই।</li>
  <li>Seller documented authenticity evidence (invoice, distributor
  agreement) সহ ১৪ দিনের মধ্যে appeal করতে পারেন।</li>
</ol>

<h2 id="penalties">Seller penalty</h2>
<ul>
  <li><strong>First strike</strong> — listing সরানো, written warning।</li>
  <li><strong>Second strike</strong> — ৩০ দিন suspension, wallet hold।</li>
  <li><strong>Third strike</strong> — permanent shop closure; বকেয়া
  balance buyer refund-এর জন্য reserve।</li>
</ul>
""",
        "related": [
            {"href": "/ip-policy/", "title": "IP Policy", "desc": "সম্পূর্ণ takedown প্রক্রিয়া।"},
            {"href": "/trust-safety/", "title": "Trust ও Safety", "desc": "Marketplace integrity programme।"},
            {"href": "/sell/code-of-conduct/", "title": "Seller আচরণবিধি", "desc": "আচরণের মান।"},
        ],
    },

    # ----------------------------------------------------------------
    "security": {
        "title": "নিরাপত্তা",
        "subtitle": "SGT Cart কীভাবে account, payment ও platform data সুরক্ষিত রাখে।",
        "section": "Trust & Safety",
        "toc": [
            {"anchor": "account",  "label": "Account নিরাপত্তা"},
            {"anchor": "payments", "label": "Payment নিরাপত্তা"},
            {"anchor": "platform", "label": "Platform নিরাপত্তা"},
            {"anchor": "report",   "label": "Vulnerability রিপোর্ট"},
        ],
        "body_html": """
<h2 id="account">Account নিরাপত্তা</h2>
<ul>
  <li>Password industry-standard work-factor algorithm-এ hash করা হয়
  — আমরা কখনো plain text-এ store করি না।</li>
  <li>Sensitive action (payout detail পরিবর্তন, data export) করতে
  registered Email-এ পাঠানো one-time code লাগে।</li>
  <li>Inactivity-র পর session auto-expire হয়, এবং remote session-গুলো
  account পেজ থেকে sign-out করা যায়।</li>
</ul>

<h2 id="payments">Payment নিরাপত্তা</h2>
<ul>
  <li>Card payment PCI-DSS-compliant gateway (SSLCommerz)-এ process
  হয়। SGT Cart কখনো raw card number store করে না।</li>
  <li>সমস্ত payment-page traffic end-to-end TLS-encrypted।</li>
  <li>সন্দেহজনক payment pattern fund release-এর আগে automated
  review trigger করে।</li>
</ul>

<h2 id="platform">Platform নিরাপত্তা</h2>
<ul>
  <li>Production server reverse proxy-র পেছনে HSTS, modern TLS ও
  rate-limited public endpoint দিয়ে isolated।</li>
  <li>Internal access least-privilege, MFA-enforced, এবং logged।</li>
  <li>Backup encrypted at rest এবং restorability নিয়মিত test করা হয়।</li>
</ul>

<h2 id="report">Vulnerability রিপোর্ট</h2>
<p>Security researcher-রা, proof-of-concept ও আপনার contact
detail-সহ <a href="mailto:security@sgtcart.com">security@sgtcart.com</a>-এ
Email করুন। আমাদের commitment:</p>
<ul>
  <li>২ business day-র মধ্যে acknowledgement।</li>
  <li>Other user-দের impact না করা good-faith research-এর জন্য
  safe-harbour।</li>
  <li>Fix ship হওয়ার পর আপনার পছন্দ অনুযায়ী public credit।</li>
</ul>
""",
        "related": [
            {"href": "/privacy/", "title": "Privacy", "desc": "আপনার data কীভাবে handle হয়।"},
            {"href": "/trust-safety/", "title": "Trust ও Safety", "desc": "Marketplace integrity।"},
            {"href": "/transparency/", "title": "স্বচ্ছতা", "desc": "Reporting commitment।"},
        ],
    },
}
