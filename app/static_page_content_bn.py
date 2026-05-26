"""Bangla translations for the 16 footer pages seeded by
`flask seed-static-pages`. Loaded by the same command when `--lang bn`
or by `flask seed-static-pages-bn`.

Keys must match `slug` values in `static_page_content.FOOTER_PAGES`.
Each value provides Bangla strings for the bilingual columns: title,
subtitle, section, body_html, toc, faq, related.
"""

FOOTER_PAGES_BN = {'help': {'title': 'সাহায্য কেন্দ্র',
          'subtitle': 'আপনার SGT কার্ট অভিজ্ঞতার প্রতিটি বিষয়ে দ্রুত উত্তর ও যোগাযোগের পথ এখানে পাবেন।',
          'section': 'কাস্টমার হেল্প',
          'toc': [{'anchor': 'ordering', 'label': 'অর্ডার করা'},
                  {'anchor': 'payments', 'label': 'পেমেন্ট'},
                  {'anchor': 'delivery', 'label': 'ডেলিভারি'},
                  {'anchor': 'returns', 'label': 'ফেরত ও রিফান্ড'},
                  {'anchor': 'account', 'label': 'অ্যাকাউন্ট ও নিরাপত্তা'}],
          'body_html': '\n'
                       '<p class="lead small">সবচেয়ে প্রচলিত প্রশ্নগুলো নিচে দেখুন, বা পুরো\n'
                       'সেলফ-সার্ভিস লাইব্রেরি ঘুরে দেখুন। যা খুঁজছেন না পেলে আমাদের টিম\n'
                       '১ কর্মদিবস-এর মধ্যে ইমেইল-এ উত্তর দেয়।</p>\n'
                       '\n'
                       '<h2 id="ordering">অর্ডার করা</h2>\n'
                       '<ul>\n'
                       '  <li><a href="/help/how-to-order/">কীভাবে অর্ডার প্লেস করবেন</a></li>\n'
                       '  <li><a href="/help/cancellations/">অর্ডার বাতিল করা</a></li>\n'
                       '  <li><a href="/shipping/">ডেলিভারি সময় ও চার্জ</a></li>\n'
                       '</ul>\n'
                       '\n'
                       '<h2 id="payments">পেমেন্ট</h2>\n'
                       '<ul>\n'
                       '  <li><a href="/help/payment-methods/">গৃহীত পেমেন্ট পদ্ধতি</a></li>\n'
                       '  <li><a href="/help/buyer-protection/">বায়ার প্রোটেকশন প্রোগ্রাম</a></li>\n'
                       '  <li><a href="/refund-policy/">রিফান্ড পলিসি</a></li>\n'
                       '</ul>\n'
                       '\n'
                       '<h2 id="delivery">ডেলিভারি</h2>\n'
                       '<ul>\n'
                       '  <li><a href="/shipping/">শিপিং জোন ও ETA</a></li>\n'
                       '  <li><a href="/returns/">ফেরতের শিপমেন্ট</a></li>\n'
                       '</ul>\n'
                       '\n'
                       '<h2 id="returns">ফেরত ও রিফান্ড</h2>\n'
                       '<p>বেশিরভাগ পণ্য ডেলিভারি-র ৭ দিনের মধ্যে ফেরত দেওয়া যায়।\n'
                       'বিস্তারিত নীতিমালা <a href="/returns/">ফেরত ও রিফান্ড</a> পেজে দেখুন।</p>\n'
                       '\n'
                       '<h2 id="account">অ্যাকাউন্ট ও নিরাপত্তা</h2>\n'
                       '<p>পাসওয়ার্ড ভুলে গেছেন? <a href="/auth/login">সাইন ইন পেজে</a>\n'
                       '"পাসওয়ার্ড ভুলে গেছেন" লিংক ব্যবহার করুন। অন্য যেকোনো সাহায্যের জন্য\n'
                       '<a href="mailto:support@sgtcart.com">সাপোর্ট@sgtcart.com</a>-এ যোগাযোগ করুন।</p>\n',
          'faq': [{'q': 'আমার অর্ডার কীভাবে ট্র্যাক করব?',
                   'a': "সাইন ইন করে <a href='/account/orders/'>আমার অর্ডার</a> খুলুন। প্রতিটি পণ্যের "
                        'বর্তমান স্ট্যাটাস দেখাবে — প্রসেসিং, শিপড, বা ডেলিভার্ড।'},
                  {'q': 'পণ্য ক্ষতিগ্রস্ত অবস্থায় পৌঁছালে কী করব?',
                   'a': "অ্যাকাউন্ট-এ অর্ডার খুলে 'রিটার্ন অনুরোধ' ক্লিক করুন। কুরিয়ার পণ্য সেলার-এর কাছে "
                        'ফেরত পৌঁছানোর ২ কর্মদিবস-র মধ্যে আমরা রিফান্ড অনুমোদন করি।'}],
          'related': [{'href': '/help/how-to-order/',
                       'title': 'অর্ডার করার নিয়ম',
                       'desc': 'নতুন বায়ার-দের জন্য ধাপে ধাপে নির্দেশিকা।'},
                      {'href': '/help/payment-methods/',
                       'title': 'পেমেন্ট পদ্ধতি',
                       'desc': 'কার্ড, COD, মোবাইল ওয়ালেট, ব্যাংক ট্রান্সফার।'},
                      {'href': '/contact/',
                       'title': 'যোগাযোগ করুন',
                       'desc': 'ফোন, WhatsApp, ইমেইল — সব চ্যানেল।'}]},
 'help/how-to-order': {'title': 'অর্ডার করার নিয়ম',
                       'subtitle': 'ব্রাউজ থেকে ডেলিভারি পর্যন্ত — পাঁচ মিনিটের সম্পূর্ণ গাইড।',
                       'section': 'কাস্টমার হেল্প',
                       'toc': [{'anchor': 'find', 'label': '১. পণ্য খুঁজুন'},
                               {'anchor': 'cart', 'label': '২. কার্ট-এ যোগ করুন'},
                               {'anchor': 'checkout', 'label': '৩. চেকআউট'},
                               {'anchor': 'pay', 'label': '৪. Pay করুন বা COD বেছে নিন'},
                               {'anchor': 'track', 'label': '৫. অর্ডার ট্র্যাক করুন'}],
                       'body_html': '\n'
                                    '<h2 id="find">১. পণ্য খুঁজুন</h2>\n'
                                    '<p>উপরের সার্চ বার ব্যবহার করুন, ক্যাটাগরি মেনু দেখুন, বা হোমপেজ\n'
                                    'ক্যারোসেল খুলুন। যেকোনো প্রোডাক্ট কার্ড-এ ক্লিক করলে পণ্যের ছবি, '
                                    'স্পেক,\n'
                                    'সেলার, রিভিউ ও স্টক ইন্ডিকেটর দেখতে পাবেন।</p>\n'
                                    '\n'
                                    '<h2 id="cart">২. কার্ট-এ যোগ করুন</h2>\n'
                                    '<p>প্রয়োজনে ভ্যারিয়েন্ট বেছে নিন (সাইজ, রং ইত্যাদি), পরিমাণ ঠিক করুন '
                                    'এবং\n'
                                    '<strong>কার্টে যোগ করুন</strong> ক্লিক করুন। আপনি শপিং চালিয়ে যেতে\n'
                                    'পারেন; উপরের ডান কোণায় কার্ট আইকন-এ মোট দেখাবে।</p>\n'
                                    '\n'
                                    '<h2 id="checkout">৩. চেকআউট</h2>\n'
                                    '<p>কার্ট খুলে পণ্যগুলো একবার দেখে নিন এবং\n'
                                    '<strong>চেকআউট-এ এগিয়ে যান</strong> ক্লিক করুন। অ্যাকাউন্ট না থাকলে\n'
                                    'সাইন ইন বা সাইন আপ করতে বলা হবে। ডেলিভারি ঠিকানা দিন — আমরা\n'
                                    'বাংলাদেশের প্রতিটি জেলায় ডেলিভারি দিই।</p>\n'
                                    '\n'
                                    '<h2 id="pay">৪. Pay করুন বা ক্যাশ অন ডেলিভারি বেছে নিন</h2>\n'
                                    '<p>চেকআউট পেজে পেমেন্ট পদ্ধতি বেছে নিন। আমরা Visa, Mastercard,\n'
                                    'bKash, Nagad, Rocket এবং ক্যাশ অন ডেলিভারি গ্রহণ করি\n'
                                    '(<a href="/help/payment-methods/">বিস্তারিত তালিকা</a>)।</p>\n'
                                    '\n'
                                    '<h2 id="track">৫. অর্ডার ট্র্যাক করুন</h2>\n'
                                    '<p>প্রতিটি স্ট্যাটাস পরিবর্তনে ইমেইল confirmation ও SMS আপডেট পাবেন।\n'
                                    'যেকোনো সময়ে <a href="/account/orders/">আমার অর্ডার</a> খুলে live\n'
                                    'স্ট্যাটাস দেখতে পারেন।</p>\n'
                                    '\n'
                                    '<blockquote>Tip: <a href="/help/">/help/</a> বুকমার্ক করে রাখুন —\n'
                                    'সব কাস্টমার পলিসি ও how-to আর্টিকেল সেখান থেকে এক ক্লিক '
                                    'দূরে।</blockquote>\n',
                       'faq': [{'q': 'অর্ডার দিতে কি অ্যাকাউন্ট দরকার?',
                                'a': 'হ্যাঁ — অ্যাকাউন্ট থাকলে আমরা ট্র্যাকিং আপডেট পাঠাতে পারি ও যেকোনো '
                                     'সমস্যা সমাধান করতে পারি। সাইন আপ মাত্র ৩০ সেকেন্ডের কাজ।'},
                               {'q': 'একসাথে বিভিন্ন সেলার-এর কাছ থেকে পণ্য অর্ডার করা যায়?',
                                'a': 'অবশ্যই। প্রতিটি সেলার তাদের পণ্য আলাদাভাবে শিপ করবে — প্রতিটি '
                                     'sub-অর্ডার-এর জন্য আলাদা ট্র্যাকিং পাবেন।'}],
                       'related': [{'href': '/help/payment-methods/',
                                    'title': 'পেমেন্ট পদ্ধতি',
                                    'desc': 'কার্ড, COD, মোবাইল ওয়ালেট।'},
                                   {'href': '/help/cancellations/',
                                    'title': 'অর্ডার বাতিল',
                                    'desc': 'ডিসপ্যাচ-এর আগে ও পরে।'},
                                   {'href': '/help/buyer-protection/',
                                    'title': 'বায়ার প্রোটেকশন',
                                    'desc': 'আপনার ক্রয় কীভাবে সুরক্ষিত।'}]},
 'sell/payouts': {'title': 'সেলার পেআউট',
                  'subtitle': 'SGT কার্ট কীভাবে ও কখন আপনার আয় সেটেল করে।',
                  'section': 'সেলার রিসোর্স',
                  'toc': [{'anchor': 'cycle', 'label': 'সেটেলমেন্ট সাইকেল'},
                          {'anchor': 'methods', 'label': 'পেআউট পদ্ধতি'},
                          {'anchor': 'fees', 'label': 'Deduct হওয়া ফি'},
                          {'anchor': 'hold', 'label': 'হোল্ড ও রিজার্ভ'},
                          {'anchor': 'issues', 'label': 'পেআউট সমস্যা'}],
                  'body_html': '\n'
                               '<h2 id="cycle">সেটেলমেন্ট সাইকেল</h2>\n'
                               '<p>SGT কার্ট সাপ্তাহিক <strong>সাপ্তাহিক সাইকেল</strong>-এ সেলার পেআউট\n'
                               'সেটেল করে। যে অর্ডার <em>ডেলিভার্ড</em> এবং ৭ দিনের রিটার্ন উইন্ডো\n'
                               'পেরিয়ে গেছে, সেগুলো পরবর্তী সোমবার পেআউট-এর জন্য এলিজিবল হয়।\n'
                               'আপনার রেজিস্টার্ড পেআউট অ্যাকাউন্ট-এ বুধবার end-of-day পর্যন্ত\n'
                               'সিঙ্গেল ট্রান্সফার হিসেবে ফান্ড রিলিজ হয়।</p>\n'
                               '\n'
                               '<h2 id="methods">পেআউট পদ্ধতি</h2>\n'
                               '<ul>\n'
                               '  <li><strong>ব্যাংক ট্রান্সফার (BEFTN)</strong> — বাংলাদেশের যেকোনো '
                               'লাইসেন্সড bank।</li>\n'
                               '  <li><strong>bKash মার্চেন্ট</strong> — ৳২৫,০০০-এর কম অ্যামাউন্ট-এ '
                               'ইনস্ট্যান্ট।</li>\n'
                               '  <li><strong>Nagad বিজনেস</strong> — ডেইলি সেটেলমেন্ট।</li>\n'
                               '</ul>\n'
                               '<p>অ্যাডমিন অনুমোদন-এর পর <a href="/seller/wallet/">সেলার ওয়ালেট</a>\n'
                               'পেজে আপনার পেআউট detail যোগ বা আপডেট করুন।</p>\n'
                               '\n'
                               '<h2 id="fees">Deduct হওয়া ফি</h2>\n'
                               '<p>আপনার পেআউট হিসাব করা হয়:</p>\n'
                               '<p><code>(পণ্যের মোট + buyer-এর shipping fee) − category commission −\n'
                               'payment-gateway fee − যেকোনো refund বা chargeback</code></p>\n'
                               '<p>ক্যাটাগরি অনুযায়ী কমিশন শতাংশ <a href="/sell/fees/">সেলার ফি\n'
                               'ও কমিশন</a> পেজে দেখুন।</p>\n'
                               '\n'
                               '<h2 id="hold">হোল্ড ও রিজার্ভ</h2>\n'
                               '<p>নতুন শপ-এর প্রথম ৩০ দিন, বা যেকোনো disputed ট্রানজ্যাকশন-এর পর\n'
                               'SGT কার্ট সাপ্তাহিক সেটেলমেন্ট-এর ১০% পর্যন্ত সাময়িকভাবে রিজার্ভ\n'
                               'রাখতে পারে — সম্ভাব্য বায়ার রিফান্ড cover করতে। বকেয়া সমস্যা সমাধান\n'
                               'হলে রিজার্ভ automatically release হয়।</p>\n'
                               '\n'
                               '<h2 id="issues">পেআউট সমস্যা</h2>\n'
                               '<p>পেআউট বিলম্বিত হলে আপনার শপ নাম ও সেটেলমেন্ট week উল্লেখ করে\n'
                               '<a '
                               'href="mailto:seller-support@sgtcart.com">seller-support@sgtcart.com</a>-এ\n'
                               'ইমেইল করুন। আমরা ১ কর্মদিবস-র মধ্যে উত্তর দিই।</p>\n',
                  'faq': [{'q': 'আমার প্রথম পেআউট কেন delay হচ্ছে?',
                           'a': 'নতুন সেলার-রা ১৪ দিনের ভেরিফিকেশন period পার করেন — পেআউট শুরু হয় সেই '
                                'window শেষ হওয়ার পরের সোমবার থেকে।'},
                          {'q': 'পেআউট bank অ্যাকাউন্ট পরিবর্তন করতে পারি?',
                           'a': 'হ্যাঁ, তবে fraud protection-এর জন্য নতুন অ্যাকাউন্ট active হতে ৪৮ ঘণ্টার '
                                'cool-off প্রযোজ্য।'}],
                  'related': [{'href': '/sell/fees/',
                               'title': 'ফি ও কমিশন',
                               'desc': 'ক্যাটাগরি-wise কমিশন rate।'},
                              {'href': '/sell/onboarding/',
                               'title': 'সেলার onboarding',
                               'desc': '১-২ দিনে আপনার শপ খুলুন।'},
                              {'href': '/seller-terms/',
                               'title': 'সেলার Agreement',
                               'desc': 'আপনি যে legal framework গ্রহণ করেন।'}]},
 'sell/prohibited-items': {'title': 'নিষিদ্ধ পণ্য',
                           'subtitle': 'SGT কার্ট-এ যে ধরনের পণ্য আপনি list করতে পারবেন না।',
                           'section': 'সেলার রিসোর্স',
                           'toc': [{'anchor': 'illegal', 'label': 'অবৈধ পণ্য'},
                                   {'anchor': 'regulated', 'label': 'Regulated items'},
                                   {'anchor': 'restricted', 'label': 'Restricted ক্যাটাগরি'},
                                   {'anchor': 'ip', 'label': 'IP লঙ্ঘনকারী পণ্য'},
                                   {'anchor': 'enforcement', 'label': 'Enforcement'}],
                           'body_html': '\n'
                                        '<h2 id="illegal">অবৈধ পণ্য</h2>\n'
                                        '<p>SGT কার্ট-এ কখনো অনুমোদিত নয়:</p>\n'
                                        '<ul>\n'
                                        '  <li>মাদক, controlled drugs ও drug paraphernalia।</li>\n'
                                        '  <li>আগ্নেয়াস্ত্র, গোলাবারুদ, বিস্ফোরক ও replica weapon।</li>\n'
                                        '  <li>চোরাই পণ্য, jaali মুদ্রা বা ভুয়া document।</li>\n'
                                        '  <li>মানব দেহাবশেষ, body part, বা trafficked wildlife।</li>\n'
                                        '  <li>শিশু-যৌনতা বা সন্ত্রাসবাদ-সংক্রান্ত content।</li>\n'
                                        '</ul>\n'
                                        '\n'
                                        '<h2 id="regulated">Regulated items</h2>\n'
                                        '<p>List করার আগে অবশ্যই\n'
                                        '<a href="mailto:policy@sgtcart.com">পলিসি@sgtcart.com</a>-এ '
                                        'যোগাযোগ\n'
                                        'করুন — special লাইসেন্স প্রয়োজন:</p>\n'
                                        '<ul>\n'
                                        '  <li>Prescription medicine ও medical device।</li>\n'
                                        '  <li>Alcohol ও tobacco।</li>\n'
                                        '  <li>Pesticide ও industrial chemical।</li>\n'
                                        '  <li>Live animal (শুধু রেজিস্টার্ড breeder/সেলার)।</li>\n'
                                        '</ul>\n'
                                        '\n'
                                        '<h2 id="restricted">Restricted ক্যাটাগরি</h2>\n'
                                        '<ul>\n'
                                        '  <li>ব্যবহৃত cosmetics, undergarments বা intimate item।</li>\n'
                                        '  <li>ব্যবহৃত child car seat বা infant safety equipment।</li>\n'
                                        '  <li>Foreign currency exchange।</li>\n'
                                        '  <li>যেকোনো ধরনের adult content।</li>\n'
                                        '  <li>Cold-chain শিপিং প্রয়োজন এমন পণ্য (অনুমোদিত কুরিয়ার '
                                        'ছাড়া)।</li>\n'
                                        '</ul>\n'
                                        '\n'
                                        '<h2 id="ip">IP লঙ্ঘনকারী পণ্য</h2>\n'
                                        '<p>Counterfeit branded পণ্য, unauthorized replica ও bootleg '
                                        'মিডিয়া\n'
                                        'প্রথম detection-এই সরিয়ে ফেলা হয়। বিস্তারিত\n'
                                        '<a href="/ip-policy/">Intellectual Property পলিসি</a>।</p>\n'
                                        '\n'
                                        '<h2 id="enforcement">Enforcement</h2>\n'
                                        '<p>লঙ্ঘন হলে: লিস্টিং সরানো, অ্যাকাউন্ট-এ strike, এবং repeat বা '
                                        'গুরুতর\n'
                                        'অপরাধে — permanent শপ closure ও ওয়ালেট ব্যালেন্স বায়ার রিফান্ড '
                                        'cover-এ\n'
                                        'forfeit। প্রয়োজনে আমরা বাংলাদেশের law enforcement-এর সঙ্গে '
                                        'সহযোগিতা\n'
                                        'করি।</p>\n',
                           'faq': [{'q': 'আমি herbal supplement বিক্রি করি — সেগুলো কি অনুমোদিত?',
                                    'a': 'হ্যাঁ, যদি DGDA-রেজিস্টার্ড হয়। List করার আগে সেলার ড্যাশবোর্ড-এ '
                                         'registration সার্টিফিকেট আপলোড করুন।'},
                                   {'q': 'Second-hand electronics-এর কী হবে?',
                                    'a': "অনুমোদিত, তবে 'Used / Refurbished' badge অবশ্যই দিতে হবে। Used "
                                         'পণ্যকে new বলে list করা fraud হিসেবে গণ্য।'}],
                           'related': [{'href': '/ip-policy/',
                                        'title': 'IP পলিসি',
                                        'desc': 'Trademark ও copyright takedown।'},
                                       {'href': '/seller-terms/',
                                        'title': 'সেলার Agreement',
                                        'desc': 'সম্পূর্ণ legal terms।'},
                                       {'href': '/sell/code-of-conduct/',
                                        'title': 'আচরণবিধি',
                                        'desc': 'সেলার-দের জন্য আচরণের মান।'}]},
 'sell/seller-protection': {'title': 'সেলার প্রোটেকশন',
                            'subtitle': 'Chargeback ও bad-faith claim থেকে সৎ সেলার-দের কীভাবে SGT কার্ট '
                                        'সুরক্ষা দেয়।',
                            'section': 'সেলার রিসোর্স',
                            'toc': [{'anchor': 'what', 'label': 'কী সুরক্ষিত'},
                                    {'anchor': 'requirements', 'label': 'Eligibility'},
                                    {'anchor': 'process', 'label': 'Claim প্রক্রিয়া'},
                                    {'anchor': 'excluded', 'label': 'যা অন্তর্ভুক্ত নয়'}],
                            'body_html': '\n'
                                         '<h2 id="what">কী সুরক্ষিত</h2>\n'
                                         '<p>বায়ার ডিসপিউট করলে এবং আপনি নিচের প্রতিটি ধাপ মানলে, SGT '
                                         'কার্ট\n'
                                         'আপনার পরিবর্তে loss cover করে:</p>\n'
                                         '<ul>\n'
                                         '  <li>"Item not received" — কুরিয়ার proof-of-ডেলিভারি file-এ '
                                         'থাকলে।</li>\n'
                                         '  <li>"Item significantly not as described" — যেখানে আপনার '
                                         'লিস্টিং\n'
                                         '  (ছবি, স্পেক, dimensions) দাবিটি objectively খণ্ডন করে।</li>\n'
                                         '  <li>Cash-on-ডেলিভারি package ডিসপ্যাচ-এর পর বায়ার refuse করলে\n'
                                         "  (return-leg শিপিং charge মাসে দু'বার পর্যন্ত waive)।</li>\n"
                                         '</ul>\n'
                                         '\n'
                                         '<h2 id="requirements">Eligibility</h2>\n'
                                         '<ol>\n'
                                         '  <li>শপ <em>Active</em> স্ট্যাটাস-এ থাকতে হবে, কোনো open পলিসি '
                                         'violation নেই।</li>\n'
                                         '  <li>অর্ডার SGT-অনুমোদিত কুরিয়ার-এ শিপ হয়েছে (signed POD '
                                         'সংরক্ষিত)।</li>\n'
                                         '  <li>লিস্টিং ডেলিভার্ড পণ্যের সঙ্গে সঠিকভাবে মিলেছে — ছবি, স্পেক, '
                                         'condition।</li>\n'
                                         '  <li>ডিসপিউট open হওয়ার ২৪ ঘণ্টার মধ্যে আপনি reply করেছেন।</li>\n'
                                         '</ol>\n'
                                         '\n'
                                         '<h2 id="process">Claim প্রক্রিয়া</h2>\n'
                                         '<p>ডিসপিউট automatically <a href="/seller/disputes/">ডিসপিউট</a>\n'
                                         'tab-এ open হয়। এভিডেন্স সহ reply করুন (কুরিয়ার slip, packaging '
                                         'ফটো,\n'
                                         'chat history)। আমাদের টিম\n'
                                         '<a href="/dispute-resolution/">ডিসপিউট-resolution পলিসি</a> '
                                         'অনুসরণ\n'
                                         'করে ৫ কর্মদিবস-র মধ্যে adjudicate করে।</p>\n'
                                         '\n'
                                         '<h2 id="excluded">যা অন্তর্ভুক্ত নয়</h2>\n'
                                         '<ul>\n'
                                         '  <li>IP infringement বা counterfeit goods-এর জন্য flagged '
                                         'লিস্টিং।</li>\n'
                                         '  <li>তিন বা তার বেশি open পলিসি strike আছে এমন শপ।</li>\n'
                                         '  <li>SGT-অনুমোদিত কুরিয়ার bypass করে self-শিপড অর্ডার।</li>\n'
                                         '  <li>Custom / made-to-অর্ডার পণ্য — যদি না explicitly insure করা '
                                         'থাকে।</li>\n'
                                         '</ul>\n',
                            'faq': [{'q': 'ডিসপ্যাচ-এর পর কতদিন পর্যন্ত protection কাজ করে?',
                                     'a': 'কুরিয়ার স্ক্যান-out date থেকে ৩০ দিন, বা ডেলিভারি-র পর ৭ দিন — '
                                          'যেটি আগে আসে।'},
                                    {'q': 'Enroll-এর জন্য কি পেমেন্ট দিতে হবে?',
                                     'a': 'না। সেলার প্রোটেকশন প্রতিটি active SGT কার্ট শপ-এর সঙ্গে অতিরিক্ত '
                                          'খরচ ছাড়াই অন্তর্ভুক্ত।'}],
                            'related': [{'href': '/dispute-resolution/',
                                         'title': 'বিরোধ নিষ্পত্তি',
                                         'desc': 'বায়ার-সেলার conflict adjudication।'},
                                        {'href': '/sell/code-of-conduct/',
                                         'title': 'আচরণবিধি',
                                         'desc': 'সেলার আচরণের প্রত্যাশা।'},
                                        {'href': '/sell/payouts/',
                                         'title': 'পেআউট',
                                         'desc': 'Win হলে যেভাবে credit হয়।'}]},
 'sell/code-of-conduct': {'title': 'সেলার আচরণবিধি',
                          'subtitle': 'প্রতিটি SGT কার্ট সেলার যে professional মান গ্রহণ করেন।',
                          'section': 'সেলার রিসোর্স',
                          'toc': [{'anchor': 'honesty', 'label': 'লিস্টিং-এ সততা'},
                                  {'anchor': 'service', 'label': 'Service মান'},
                                  {'anchor': 'behaviour', 'label': 'যোগাযোগ'},
                                  {'anchor': 'competition', 'label': 'Fair competition'},
                                  {'anchor': 'consequences', 'label': 'ফলাফল'}],
                          'body_html': '\n'
                                       '<h2 id="honesty">লিস্টিং-এ সততা</h2>\n'
                                       '<ul>\n'
                                       '  <li>নিজের পণ্যের ছবি বা সঠিক licensing-সহ ছবি ব্যবহার করুন।</li>\n'
                                       '  <li>Condition সঠিকভাবে বলুন (new, refurbished, used)।</li>\n'
                                       '  <li>Fake ডিসকাউন্ট দেখাতে original price বাড়িয়ে দেখাবেন '
                                       'না।</li>\n'
                                       '  <li>সব ভ্যারিয়েন্ট, ফি ও lead-time আগে থেকেই উল্লেখ করুন।</li>\n'
                                       '</ul>\n'
                                       '\n'
                                       '<h2 id="service">Service মান</h2>\n'
                                       '<ul>\n'
                                       '  <li>আপনি যে lead-time commit করেছেন তার মধ্যে ডিসপ্যাচ করুন\n'
                                       '  (সাধারণত ২৪-৪৮ ঘণ্টা)।</li>\n'
                                       '  <li>On-time-ডেলিভারি ৯০%-এর উপরে এবং অর্ডার-defect rate ২%-এর নিচে '
                                       'রাখুন।</li>\n'
                                       '  <li>বায়ার chat-এ এক কর্মদিবস-র মধ্যে reply করুন।</li>\n'
                                       '  <li>প্রকাশিত রিটার্ন পলিসি harassment ছাড়াই সম্মান করুন।</li>\n'
                                       '</ul>\n'
                                       '\n'
                                       '<h2 id="behaviour">যোগাযোগ</h2>\n'
                                       '<p>সব communication SGT কার্ট-এর মধ্যেই হতে হবে। ফোন number,\n'
                                       'external লিংক শেয়ার করা, বা off-platform ট্রানজ্যাকশন-এ বায়ার-কে '
                                       'আহ্বান\n'
                                       'করা — উভয়ই violation। এটি safety এবং বায়ার-protection programme\n'
                                       'কার্যকর রাখার জন্য।</p>\n'
                                       '\n'
                                       '<h2 id="competition">Fair competition</h2>\n'
                                       '<ul>\n'
                                       '  <li>নিজের বা প্রতিযোগী লিস্টিং-এ রিভিউ manipulate করবেন না।</li>\n'
                                       '  <li>Strike বা ban এড়াতে একাধিক শপ চালাবেন না।</li>\n'
                                       '  <li>নিজের পণ্য bid up করা বা fake-অর্ডার scheme নিষিদ্ধ।</li>\n'
                                       '</ul>\n'
                                       '\n'
                                       '<h2 id="consequences">ফলাফল</h2>\n'
                                       '<p>১২ মাসে তিন strike → ৩০ দিন suspension। গুরুতর violation (IP '
                                       'চুরি,\n'
                                       'fraud, repeated বায়ার harassment) → permanent শপ closure। এপিল\n'
                                       'process আমাদের <a href="/dispute-resolution/">বিরোধ নিষ্পত্তি</a>\n'
                                       'পেজে বর্ণিত।</p>\n',
                          'related': [{'href': '/seller-terms/',
                                       'title': 'সেলার Agreement',
                                       'desc': 'Binding legal terms।'},
                                      {'href': '/sell/prohibited-items/',
                                       'title': 'নিষিদ্ধ পণ্য',
                                       'desc': 'যা list করা যাবে না।'},
                                      {'href': '/sell/seller-protection/',
                                       'title': 'সেলার প্রোটেকশন',
                                       'desc': 'কখন SGT কার্ট loss absorb করে।'}]},
 'accessibility': {'title': 'Accessibility বিবৃতি',
                   'subtitle': 'SGT কার্ট সবাইকে — assistive technology user-সহ — সহজে ব্যবহারযোগ্য রাখার '
                               'প্রতিশ্রুতি।',
                   'section': 'Company',
                   'toc': [{'anchor': 'commitment', 'label': 'আমাদের প্রতিশ্রুতি'},
                           {'anchor': 'standards', 'label': 'যে standards মেনে চলি'},
                           {'anchor': 'features', 'label': 'Accessibility features'},
                           {'anchor': 'feedback', 'label': 'Feedback ও সাহায্য'}],
                   'body_html': '\n'
                                '<h2 id="commitment">আমাদের প্রতিশ্রুতি</h2>\n'
                                '<p>SGT কার্ট এমনভাবে তৈরি ও maintain করা হয় যাতে বাংলাদেশের সবাই —\n'
                                'assistive technology ব্যবহারকারী বা low-bandwidth connection-এর\n'
                                'user-ও — ব্যবহার করতে পারেন। Accessibility আমাদের কাছে একটি ongoing\n'
                                'engineering priority, এক-বারের audit নয়।</p>\n'
                                '\n'
                                '<h2 id="standards">যে standards মেনে চলি</h2>\n'
                                '<p>আমরা web storefront ও সেলার ড্যাশবোর্ড-এর জন্য <strong>WCAG 2.1\n'
                                'Level AA</strong> target করি। যেখানে কোনো পেজ পিছিয়ে আছে, সেখানে\n'
                                'user impact অনুযায়ী fix priority দিই।</p>\n'
                                '\n'
                                '<h2 id="features">Accessibility features</h2>\n'
                                '<ul>\n'
                                '  <li>প্রতিটি interactive control-এ keyboard navigation।</li>\n'
                                '  <li>লিংক, বাটন ও form field-এ visible focus ইন্ডিকেটর।</li>\n'
                                '  <li>প্রোডাক্ট ফটো-তে alt-টেক্সট (সেলার-দের কাছেও আমরা সেটি চাই)।</li>\n'
                                '  <li>Body copy ও primary action-এ পর্যাপ্ত colour contrast।</li>\n'
                                '  <li>প্রতিটি পেজে বাংলা ও English language toggle।</li>\n'
                                '  <li>৩২০px wide পর্যন্ত reflow করে mobile-first responsive layout।</li>\n'
                                '</ul>\n'
                                '\n'
                                '<h2 id="feedback">Feedback ও সাহায্য</h2>\n'
                                '<p>কোনো পেজে barrier পেলে পেজের URL ও যে সমস্যা হয়েছে তা উল্লেখ করে\n'
                                '<a href="mailto:accessibility@sgtcart.com">accessibility@sgtcart.com</a>-এ\n'
                                'ইমেইল করুন। আমরা ২ কর্মদিবস-র মধ্যে acknowledge করি ও use blocking\n'
                                'সমস্যা-গুলো ৩০ দিনের মধ্যে fix-এর target রাখি।</p>\n',
                   'related': [{'href': '/contact/', 'title': 'যোগাযোগ করুন', 'desc': 'সব সাপোর্ট চ্যানেল।'},
                               {'href': '/privacy/',
                                'title': 'Privacy',
                                'desc': 'আপনার data কীভাবে handle করা হয়।'},
                               {'href': '/help/',
                                'title': 'সাহায্য কেন্দ্র',
                                'desc': 'সেলফ-সার্ভিস আর্টিকেল।'}]},
 'governing-law': {'title': 'প্রযোজ্য আইন ও Jurisdiction',
                   'subtitle': 'SGT কার্ট-সম্পর্কিত বিরোধে কোন আইন প্রযোজ্য।',
                   'section': 'Legal',
                   'toc': [{'anchor': 'law', 'label': 'প্রযোজ্য আইন'},
                           {'anchor': 'venue', 'label': 'Exclusive venue'},
                           {'anchor': 'currency', 'label': 'Currency'},
                           {'anchor': 'consumer', 'label': 'Consumer অধিকার'}],
                   'body_html': '\n'
                                '<h2 id="law">প্রযোজ্য আইন</h2>\n'
                                '<p>SGT কার্ট-এ সমস্ত ট্রানজ্যাকশন এবং বায়ার, সেলার ও SGT কার্ট-এর\n'
                                'মধ্যকার সম্পর্ক <strong>গণপ্রজাতন্ত্রী বাংলাদেশের</strong> আইন\n'
                                'দ্বারা পরিচালিত — কোনো conflict-of-law নীতি বিবেচনা না করেই।</p>\n'
                                '\n'
                                '<h2 id="venue">Exclusive venue</h2>\n'
                                '<p>আমাদের <a href="/dispute-resolution/">বিরোধ নিষ্পত্তি</a> পেজে\n'
                                'উল্লিখিত binding arbitration clause-এর সাপেক্ষে, SGT কার্ট সংক্রান্ত\n'
                                'যেকোনো court proceeding শুধুমাত্র <strong>ঢাকা, বাংলাদেশের</strong>\n'
                                'সক্ষম আদালতে আনতে হবে। উভয় পক্ষ সেখানে personal jurisdiction\n'
                                'স্বীকার করে।</p>\n'
                                '\n'
                                '<h2 id="currency">Currency</h2>\n'
                                '<p>SGT কার্ট-এর সমস্ত price, ফি ও সেটেলমেন্ট\n'
                                '<strong>বাংলাদেশি টাকা (BDT, ৳)</strong>-তে denominate। আমরা বর্তমানে\n'
                                'multi-currency pricing বা international সেটেলমেন্ট প্রস্তাব করি না।</p>\n'
                                '\n'
                                '<h2 id="consumer">Consumer অধিকার</h2>\n'
                                '<p>আমাদের কোনো terms-ই বাংলাদেশ Consumer Rights Protection Act, 2009\n'
                                'বা তার successor legislation-এর অধীনে আপনার non-waivable statutory\n'
                                'অধিকার সীমিত করে না।</p>\n',
                   'related': [{'href': '/terms/',
                                'title': 'কাস্টমার Terms',
                                'desc': 'বায়ার-side contract।'},
                               {'href': '/seller-terms/',
                                'title': 'সেলার Agreement',
                                'desc': 'সেলার-side contract।'},
                               {'href': '/dispute-resolution/',
                                'title': 'বিরোধ নিষ্পত্তি',
                                'desc': 'Arbitration framework।'}]},
 'careers': {'title': 'SGT কার্ট-এ ক্যারিয়ার',
             'subtitle': 'বাংলাদেশের সবচেয়ে নির্ভরযোগ্য marketplace গড়তে আমাদের সঙ্গে যোগ দিন।',
             'section': 'Company',
             'toc': [{'anchor': 'why', 'label': 'কেন SGT কার্ট'},
                     {'anchor': 'openings', 'label': 'বর্তমান openings'},
                     {'anchor': 'apply', 'label': 'কীভাবে apply করবেন'},
                     {'anchor': 'internships', 'label': 'Internships'}],
             'body_html': '\n'
                          '<h2 id="why">কেন SGT কার্ট</h2>\n'
                          '<p>SGT কার্ট Smart Global Trade group-এর অংশ — একটি বাংলাদেশি\n'
                          'technology group যা আমাদের home market-এ online commerce-এর digital\n'
                          'backbone গড়ে তুলছে। আমরা ছোট, senior একটি টিম — যেখানে\n'
                          'craftsmanship, fast iteration ও outcome ownership-এর গুরুত্ব দেওয়া\n'
                          'হয়।</p>\n'
                          '\n'
                          '<h2 id="openings">বর্তমান openings</h2>\n'
                          '<p>নিচের function-গুলোতে আমরা ধারাবাহিকভাবে hire করি। নির্দিষ্ট role\n'
                          'list-এ না থাকলেও strong CV পাঠান — ভালো application আমরা file-এ\n'
                          'রাখি।</p>\n'
                          '<ul>\n'
                          '  <li><strong>Engineering</strong> — Python / Flask, Flutter (mobile), '
                          'DevOps।</li>\n'
                          '  <li><strong>Operations</strong> — সেলার success, logistics, কুরিয়ার '
                          'coordination।</li>\n'
                          '  <li><strong>কাস্টমার সাপোর্ট</strong> — Bilingual (বাংলা + English) chat ও '
                          'voice।</li>\n'
                          '  <li><strong>Trust ও Safety</strong> — পলিসি enforcement ও ডিসপিউট '
                          'analyst।</li>\n'
                          '  <li><strong>Marketing</strong> — Performance, content ও ব্র্যান্ড।</li>\n'
                          '</ul>\n'
                          '\n'
                          '<h2 id="apply">কীভাবে apply করবেন</h2>\n'
                          '<p>আপনার CV, কী কাজে দক্ষ তার সংক্ষিপ্ত note, ও আপনি গর্ববোধ করেন\n'
                          'এমন কিছু লিংক-সহ\n'
                          '<a href="mailto:careers@sgtcart.com">ক্যারিয়ার@sgtcart.com</a>-এ ইমেইল\n'
                          'করুন। আমরা প্রতিটি ইমেইল-এর উত্তর দিই — সাধারণত ৫ কর্মদিবস-র\n'
                          'মধ্যে।</p>\n'
                          '\n'
                          '<h2 id="internships">Internships</h2>\n'
                          '<p>বাংলাদেশি বিশ্ববিদ্যালয়ের final-year undergraduate-রা আমাদের ৩-মাসের\n'
                          'paid internship-এ (engineering ও operations) apply করতে পারেন। Subject\n'
                          'line-এ <em>"Internship"</em> লিখুন।</p>\n',
             'related': [{'href': '/about/', 'title': 'আমাদের সম্পর্কে', 'desc': 'Mission ও founder।'},
                         {'href': '/newsroom/', 'title': 'Newsroom', 'desc': 'সর্বশেষ ঘোষণা।'},
                         {'href': '/contact/',
                          'title': 'যোগাযোগ',
                          'desc': 'আমাদের কাছে পৌঁছানোর অন্য উপায়।'}]},
 'newsroom': {'title': 'Newsroom',
              'subtitle': 'প্রেস release, milestone ও মিডিয়া resource।',
              'section': 'Company',
              'toc': [{'anchor': 'press', 'label': 'প্রেস release'},
                      {'anchor': 'kit', 'label': 'মিডিয়া কিট'},
                      {'anchor': 'contact', 'label': 'প্রেস যোগাযোগ'}],
              'body_html': '\n'
                           '<h2 id="press">প্রেস release</h2>\n'
                           '<p>আমরা formal ঘোষণা publish করি যখন বড় company milestone হয় —\n'
                           'funding round, regulatory অনুমোদন, সেলার-count record, নতুন প্রোডাক্ট\n'
                           'launch। Newsroom RSS feed-এ সাবস্ক্রাইব করুন বা আমাদের distribution\n'
                           'list-এ যুক্ত হতে\n'
                           '<a href="mailto:press@sgtcart.com">প্রেস@sgtcart.com</a>-এ ইমেইল করুন।</p>\n'
                           '\n'
                           '<p><em>এখনো কোনো public release নেই — site-এর এই version-এর সঙ্গেই\n'
                           'আমরা launch করছি। আপডেট-এর জন্য এখানে দেখুন।</em></p>\n'
                           '\n'
                           '<h2 id="kit">মিডিয়া কিট</h2>\n'
                           '<p>আমাদের logo, ব্র্যান্ড colour বা executive photography দরকার?\n'
                           '<a href="mailto:press@sgtcart.com">প্রেস@sgtcart.com</a>-এ ইমেইল করুন,\n'
                           'asset bundle (PNG/SVG logo, ব্র্যান্ড-style PDF, high-resolution ফটো)\n'
                           'শেয়ার করব।</p>\n'
                           '\n'
                           '<h2 id="contact">প্রেস যোগাযোগ</h2>\n'
                           '<p>ইন্টারভিউ, podcast guest বা off-the-record briefing-এর জন্য\n'
                           '<strong>SGT কার্ট Communications</strong>-এ\n'
                           '<a href="mailto:press@sgtcart.com">প্রেস@sgtcart.com</a>-এ যোগাযোগ\n'
                           'করুন। Journalist-দের আমরা weekday-এ ২৪ ঘণ্টার মধ্যে reply করি।</p>\n',
              'related': [{'href': '/about/', 'title': 'আমাদের সম্পর্কে', 'desc': 'Company background।'},
                          {'href': '/careers/', 'title': 'ক্যারিয়ার', 'desc': 'টিম-এ যোগ দিন।'},
                          {'href': '/sustainability/', 'title': 'টেকসইতা', 'desc': 'পরিবেশগত প্রতিশ্রুতি।'}]},
 'sustainability': {'title': 'টেকসইতা',
                    'subtitle': 'Marketplace গড়া যা পৃথিবীর জন্য ক্ষতিকর নয়।',
                    'section': 'Company',
                    'toc': [{'anchor': 'packaging', 'label': 'Packaging'},
                            {'anchor': 'logistics', 'label': 'Logistics'},
                            {'anchor': 'supply', 'label': 'Supply chain'},
                            {'anchor': 'future', 'label': 'ভবিষ্যৎ পরিকল্পনা'}],
                    'body_html': '\n'
                                 '<h2 id="packaging">Packaging</h2>\n'
                                 '<p>আমরা কুরিয়ার partner-দের সঙ্গে single-use plastic mailer ছেড়ে\n'
                                 'recycled-paper alternative-এ যাওয়ার কাজ করছি। আমাদের <em>Green Pack</em>\n'
                                 'programme-এ যোগ দেওয়া সেলার-রা subsidised compostable packaging\n'
                                 'এবং তাদের লিস্টিং-এ "Green Pack" badge পান।</p>\n'
                                 '\n'
                                 '<h2 id="logistics">Logistics</h2>\n'
                                 '<p>যেখানে সম্ভব আমরা একই জেলামুখী অর্ডার একত্রে consolidated run-এ\n'
                                 'শিপ করি। ঢাকার ভেতরে আমরা দুটি কুরিয়ার partner-এর সঙ্গে short-distance\n'
                                 'last-mile ডেলিভারি-র জন্য electric two-wheeler pilot করছি।</p>\n'
                                 '\n'
                                 '<h2 id="supply">Supply chain</h2>\n'
                                 '<p>উচ্চ environmental risk আছে এমন পণ্যের জন্য platform সাপোর্ট\n'
                                 'আমরা সক্রিয়ভাবে কমাচ্ছি — single-use vape kit, microplastic-যুক্ত\n'
                                 'glitter craft kit, এবং disposable thin-film fashion item। এসব\n'
                                 'ক্যাটাগরি-র সেলার-দের আমরা refillable বা higher-quality alternative\n'
                                 'দেওয়ার জন্য উৎসাহিত করি।</p>\n'
                                 '\n'
                                 '<h2 id="future">ভবিষ্যৎ পরিকল্পনা</h2>\n'
                                 '<p>২০২৮ সালের মধ্যে আমাদের লক্ষ্য:</p>\n'
                                 '<ul>\n'
                                 '  <li>SGT কার্ট-পরিচালিত সব warehouse-এ rooftop solar (target: ৬০%\n'
                                 '  on-site generation)।</li>\n'
                                 '  <li>আমাদের top ১০ কুরিয়ার ও warehousing partner-এর সঙ্গে co-signed\n'
                                 '  বার্ষিক sustainability report publish।</li>\n'
                                 '  <li>প্রতিটি অর্ডার-এ default হিসেবে carbon-neutral চেকআউট।</li>\n'
                                 '</ul>\n'
                                 '<p>এটি একটি honest "in-progress" পেজ — আমরা greenwash করব না।\n'
                                 'Real number হাতে এলে এখানে publish করব।</p>\n',
                    'related': [{'href': '/about/',
                                 'title': 'আমাদের সম্পর্কে',
                                 'desc': 'Company background।'},
                                {'href': '/trust-safety/',
                                 'title': 'Trust ও Safety',
                                 'desc': 'Marketplace integrity।'},
                                {'href': '/transparency/',
                                 'title': 'স্বচ্ছতা',
                                 'desc': 'Reporting commitment।'}]},
 'trust-safety': {'title': 'Trust ও Safety',
                  'subtitle': 'বায়ার, সেলার ও platform-কে আমরা কীভাবে নিরাপদ রাখি।',
                  'section': 'Trust & Safety',
                  'toc': [{'anchor': 'pillars', 'label': 'চারটি ভিত্তি'},
                          {'anchor': 'moderation', 'label': 'Content moderation'},
                          {'anchor': 'fraud', 'label': 'Fraud prevention'},
                          {'anchor': 'report', 'label': 'Concern রিপোর্ট করুন'}],
                  'body_html': '\n'
                               '<h2 id="pillars">চারটি ভিত্তি</h2>\n'
                               '<ol>\n'
                               '  <li><strong>Genuine সেলার।</strong> প্রকাশের আগে প্রতিটি শপ\n'
                               '  ভেরিফাইড — জাতীয় পরিচয়পত্র, ট্রেড লাইসেন্স ও bank অ্যাকাউন্ট '
                               'check।</li>\n'
                               '  <li><strong>সৎ লিস্টিং।</strong> Automated check + high-risk\n'
                               '  ক্যাটাগরি-তে human রিভিউ, এবং counterfeit goods-এর ইনস্ট্যান্ট '
                               'takedown।</li>\n'
                               '  <li><strong>Safe ট্রানজ্যাকশন।</strong> Encrypted পেমেন্ট, escrowed\n'
                               '  COD reconciliation, ৭ দিনের রিটার্ন উইন্ডো।</li>\n'
                               '  <li><strong>Respectful community।</strong> রিভিউ, Q&amp;A ও chat সবই\n'
                               '  আমাদের <a href="/sell/code-of-conduct/">আচরণবিধি</a>-র সঙ্গে\n'
                               '  সামঞ্জস্যপূর্ণ।</li>\n'
                               '</ol>\n'
                               '\n'
                               '<h2 id="moderation">Content moderation</h2>\n'
                               '<p>আমরা ML classifier, keyword ফিল্টার ও human রিভিউ একত্রে ব্যবহার\n'
                               'করি। নিষিদ্ধ পণ্যের flag করা লিস্টিং ৪ ঘণ্টার মধ্যে offline করা হয়;\n'
                               'এপিল ৪৮ ঘণ্টায় রিভিউ করা হয়।</p>\n'
                               '\n'
                               '<h2 id="fraud">Fraud prevention</h2>\n'
                               '<p>SGT কার্ট-এর risk engine সন্দেহজনক পেমেন্ট pattern, repeat-chargeback\n'
                               'বায়ার ও wash-trading-এর মতো সেলার activity-র দিকে নজর রাখে।\n'
                               'সিদ্ধান্ত explainable — বায়ার ও সেলার উভয়েই restriction-এর কারণ\n'
                               'জানতে পারেন।</p>\n'
                               '\n'
                               '<h2 id="report">Concern রিপোর্ট করুন</h2>\n'
                               '<p>কিছু দেখেছেন? <a href="/report-illegal/">/report-illegal/</a>-এ\n'
                               'দ্রুত report ফাইল করুন বা\n'
                               '<a href="mailto:trust@sgtcart.com">trust@sgtcart.com</a>-এ ইমেইল\n'
                               'করুন। Critical safety report ১ ঘণ্টার মধ্যে triage হয়।</p>\n',
                  'related': [{'href': '/transparency/', 'title': 'স্বচ্ছতা', 'desc': 'Report ও disclosure।'},
                              {'href': '/anti-counterfeit/',
                               'title': 'নকল পণ্য প্রতিরোধ',
                               'desc': 'ব্র্যান্ড protection programme।'},
                              {'href': '/report-illegal/',
                               'title': 'অবৈধ content রিপোর্ট',
                               'desc': 'Safety report খুলুন।'}]},
 'transparency': {'title': 'স্বচ্ছতা',
                  'subtitle': 'বার্ষিক disclosure, take-down statistics ও government request log।',
                  'section': 'Trust & Safety',
                  'toc': [{'anchor': 'principle', 'label': 'আমাদের নীতি'},
                          {'anchor': 'takedowns', 'label': 'Take-down reporting'},
                          {'anchor': 'requests', 'label': 'Government request'},
                          {'anchor': 'data', 'label': 'Data access log'}],
                  'body_html': '\n'
                               '<h2 id="principle">আমাদের নীতি</h2>\n'
                               '<p>SGT কার্ট একটি তরুণ company, কিন্তু আমরা প্রতিষ্ঠিত global\n'
                               'marketplace-এর সমান transparency standard publicly commit করছি:</p>\n'
                               '<ul>\n'
                               '  <li>বার্ষিক transparency report (প্রথম edition Q1 2027-এ আসবে)।</li>\n'
                               '  <li>প্রাপ্ত প্রতিটি government / law-enforcement request-এর aggregate\n'
                               '  disclosure।</li>\n'
                               '  <li>Platform decision-এ ক্ষতিগ্রস্ত যেকোনো সেলার বা বায়ার-এর জন্য\n'
                               '  স্পষ্ট এপিল path।</li>\n'
                               '</ul>\n'
                               '\n'
                               '<h2 id="takedowns">Take-down reporting</h2>\n'
                               '<p>আমরা ত্রৈমাসিক number publish করি:</p>\n'
                               '<ul>\n'
                               '  <li>IP infringement-এর জন্য সরানো লিস্টিং (reporter type অনুযায়ী)।</li>\n'
                               '  <li>Fraud, harassment বা নিষিদ্ধ পণ্যের জন্য suspended অ্যাকাউন্ট।</li>\n'
                               '  <li>Fake-রিভিউ rule লঙ্ঘনের জন্য সরানো রিভিউ।</li>\n'
                               '</ul>\n'
                               '<p>প্রথম quarter-এর reportable data <strong>এপ্রিল-জুন ২০২৬</strong>\n'
                               'cover করে এবং ১ আগস্ট ২০২৬-এর মধ্যে এখানে প্রকাশিত হবে।</p>\n'
                               '\n'
                               '<h2 id="requests">Government request</h2>\n'
                               '<p>SGT কার্ট বৈধ warrant বা court অর্ডার পেলে বাংলাদেশের law enforcement-এর\n'
                               'সঙ্গে সহযোগিতা করে। Disclosure আইনত প্রয়োজনীয় সর্বনিম্ন data-তে\n'
                               'সীমাবদ্ধ রাখি, অনুমোদিত হলে user-কে জানাই, এবং বার্ষিক report-এর\n'
                               'জন্য প্রতিটি request log করি।</p>\n'
                               '\n'
                               '<h2 id="data">Data access log</h2>\n'
                               '<p>User data-এর internal access ক্ষুদ্রতম সম্ভাব্য টিম-এ সীমিত এবং\n'
                               'রিভিউ-এর জন্য logged। Log ত্রৈমাসিকভাবে স্বাধীন reviewer দ্বারা\n'
                               'audit হয়।</p>\n',
                  'related': [{'href': '/trust-safety/',
                               'title': 'Trust ও Safety',
                               'desc': 'Marketplace integrity overview।'},
                              {'href': '/privacy/',
                               'title': 'Privacy পলিসি',
                               'desc': 'আপনার data কীভাবে ব্যবহৃত হয়।'},
                              {'href': '/governing-law/',
                               'title': 'প্রযোজ্য আইন',
                               'desc': 'Applicable jurisdiction।'}]},
 'report-illegal': {'title': 'অবৈধ content রিপোর্ট',
                    'subtitle': 'SGT কার্ট-কে আইন লঙ্ঘনকারী লিস্টিং, content বা আচরণ সম্পর্কে কীভাবে '
                                'জানাবেন।',
                    'section': 'Trust & Safety',
                    'toc': [{'anchor': 'what', 'label': 'কী illegal বলে গণ্য'},
                            {'anchor': 'how', 'label': 'কীভাবে রিপোর্ট করবেন'},
                            {'anchor': 'anonymous', 'label': 'Anonymous tip'},
                            {'anchor': 'emergency', 'label': 'জরুরি'}],
                    'body_html': '\n'
                                 '<h2 id="what">কী illegal বলে গণ্য</h2>\n'
                                 '<p>কোনো লিস্টিং, রিভিউ, message বা সেলার নিচের কিছু সম্পর্কিত মনে\n'
                                 'হলে অনুগ্রহ করে রিপোর্ট করুন:</p>\n'
                                 '<ul>\n'
                                 '  <li>Counterfeit branded goods বা pirated digital content।</li>\n'
                                 '  <li>অস্ত্র, গোলাবারুদ, বিস্ফোরক বা related parts।</li>\n'
                                 '  <li>Drug (recreational, controlled বা unlicensed prescription)।</li>\n'
                                 '  <li>Child sexual abuse material বা grooming behaviour।</li>\n'
                                 '  <li>Trafficked goods (wildlife, antique, চোরাই গাড়ি ইত্যাদি)।</li>\n'
                                 '  <li>Terrorism financing বা extremist content।</li>\n'
                                 '  <li>হুমকি, harassment বা doxxing।</li>\n'
                                 '</ul>\n'
                                 '\n'
                                 '<h2 id="how">কীভাবে রিপোর্ট করবেন</h2>\n'
                                 '<ol>\n'
                                 '  <li>URL, screenshot ও সংক্ষিপ্ত বিবরণ-সহ\n'
                                 '  <a href="mailto:trust@sgtcart.com">trust@sgtcart.com</a>-এ ইমেইল\n'
                                 '  করুন।</li>\n'
                                 '  <li>আপনি rights-holder হলে IP infringement রিপোর্টের জন্য\n'
                                 '  <a href="/ip-policy/">IP পলিসি</a>-র notice format অনুসরণ করুন।</li>\n'
                                 '  <li>আমরা Severity-1 report ৪ ঘণ্টায় acknowledge ও ২৪ ঘণ্টায় action '
                                 'নিই।</li>\n'
                                 '</ol>\n'
                                 '\n'
                                 '<h2 id="anonymous">Anonymous tip</h2>\n'
                                 '<p>Anonymous report গ্রহণযোগ্য, তবে তদন্তের জন্য যথেষ্ট detail দিন\n'
                                 '(screenshot, URL, তারিখ)। আপনি যোগাযোগ information না দিলে আমরা\n'
                                 'follow-up করতে পারব না।</p>\n'
                                 '\n'
                                 '<h2 id="emergency">জরুরি</h2>\n'
                                 '<p>কেউ immediate physical danger-এ আছেন মনে হলে প্রথমে বাংলাদেশ\n'
                                 'emergency service-এ <strong>৯৯৯</strong>-এ যোগাযোগ করুন, তারপর\n'
                                 'আমাদের জানান।</p>\n',
                    'related': [{'href': '/trust-safety/',
                                 'title': 'Trust ও Safety',
                                 'desc': 'Marketplace নিরাপত্তা।'},
                                {'href': '/anti-counterfeit/',
                                 'title': 'নকল পণ্য প্রতিরোধ',
                                 'desc': 'ব্র্যান্ড protection।'},
                                {'href': '/ip-policy/',
                                 'title': 'IP পলিসি',
                                 'desc': 'Trademark ও copyright প্রক্রিয়া।'}]},
 'anti-counterfeit': {'title': 'নকল পণ্য প্রতিরোধ programme',
                      'subtitle': 'ব্র্যান্ড owner-রা SGT কার্ট-এ তাদের IP কীভাবে সুরক্ষিত রাখেন।',
                      'section': 'Trust & Safety',
                      'toc': [{'anchor': 'commitment', 'label': 'আমাদের প্রতিশ্রুতি'},
                              {'anchor': 'enrol', 'label': 'ব্র্যান্ড enrolment'},
                              {'anchor': 'process', 'label': 'Take-down প্রক্রিয়া'},
                              {'anchor': 'penalties', 'label': 'সেলার penalty'}],
                      'body_html': '\n'
                                   '<h2 id="commitment">আমাদের প্রতিশ্রুতি</h2>\n'
                                   '<p>SGT কার্ট counterfeit লিস্টিং সহ্য করে না। ভেরিফাইড ব্র্যান্ড '
                                   'owner-রা\n'
                                   'আমাদের Anti-Counterfeit Programme-এ register করে expedited takedown,\n'
                                   'proactive লিস্টিং screening ও direct অ্যাকাউন্ট manager পেতে পারেন।</p>\n'
                                   '\n'
                                   '<h2 id="enrol">ব্র্যান্ড enrolment</h2>\n'
                                   '<p>Enroll করতে নিচেরগুলো\n'
                                   '<a '
                                   'href="mailto:brand-protect@sgtcart.com">ব্র্যান্ড-protect@sgtcart.com</a>-এ\n'
                                   'পাঠান:</p>\n'
                                   '<ul>\n'
                                   '  <li>রেজিস্টার্ড trademark সার্টিফিকেট (বাংলাদেশ বা international,\n'
                                   '  WIPO designation-সহ)।</li>\n'
                                   '  <li>ব্র্যান্ড-এর পক্ষে কাজ করার অনুমোদনের proof।</li>\n'
                                   '  <li>একজন primary যোগাযোগ ও authorised escalation list।</li>\n'
                                   '</ul>\n'
                                   '<p>আমরা ৫ কর্মদিবস-র মধ্যে enrolment confirm করি।</p>\n'
                                   '\n'
                                   '<h2 id="process">Take-down প্রক্রিয়া</h2>\n'
                                   '<ol>\n'
                                   '  <li>Enrolled ব্র্যান্ড-রা ব্র্যান্ড পোর্টাল-এর মাধ্যমে (বা পোর্টাল '
                                   'launch\n'
                                   '  পর্যন্ত ইমেইল-এ) takedown request file করেন।</li>\n'
                                   '  <li>Enrolled ব্র্যান্ড-এর request আমরা <strong>২৪ ঘণ্টায়</strong>,\n'
                                   '  non-enrolled rights-holder-এর <strong>৭২ ঘণ্টায়</strong> action '
                                   'নিই।</li>\n'
                                   '  <li>সেলার documented authenticity এভিডেন্স (ইনভয়েস, distributor\n'
                                   '  agreement) সহ ১৪ দিনের মধ্যে এপিল করতে পারেন।</li>\n'
                                   '</ol>\n'
                                   '\n'
                                   '<h2 id="penalties">সেলার penalty</h2>\n'
                                   '<ul>\n'
                                   '  <li><strong>First strike</strong> — লিস্টিং সরানো, written '
                                   'warning।</li>\n'
                                   '  <li><strong>Second strike</strong> — ৩০ দিন suspension, ওয়ালেট '
                                   'হোল্ড।</li>\n'
                                   '  <li><strong>Third strike</strong> — permanent শপ closure; বকেয়া\n'
                                   '  ব্যালেন্স বায়ার রিফান্ড-এর জন্য রিজার্ভ।</li>\n'
                                   '</ul>\n',
                      'related': [{'href': '/ip-policy/',
                                   'title': 'IP পলিসি',
                                   'desc': 'সম্পূর্ণ takedown প্রক্রিয়া।'},
                                  {'href': '/trust-safety/',
                                   'title': 'Trust ও Safety',
                                   'desc': 'Marketplace integrity programme।'},
                                  {'href': '/sell/code-of-conduct/',
                                   'title': 'সেলার আচরণবিধি',
                                   'desc': 'আচরণের মান।'}]},
 'security': {'title': 'নিরাপত্তা',
              'subtitle': 'SGT কার্ট কীভাবে অ্যাকাউন্ট, পেমেন্ট ও platform data সুরক্ষিত রাখে।',
              'section': 'Trust & Safety',
              'toc': [{'anchor': 'account', 'label': 'অ্যাকাউন্ট নিরাপত্তা'},
                      {'anchor': 'payments', 'label': 'পেমেন্ট নিরাপত্তা'},
                      {'anchor': 'platform', 'label': 'Platform নিরাপত্তা'},
                      {'anchor': 'report', 'label': 'Vulnerability রিপোর্ট'}],
              'body_html': '\n'
                           '<h2 id="account">অ্যাকাউন্ট নিরাপত্তা</h2>\n'
                           '<ul>\n'
                           '  <li>পাসওয়ার্ড industry-standard work-factor algorithm-এ hash করা হয়\n'
                           '  — আমরা কখনো plain টেক্সট-এ স্টোর করি না।</li>\n'
                           '  <li>Sensitive action (পেআউট detail পরিবর্তন, data export) করতে\n'
                           '  রেজিস্টার্ড ইমেইল-এ পাঠানো one-time code লাগে।</li>\n'
                           '  <li>Inactivity-র পর session auto-expire হয়, এবং remote session-গুলো\n'
                           '  অ্যাকাউন্ট পেজ থেকে sign-out করা যায়।</li>\n'
                           '</ul>\n'
                           '\n'
                           '<h2 id="payments">পেমেন্ট নিরাপত্তা</h2>\n'
                           '<ul>\n'
                           '  <li>কার্ড পেমেন্ট PCI-DSS-compliant গেটওয়ে (SSLCommerz)-এ process\n'
                           '  হয়। SGT কার্ট কখনো raw কার্ড number স্টোর করে না।</li>\n'
                           '  <li>সমস্ত পেমেন্ট-পেজ traffic end-to-end TLS-encrypted।</li>\n'
                           '  <li>সন্দেহজনক পেমেন্ট pattern ফান্ড রিলিজ-এর আগে automated\n'
                           '  রিভিউ trigger করে।</li>\n'
                           '</ul>\n'
                           '\n'
                           '<h2 id="platform">Platform নিরাপত্তা</h2>\n'
                           '<ul>\n'
                           '  <li>Production server reverse proxy-র পেছনে HSTS, modern TLS ও\n'
                           '  rate-limited public endpoint দিয়ে isolated।</li>\n'
                           '  <li>Internal access least-privilege, MFA-enforced, এবং logged।</li>\n'
                           '  <li>Backup encrypted at rest এবং restorability নিয়মিত test করা হয়।</li>\n'
                           '</ul>\n'
                           '\n'
                           '<h2 id="report">Vulnerability রিপোর্ট</h2>\n'
                           '<p>Security researcher-রা, proof-of-concept ও আপনার যোগাযোগ\n'
                           'detail-সহ <a href="mailto:security@sgtcart.com">security@sgtcart.com</a>-এ\n'
                           'ইমেইল করুন। আমাদের commitment:</p>\n'
                           '<ul>\n'
                           '  <li>২ কর্মদিবস-র মধ্যে acknowledgement।</li>\n'
                           '  <li>Other user-দের impact না করা good-faith research-এর জন্য\n'
                           '  safe-harbour।</li>\n'
                           '  <li>Fix শিপ হওয়ার পর আপনার পছন্দ অনুযায়ী public credit।</li>\n'
                           '</ul>\n',
              'related': [{'href': '/privacy/', 'title': 'Privacy', 'desc': 'আপনার data কীভাবে handle হয়।'},
                          {'href': '/trust-safety/',
                           'title': 'Trust ও Safety',
                           'desc': 'Marketplace integrity।'},
                          {'href': '/transparency/', 'title': 'স্বচ্ছতা', 'desc': 'Reporting commitment।'}]}}
