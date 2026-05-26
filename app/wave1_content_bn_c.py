# -*- coding: utf-8 -*-
"""
Bangla translations for Wave 1 Group C (Seller Resources) pages.

Slugs covered:
    - sell                       (Sell on SGT Cart)
    - sell/onboarding            (Seller Onboarding Guide)
    - sell/fees                  (Seller Fees & Commission)
    - sell/listing-guidelines    (Product Listing Guidelines)

Style: "আপনি" tone, professional/business-oriented, common UI/business terms
kept as Bangla transliteration. HTML structure, anchor IDs, hrefs, class
attributes, code/URL/email, and numeric values for amounts/percentages/sizes
are preserved exactly. Bangla digits are used only for section numbering.
"""

WAVE1_BN_C = {
    "sell": {
        "title_bn": "SGT Cart-এ বিক্রি করুন",
        "subtitle_bn": (
            "SGT Cart-এ আপনার শপ খুলুন এবং সারা বাংলাদেশের কাস্টমারদের কাছে "
            "বিক্রি শুরু করুন — বাইলিঙ্গুয়াল স্টোরফ্রন্ট, মাল্টি-পেমেন্ট চেকআউট, "
            "বায়ারদের সঙ্গে রিয়েল-টাইম চ্যাট, এবং মোবাইল-ফ্রেন্ডলি সেলার ড্যাশবোর্ড।"
        ),
        "section_bn": "সেলার রিসোর্স",
        "body_html_bn": """<p class="lead">
		SGT Cart-এ আপনার শপ খুলুন এবং সারা বাংলাদেশের কাস্টমারদের কাছে
		বিক্রি শুরু করুন — বাইলিঙ্গুয়াল স্টোরফ্রন্ট, মাল্টি-পেমেন্ট চেকআউট,
		বায়ারদের সঙ্গে রিয়েল-টাইম চ্যাট, এবং মোবাইল-ফ্রেন্ডলি সেলার ড্যাশবোর্ড।
	</p>

	<div class="row g-2 mt-3">
		<div class="col-lg-4 col-md-6">
			<div class="border rounded p-2 d-flex gap-2 align-items-start">
				<i class="lni lni-checkmark-circle fs-5 theme-cl mt-1"></i>
				<div>
					<h6 class="ft-bold mb-1 small">সহজ সেটআপ</h6>
					<p class="text-muted small mb-0">
						সাইনআপ করুন, ট্রেড লাইসেন্স + NID আপলোড করুন, অ্যাডমিন
						1-2 দিনে অ্যাপ্রুভ করবে। স্টোর সঙ্গে সঙ্গেই লাইভ হয়ে যাবে।
					</p>
				</div>
			</div>
		</div>
		<div class="col-lg-4 col-md-6">
			<div class="border rounded p-2 d-flex gap-2 align-items-start">
				<i class="lni lni-wallet fs-5 theme-cl mt-1"></i>
				<div>
					<h6 class="ft-bold mb-1 small">যৌক্তিক কমিশন</h6>
					<p class="text-muted small mb-0">
						প্রতি ডেলিভার হওয়া সেলে অল্প একটি প্ল্যাটফর্ম কমিশন — কোনো
						মাসিক ফি বা লিস্টিং ফি নেই।
					</p>
				</div>
			</div>
		</div>
		<div class="col-lg-4 col-md-6">
			<div class="border rounded p-2 d-flex gap-2 align-items-start">
				<i class="lni lni-bar-chart fs-5 theme-cl mt-1"></i>
				<div>
					<h6 class="ft-bold mb-1 small">পূর্ণাঙ্গ এনালিটিক্স</h6>
					<p class="text-muted small mb-0">
						সেলস ড্যাশবোর্ড, টপ প্রোডাক্ট, রেভিনিউ, রিভিউ,
						লো-স্টক অ্যালার্ট — সবই বিল্ট-ইন।
					</p>
				</div>
			</div>
		</div>
		<div class="col-lg-4 col-md-6">
			<div class="border rounded p-2 d-flex gap-2 align-items-start">
				<i class="lni lni-tag fs-5 theme-cl mt-1"></i>
				<div>
					<h6 class="ft-bold mb-1 small">নিজস্ব প্রমোশন</h6>
					<p class="text-muted small mb-0">
						নিজের প্রোডাক্টে স্টোর কুপন তৈরি করুন, ডিসকাউন্ট প্রাইস
						সেট করুন এবং ফ্ল্যাশ সেল চালান।
					</p>
				</div>
			</div>
		</div>
		<div class="col-lg-4 col-md-6">
			<div class="border rounded p-2 d-flex gap-2 align-items-start">
				<i class="lni lni-comments fs-5 theme-cl mt-1"></i>
				<div>
					<h6 class="ft-bold mb-1 small">ডাইরেক্ট চ্যাট</h6>
					<p class="text-muted small mb-0">
						প্রোডাক্ট সংক্রান্ত প্রশ্নের লাইভ উত্তর দিন; ডেলিভারি / রিফান্ড
						ইস্যু চলে যাবে SGT Support-এ।
					</p>
				</div>
			</div>
		</div>
		<div class="col-lg-4 col-md-6">
			<div class="border rounded p-2 d-flex gap-2 align-items-start">
				<i class="lni lni-money-protection fs-5 theme-cl mt-1"></i>
				<div>
					<h6 class="ft-bold mb-1 small">ফ্লেক্সিবল পেআউট</h6>
					<p class="text-muted small mb-0">
						bKash, Nagad বা ব্যাংকে উইথড্র করুন। শিডিউল করা
						অটো-পেআউটও পাওয়া যাবে।
					</p>
				</div>
			</div>
		</div>
	</div>

	<div class="text-center mt-4">
		<a href="/signup/?role=seller" class="btn btn-primary px-4">
			সেলার হোন</a>
		<div class="text-muted small mt-2">
			আগে থেকেই সেলার অ্যাকাউন্ট আছে?
			<a href="/login/">সাইন ইন করুন</a>।
		</div>
	</div>""",
        "toc_bn": [],
        "faq_bn": [],
        "related_bn": [],
    },

    "sell/onboarding": {
        "title_bn": "সেলার অনবোর্ডিং গাইড",
        "subtitle_bn": (
            "সাইনআপ থেকে শুরু করে SGT Cart-এ আপনার প্রথম বিক্রি পর্যন্ত — "
            "নতুন সেলারদের জন্য ধাপে ধাপে গাইড।"
        ),
        "section_bn": "সেলার রিসোর্স",
        "body_html_bn": """<p class="lead small">
		SGT Cart-এ শপ খুলতে ফর্ম পূরণে প্রায় <strong>30 মিনিট</strong> লাগে, এবং
		অ্যাডমিন ভেরিফিকেশনের জন্য আরও 1-2 কর্মদিবস। এই গাইড আপনাকে
		শূন্য থেকে লাইভ স্টোর এবং প্রথম বিক্রি পর্যন্ত নিয়ে যাবে।
	</p>
	<p class="small">
		শুরু করার আগে <a href="/seller-terms/">সেলার এগ্রিমেন্ট</a> এবং
		<a href="/sell/listing-guidelines/">লিস্টিং গাইডলাইন</a> পড়ে নিন —
		লিস্টিং করার মাধ্যমে আপনি যে নিয়মগুলো গ্রহণ করছেন সেগুলো এখানেই বলা আছে।
	</p>

	<h2 id="eligibility">১. SGT Cart-এ কারা বিক্রি করতে পারবেন</h2>
	<table>
		<tr><th>আপনি যোগ্য যদি আপনি হন…</th><th>যা লাগবে</th></tr>
		<tr><td>বাংলাদেশে বসবাসকারী একজন ব্যক্তি / সোল ট্রেডার</td><td>বয়স 18+, বৈধ NID, ট্রেড লাইসেন্স, TIN।</td></tr>
		<tr><td>বাংলাদেশে রেজিস্টার্ড কোম্পানি / পার্টনারশিপ / প্রোপ্রাইটরশিপ</td><td>RJSC সার্টিফিকেট, ট্রেড লাইসেন্স, TIN, প্রযোজ্য হলে BIN (VAT), অথরাইজড প্রতিনিধির NID।</td></tr>
		<tr><td>স্থানীয় রেজিস্টার্ড এনটিটি সহ অনিবাসী বাংলাদেশি (NRB)</td><td>কোম্পানির মতোই সবকিছু, এবং বাংলাদেশের ভেতরে অপারেটিং ঠিকানা।</td></tr>
	</table>

	<h2 id="documents">২. যেসব ডকুমেন্ট লাগবে</h2>
	<ul>
		<li><strong>NID</strong> — সামনে + পেছনের পরিষ্কার স্ক্যান বা ছবি।</li>
		<li><strong>ট্রেড লাইসেন্স</strong> — পরিষ্কার স্ক্যান (PDF/JPG)।</li>
		<li><strong>TIN সার্টিফিকেট</strong> — National Board of Revenue থেকে ইস্যু করা।</li>
		<li><strong>BIN / VAT রেজিস্ট্রেশন</strong> — আপনার বার্ষিক টার্নওভার NBR থ্রেশহোল্ডের উপরে হলে।</li>
		<li><strong>ব্যাংক স্টেটমেন্টের প্রথম পেজ</strong> অথবা <strong>bKash / Nagad মার্চেন্ট অ্যাকাউন্টের স্ক্রিনশট</strong>।</li>
		<li><strong>শপ লোগো</strong> (PNG, ট্রান্সপারেন্ট ব্যাকগ্রাউন্ড, ≥ 256×256 px)।</li>
		<li><strong>শপ ব্যানার</strong> (JPG, 1920×600 px সুপারিশকৃত)।</li>
	</ul>

	<h2 id="step1-account">৩. ধাপ 1 — আপনার অ্যাকাউন্ট তৈরি করুন</h2>
	<ol>
		<li><a href="/signup/?role=seller">/signup/?role=seller</a>-এ যান।</li>
		<li>আপনার বিজনেস ইমেইল, মোবাইল নম্বর দিন এবং একটি পাসওয়ার্ড সেট করুন।</li>
		<li>ইনবক্সে পাঠানো ওয়ান-টাইম কোড দিয়ে ইমেইল ভেরিফাই করুন।</li>
		<li>আপনি <strong>Seller Center</strong>-এ "<em>Pending Verification</em>" স্ট্যাটাসে লগইন হয়ে যাবেন।</li>
	</ol>

	<h2 id="step2-kyc">৪. ধাপ 2 — ভেরিফিকেশনের জন্য KYC সাবমিট করুন</h2>
	<ol>
		<li><a href="/seller/">/seller/</a> থেকে <strong>Shop Verification (KYC)</strong>-এ ট্যাপ করুন।</li>
		<li>আপনার বিজনেস টাইপ বেছে নিন (ইন্ডিভিজুয়াল / কোম্পানি / পার্টনারশিপ)।</li>
		<li>NID সামনে + পেছনে আপলোড করুন; কার্ডে যেভাবে লেখা আছে ঠিক সেভাবেই NID নম্বর লিখুন।</li>
		<li>ট্রেড লাইসেন্স আপলোড করুন; লাইসেন্স নম্বর লিখুন।</li>
		<li>TIN সার্টিফিকেট আপলোড করুন; TIN লিখুন।</li>
		<li>শপের সম্পূর্ণ ঠিকানা দিন।</li>
		<li>সাবমিট করুন।</li>
	</ol>
	<p>
		একজন SGT Cart অ্যাডমিন <strong>1-2 কর্মদিবসের</strong> মধ্যে আপনার সাবমিশন রিভিউ করবেন।
		সিদ্ধান্ত হলে আপনি একটি ইমেইল পাবেন।
	</p>

	<h2 id="step3-store">৫. ধাপ 3 — আপনার স্টোর প্রোফাইল তৈরি করুন</h2>
	<ul>
		<li><strong>শপের নাম (English + বাংলা)</strong> — বাইলিঙ্গুয়াল রাখা দৃঢ়ভাবে সুপারিশ করা হলো।</li>
		<li><strong>শপ স্লাগ</strong> — URL-এ ব্যবহার হবে <code>/store/your-slug/</code>।</li>
		<li><strong>ডেসক্রিপশন</strong> — ২-৩ প্যারাগ্রাফের একটি পরিচিতি।</li>
		<li><strong>লোগো</strong> — স্কয়ার ট্রান্সপারেন্ট PNG সবচেয়ে ভালো দেখায়।</li>
		<li><strong>ব্যানার</strong> — স্টোর পেজের জন্য ওয়াইড কভার ইমেজ।</li>
	</ul>

	<h2 id="step4-products">৬. ধাপ 4 — আপনার প্রথম প্রোডাক্ট লিস্ট করুন</h2>
	<ol>
		<li>Seller Center থেকে <strong>My Products → Create</strong>-এ ট্যাপ করুন।</li>
		<li>টাইটেল (EN + BN), ক্যাটাগরি, বেস প্রাইস, স্টক, SKU, ডেসক্রিপশন পূরণ করুন।</li>
		<li>1-8টি প্রোডাক্ট ইমেজ আপলোড করুন। প্রথমটি কভার হিসেবে ব্যবহৃত হবে।</li>
		<li>প্রযোজ্য হলে ভ্যারিয়েন্ট যোগ করুন — কালার, সাইজ, প্রতিটির নিজস্ব প্রাইস এবং স্টক সহ।</li>
		<li><strong>Submit for review</strong>-এ ট্যাপ করুন।</li>
	</ol>

	<h2 id="step5-payout">৭. ধাপ 5 — পেআউট ও ট্যাক্স সেটআপ করুন</h2>
	<ol>
		<li>Seller Center থেকে <strong>Payout Settings</strong> খুলুন।</li>
		<li>আপনার প্রাইমারি পেআউট মেথড বেছে নিন (ব্যাংক / bKash / Nagad)।</li>
		<li>আপনার TIN নিশ্চিত করুন।</li>
		<li><a href="/seller-terms/">সেলার এগ্রিমেন্ট</a> পড়ুন এবং অ্যাকসেপ্ট করুন।</li>
	</ol>""",
        "toc_bn": [
            {"anchor": "eligibility", "label": "১. SGT Cart-এ কারা বিক্রি করতে পারবেন"},
            {"anchor": "documents", "label": "২. যেসব ডকুমেন্ট লাগবে"},
            {"anchor": "step1-account", "label": "৩. ধাপ 1 — আপনার অ্যাকাউন্ট তৈরি করুন"},
            {"anchor": "step2-kyc", "label": "৪. ধাপ 2 — ভেরিফিকেশনের জন্য KYC সাবমিট করুন"},
            {"anchor": "step3-store", "label": "৫. ধাপ 3 — আপনার স্টোর প্রোফাইল তৈরি করুন"},
            {"anchor": "step4-products", "label": "৬. ধাপ 4 — আপনার প্রথম প্রোডাক্ট লিস্ট করুন"},
            {"anchor": "step5-payout", "label": "৭. ধাপ 5 — পেআউট ও ট্যাক্স সেটআপ করুন"},
        ],
        "faq_bn": [
            {
                "q": "আমার শপ কত দ্রুত লাইভ হতে পারে?",
                "a": "প্রায়ই একই দিনে। KYC ডকুমেন্ট পরিষ্কার এবং সম্পূর্ণ থাকলে অ্যাডমিন রিভিউতে 1-2 কর্মদিবস লাগে।",
            },
            {
                "q": "আমার কি ফিজিক্যাল শপ থাকা জরুরি?",
                "a": "না। হোম-বেসড সেলার, ইম্পোর্টার, ড্রপশিপার এবং ক্রাফটসপারসন — সবাই যোগ্য।",
            },
            {
                "q": "আমি কি একাধিক ক্যাটাগরিতে বিক্রি করতে পারব?",
                "a": "হ্যাঁ। কোনো ক্যাটাগরির সীমাবদ্ধতা নেই। আমাদের অনেক টপ সেলার 3-5টি ক্যাটাগরিতে কাজ করেন।",
            },
        ],
        "related_bn": [
            {
                "href": "/seller-terms/",
                "title": "সেলার এগ্রিমেন্ট",
                "desc": "যে কন্ট্রাক্ট আপনার শপ পরিচালনা করবে।",
            },
            {
                "href": "/sell/fees/",
                "title": "ফি ও কমিশন",
                "desc": "প্রতি ডেলিভার হওয়া সেলে SGT Cart যা চার্জ করে।",
            },
            {
                "href": "/sell/listing-guidelines/",
                "title": "লিস্টিং গাইডলাইন",
                "desc": "যেভাবে লিস্টিং লিখলে অ্যাপ্রুভ হবে।",
            },
        ],
    },

    "sell/fees": {
        "title_bn": "সেলার ফি ও কমিশন",
        "subtitle_bn": (
            "SGT Cart সেলারদের কাছ থেকে ঠিক কী চার্জ করে — ক্যাটাগরি অনুযায়ী কমিশন, "
            "পেমেন্ট-প্রসেসিং পাস-থ্রু, VAT, এবং অপশনাল সার্ভিস।"
        ),
        "section_bn": "সেলার রিসোর্স",
        "body_html_bn": """<p class="lead small">
		SGT Cart-এর প্রাইসিং খুব সহজ: প্রতি ডেলিভার হওয়া সেলে একটি ফ্ল্যাট
		প্ল্যাটফর্ম কমিশন, কোনো মাসিক সাবস্ক্রিপশন নেই, কোনো লিস্টিং ফি নেই।
		অপশনাল প্রমোশনাল সার্ভিস আলাদাভাবে বিল করা হয় এবং শুধু তখনই, যখন আপনি অপ্ট ইন করেন।
	</p>

	<h2 id="commission">১. প্ল্যাটফর্ম কমিশন</h2>
	<p>
		কমিশন <strong>শুধুমাত্র ডেলিভার হওয়া সাব-অর্ডারে</strong> চার্জ করা হয়। ক্যানসেল
		বা রিফান্ড হওয়া সাব-অর্ডারে কোনো কমিশন নেই।
	</p>
	<table>
		<tr><th>ক্যাটাগরি</th><th>কমিশন রেট</th></tr>
		<tr><td>ডিফল্ট (বেশিরভাগ ক্যাটাগরি)</td><td>10.0%</td></tr>
		<tr><td>ইলেকট্রনিকস ও মোবাইল</td><td>8.0%</td></tr>
		<tr><td>বই ও স্টেশনারি</td><td>5.0%</td></tr>
		<tr><td>ফ্যাশন (পোশাক, জুতা, অ্যাকসেসরিজ)</td><td>12.0%</td></tr>
		<tr><td>হেলথ ও বিউটি</td><td>12.0%</td></tr>
		<tr><td>হোম ও লিভিং</td><td>10.0%</td></tr>
		<tr><td>গ্রোসারি (FMCG)</td><td>6.0%</td></tr>
		<tr><td>ঘড়ি ও জুয়েলারি</td><td>8.0%</td></tr>
		<tr><td>খেলনা ও বেবি</td><td>10.0%</td></tr>
	</table>

	<h2 id="payment">২. পেমেন্ট-প্রসেসিং ফি</h2>
	<p>পেমেন্ট-নেটওয়ার্ক ফি <strong>কস্ট প্রাইসে পাস-থ্রু করা হয়</strong> — SGT Cart এতে কোনো মার্ক-আপ করে না:</p>
	<table>
		<tr><th>মেথড</th><th>ফি</th></tr>
		<tr><td>SSLCommerz কার্ড (Visa / MasterCard / AMEX)</td><td>অর্ডার অ্যামাউন্টের 2.5%</td></tr>
		<tr><td>bKash</td><td>অর্ডার অ্যামাউন্টের 1.85%</td></tr>
		<tr><td>Nagad</td><td>অর্ডার অ্যামাউন্টের 1.5%</td></tr>
		<tr><td>Cash on Delivery</td><td>প্রতি সাব-অর্ডারে Tk 20 ফ্ল্যাট</td></tr>
		<tr><td>SGT Cart ওয়ালেট ক্রেডিট / Reward Points</td><td>0%</td></tr>
	</table>

	<h2 id="promotion">৩. অপশনাল প্রমোশনাল সার্ভিস</h2>
	<table>
		<tr><th>সার্ভিস</th><th>রেট</th></tr>
		<tr><td>স্পনসর্ড সার্চ পজিশন</td><td>প্রতি ক্লিকে Tk 3-15 (CPC, আপনার বিড)</td></tr>
		<tr><td>হোমপেজ হিরো ব্যানার</td><td>Tk 5,000 / সপ্তাহ (অ্যাডমিন-কিউরেটেড)</td></tr>
		<tr><td>হোমপেজ স্ট্রিপ ব্যানার</td><td>Tk 2,500 / সপ্তাহ</td></tr>
		<tr><td>ফ্ল্যাশ-সেল ফিচার</td><td>সেলারের জন্য ফ্রি</td></tr>
	</table>

	<h2 id="refund">৪. রিফান্ড হওয়া অর্ডারের কমিশন রিভার্সাল</h2>
	<p>
		ডেলিভার হওয়া কোনো সাব-অর্ডার পরে রিফান্ড হলে, রিফান্ডের অনুপাতে
		<strong>SGT Cart-এর কমিশনও রিফান্ড করা হয়</strong>।
	</p>

	<h2 id="vat">৫. VAT কালেকশন ও জমাদান</h2>
	<p>
		অনলাইন মার্কেটপ্লেসের জন্য NBR-এর নিয়ম অনুযায়ী, SGT Cart নির্দিষ্ট
		ক্যাটাগরির সেলে সোর্সে VAT কেটে রাখে (বর্তমানে বেশিরভাগ ক্যাটাগরির জন্য 5%)
		এবং সেটি NBR-এ জমা দেয়।
	</p>

	<h2 id="worked-example">৬. উদাহরণসহ হিসাব — Tk 1,000-এর একটি সেল</h2>
	<p>কাস্টমার একটি ফ্যাশন আইটেমের জন্য bKash-এ Tk 1,000 (VAT সহ) পেমেন্ট করলেন।</p>
	<table>
		<tr><td>মোট অর্ডার অ্যামাউন্ট</td><td><strong>Tk 1,000.00</strong></td></tr>
		<tr><td>আইটেম সাবটোটাল</td><td>Tk 952.38</td></tr>
		<tr><td>VAT অংশ (5%)</td><td>Tk 47.62</td></tr>
		<tr><td>কমিশন @ 12%</td><td>− Tk 114.29</td></tr>
		<tr><td>bKash গেটওয়ে ফি @ 1.85%</td><td>− Tk 18.50</td></tr>
		<tr><td>উইথহোল্ড করা VAT</td><td>− Tk 47.62</td></tr>
		<tr><td><strong>আপনার ওয়ালেটে নেট</strong></td><td><strong>Tk 819.59</strong></td></tr>
	</table>""",
        "toc_bn": [
            {"anchor": "commission", "label": "১. প্ল্যাটফর্ম কমিশন"},
            {"anchor": "payment", "label": "২. পেমেন্ট-প্রসেসিং ফি"},
            {"anchor": "promotion", "label": "৩. অপশনাল প্রমোশনাল সার্ভিস"},
            {"anchor": "refund", "label": "৪. রিফান্ড হওয়া অর্ডারের কমিশন রিভার্সাল"},
            {"anchor": "vat", "label": "৫. VAT কালেকশন ও জমাদান"},
            {"anchor": "worked-example", "label": "৬. উদাহরণসহ হিসাব — Tk 1,000-এর একটি সেল"},
        ],
        "faq_bn": [
            {
                "q": "মাসিক কোনো সাবস্ক্রিপশন ফি আছে কি?",
                "a": "না। SGT Cart-এ কোনো মাসিক সাবস্ক্রিপশন নেই, কোনো লিস্টিং ফি নেই, কোনো এনরোলমেন্ট ফি নেই। আপনি শুধু ডেলিভার হওয়া সেলের কমিশন দেবেন।",
            },
            {
                "q": "আমি কি কম কমিশনের জন্য নেগোসিয়েট করতে পারি?",
                "a": "হাই-ভলিউম সেলার (নিয়মিতভাবে মাসিক Tk 5 লাখ+ GMV) seller-support@sgtcart.com-এ যোগাযোগ করে কাস্টম রেটের জন্য নেগোসিয়েট করতে পারেন।",
            },
            {
                "q": "SGT Cart কি আমার ইনকাম ট্যাক্স জমা দেয়?",
                "a": "আমরা ইনকাম ট্যাক্স উইথহোল্ড করি না — শুধু আইনে যেখানে প্রয়োজন সেখানেই VAT কেটে রাখি।",
            },
        ],
        "related_bn": [
            {
                "href": "/sell/onboarding/",
                "title": "অনবোর্ডিং গাইড",
                "desc": "যেভাবে আপনার শপ খুলবেন।",
            },
            {
                "href": "/seller-terms/",
                "title": "সেলার এগ্রিমেন্ট",
                "desc": "পূর্ণাঙ্গ কন্ট্রাক্টের শর্তাবলী।",
            },
            {
                "href": "/sell/payouts/",
                "title": "পেআউট",
                "desc": "কখন এবং কীভাবে টাকা আপনার অ্যাকাউন্টে আসবে।",
            },
        ],
    },

    "sell/listing-guidelines": {
        "title_bn": "প্রোডাক্ট লিস্টিং গাইডলাইন",
        "subtitle_bn": (
            "SGT Cart-এ একটি প্রোডাক্ট লিস্টিং যেভাবে অ্যাপ্রুভ-যোগ্য হয় — "
            "এবং সচরাচর যেসব ভুলের কারণে রিজেক্ট হয়।"
        ),
        "section_bn": "সেলার রিসোর্স",
        "body_html_bn": """<p class="lead small">
		একটি ভালো লিস্টিং ক্লিক, কনভার্সন এবং রিপিট কাস্টমার নিয়ে আসে। একটি খারাপ
		লিস্টিং রিজেক্ট হয়, সময় নষ্ট করে এবং আপনার সার্চ র‍্যাঙ্কের ক্ষতি করে।
	</p>

	<h2 id="title">১. টাইটেলের নিয়ম</h2>
	<ul>
		<li><strong>দৈর্ঘ্য</strong>: 30-90 ক্যারেক্টার।</li>
		<li><strong>স্ট্রাকচার</strong>: <em>Brand — Model — Key Spec — Variant</em>।</li>
		<li><strong>কীওয়ার্ড স্টাফিং নয়</strong>: একই শব্দ বারবার লেখা বা ব্র্যান্ড নামের কমা-স্টাফিং রিজেক্ট করা হবে।</li>
		<li><strong>ব্র্যান্ডের অপব্যবহার নয়</strong>: আপনার প্রোডাক্ট যদি কোনো বিখ্যাত ব্র্যান্ডের তৈরি না হয়, তাহলে সেই ব্র্যান্ডের নাম টাইটেলে দেবেন না।</li>
		<li><strong>কোনো ইমোজি, ALL CAPS, বা বিস্ময়সূচক চিহ্ন নয়</strong>।</li>
		<li><strong>কোনো কন্টাক্ট ইনফো নয়</strong>: টাইটেলে কোনো ফোন নম্বর, WhatsApp, Telegram, বা ইমেইল অ্যাড্রেস নয়।</li>
	</ul>

	<h2 id="description">২. ডেসক্রিপশনের কোয়ালিটি</h2>
	<ul>
		<li><strong>মৌলিক টেক্সট</strong> — নিজের ডেসক্রিপশন নিজে লিখুন। কপি-পেস্ট রিজেক্টের কারণ হতে পারে।</li>
		<li><strong>ইউজ কেস দিয়ে শুরু করুন</strong> — এটি কার জন্য, কোন সমস্যা সমাধান করে?</li>
		<li><strong>স্পেসিফিকেশন লিস্ট করুন</strong> — স্ট্রাকচার্ড Spec rows ফিচার ব্যবহার করুন।</li>
		<li><strong>বক্সে কী আছে উল্লেখ করুন</strong> — মূল আইটেম + অ্যাকসেসরিজ + ওয়ারেন্টি কার্ড।</li>
		<li><strong>ওয়ারেন্টি / রিটার্নের শর্ত উল্লেখ করুন</strong>।</li>
		<li><strong>অ্যান্টি-ডিসইন্টারমিডিয়েশন</strong> — কোনো ফোন নম্বর নয়, অফ-প্ল্যাটফর্ম URL নয়।</li>
	</ul>

	<h2 id="images">৩. ইমেজের মান</h2>
	<table>
		<tr><th>নিয়ম</th><th>বিবরণ</th></tr>
		<tr><td>রেজোলিউশন</td><td>সর্বনিম্ন 1000×1000 px। স্কয়ার (1:1) সুপারিশকৃত।</td></tr>
		<tr><td>ফরম্যাট</td><td>JPG বা PNG।</td></tr>
		<tr><td>ফাইল সাইজ</td><td>প্রতিটি ইমেজ 4 MB-এর নিচে।</td></tr>
		<tr><td>ব্যাকগ্রাউন্ড</td><td>কভারের জন্য সাদা বা প্রায়-সাদা।</td></tr>
		<tr><td>সংখ্যা</td><td>প্রতি লিস্টিংয়ে 1-8টি ইমেজ।</td></tr>
		<tr><td>ওয়াটারমার্ক</td><td>আপনার শপ লোগো / ফোন / URL ওয়াটারমার্ক হিসেবে দেবেন না।</td></tr>
		<tr><td>চুরি করা ইমেজ</td><td>শুধু সেই ইমেজ ব্যবহার করুন যেগুলো আপনি নিজে তুলেছেন বা ব্যবহারের অধিকার আপনার আছে।</td></tr>
	</table>

	<h2 id="bilingual">৪. বাইলিঙ্গুয়াল লিস্টিংকে উৎসাহ</h2>
	<p>
		বাইলিঙ্গুয়াল লিস্টিং (বাংলা + English) সার্চে স্পষ্টভাবে উপরে র‍্যাঙ্ক করে।
		সেলার ফর্মে প্যারালাল ফিল্ড আছে (<code>title_en</code> + <code>title_bn</code>); দুটোই পূরণ করুন।
	</p>

	<h2 id="pricing">৫. প্রাইসিং ও MRP-এর নিয়ম</h2>
	<ul>
		<li><strong>প্রাইস BDT-তে, VAT সহ</strong>।</li>
		<li><strong>ভুয়া ডিসকাউন্ট দেখানোর জন্য বাড়ানো "MRP" নয়</strong>।</li>
		<li><strong>লিস্টিং চলাকালীন লিস্টেড প্রাইস সম্মান করুন</strong>।</li>
		<li><strong>প্রতারণামূলক দাম পরিবর্তন (bait-and-switch) নয়</strong>।</li>
	</ul>

	<h2 id="variants">৬. ভ্যারিয়েন্ট ও বাল্ক টিয়ার</h2>
	<p>ভ্যারিয়েন্ট (সাইজ, কালার) এবং বাল্ক প্রাইসিং টিয়ার সৎভাবে ব্যবহার করলে কনভার্সন বাড়াতে সহায়ক টুল।</p>

	<h2 id="category">৭. ক্যাটাগরি বাছাই</h2>
	<p>সবচেয়ে গভীর এবং সঠিক সাব-ক্যাটাগরি বেছে নিন।</p>

	<h2 id="rejections">৮. সচরাচর রিজেকশন ও সমাধান</h2>
	<table>
		<tr><th>রিজেকশনের কারণ</th><th>সমাধান</th></tr>
		<tr><td>অন্য সাইট থেকে ডেসক্রিপশন কপি করা</td><td>নিজের ভাষায় লিখুন।</td></tr>
		<tr><td>ইমেজে ওয়াটারমার্ক বা কন্টাক্ট ইনফো আছে</td><td>ওয়াটারমার্ক ছাড়া রি-এক্সপোর্ট করুন।</td></tr>
		<tr><td>ব্র্যান্ডের নামের অপব্যবহার</td><td>একটি জেনেরিক ডেসক্রিপ্টর দিয়ে রিপ্লেস করুন।</td></tr>
		<tr><td>বাড়ানো MRP / ভুয়া ডিসকাউন্ট</td><td>আসল আগের প্রাইস MRP হিসেবে সেট করুন।</td></tr>
		<tr><td>ডেসক্রিপশনে ফোন নম্বর</td><td>সরিয়ে ফেলুন।</td></tr>
	</table>""",
        "toc_bn": [
            {"anchor": "title", "label": "১. টাইটেলের নিয়ম"},
            {"anchor": "description", "label": "২. ডেসক্রিপশনের কোয়ালিটি"},
            {"anchor": "images", "label": "৩. ইমেজের মান"},
            {"anchor": "bilingual", "label": "৪. বাইলিঙ্গুয়াল লিস্টিংকে উৎসাহ"},
            {"anchor": "pricing", "label": "৫. প্রাইসিং ও MRP-এর নিয়ম"},
            {"anchor": "variants", "label": "৬. ভ্যারিয়েন্ট ও বাল্ক টিয়ার"},
            {"anchor": "category", "label": "৭. ক্যাটাগরি বাছাই"},
            {"anchor": "rejections", "label": "৮. সচরাচর রিজেকশন ও সমাধান"},
        ],
        "faq_bn": [
            {
                "q": "লিস্টিং রিভিউতে কত সময় লাগে?",
                "a": "সাধারণত একই দিনে, প্রায়ই অফিস সময়ের মধ্যে 2-4 ঘণ্টার মধ্যেই।",
            },
            {
                "q": "পাবলিশড লিস্টিং রি-রিভিউ ছাড়া এডিট করা যায় কি?",
                "a": "হ্যাঁ — প্রাইস, স্টক, ডিসকাউন্ট-প্রাইসের পরিবর্তন সঙ্গে সঙ্গেই কার্যকর হয়।",
            },
            {
                "q": "আমার লিস্টিংয়ে 'Verified by SGT' ব্যাজ কীভাবে পাব?",
                "a": "সম্পূর্ণ KYC সাবমিট করুন। ব্যাজটি অ্যাপ্রুভড সব সেলারকে স্বয়ংক্রিয়ভাবে দেওয়া হয়।",
            },
        ],
        "related_bn": [
            {
                "href": "/sell/prohibited-items/",
                "title": "নিষিদ্ধ আইটেম",
                "desc": "যা আপনি কখনোই লিস্ট করতে পারবেন না।",
            },
            {
                "href": "/sell/onboarding/",
                "title": "অনবোর্ডিং গাইড",
                "desc": "30 মিনিটে আপনার শপ লাইভ করুন।",
            },
            {
                "href": "/seller-terms/",
                "title": "সেলার এগ্রিমেন্ট",
                "desc": "এই নিয়মগুলোর পেছনের কন্ট্রাক্ট।",
            },
        ],
    },
}
