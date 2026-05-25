"""Public storefront — DB-backed catalog & product detail (Phase 2)."""
from datetime import datetime

from flask import (
    Blueprint, render_template, request, abort, session, jsonify, flash,
    redirect, url_for,
)
from flask_login import current_user

from app.extensions import db, limiter
from app.models.catalog import Product, Category, PRODUCT_PUBLISHED
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.services.review_service import (
    can_review, existing_review,
    rating_distribution, paginated_reviews, review_photos,
    REVIEW_SORT_NEWEST, REVIEW_SORTS, REVIEW_SORT_LABELS,
)
from app.services.flash_sale_service import live_sales
from app.services.search_service import (
    apply_ranking, log_view, log_search, autocomplete,
)
from app.services.recommendation_service import (
    similar_products, also_viewed, frequently_bought_together,
)
from app.services import image_search_service

storefront = Blueprint("storefront", __name__)

PER_PAGE = 40    # Daraz-style: large page, "Load More" instead of 1/2/3 pagination

# Session key for the product-page inline coupon preview (Phase 15 D-5 M2).
# Kept separate from `cart.COUPON_SESSION` so previewing a code on a product
# page doesn't auto-apply it at checkout — the customer still has to add the
# item, then re-apply at checkout.
_PRODUCT_COUPON_SESSION_KEY = "pdp_coupon"


def _capture_affiliate_ref():
    """Remember an affiliate share code (?ref=) so checkout can credit it."""
    ref = request.args.get("ref")
    if ref:
        session["affiliate_ref"] = ref.strip().upper()[:12]


@storefront.route("/shop/")
def shop():
    """Catalog listing — published products with category / search / price filters."""
    page = request.args.get("page", 1, type=int)
    category_slug = (request.args.get("category") or "").strip()
    brand_slug = (request.args.get("brand") or "").strip()
    q = (request.args.get("q") or "").strip()
    min_price = request.args.get("min", type=float)
    max_price = request.args.get("max", type=float)

    query = Product.query.filter_by(status=PRODUCT_PUBLISHED)

    active_category = None
    if category_slug:
        active_category = Category.query.filter_by(slug=category_slug).first()
        if active_category:
            cat_ids = [active_category.id] + [c.id for c in active_category.children]
            query = query.filter(Product.category_id.in_(cat_ids))

    # Phase 15 D-1: brand filter — used by the product page's
    # "More from {brand}" link.
    active_brand = None
    if brand_slug:
        from app.models.catalog import Brand
        active_brand = Brand.query.filter_by(slug=brand_slug).first()
        if active_brand:
            query = query.filter(Product.brand_id == active_brand.id)

    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Product.title_en.ilike(like), Product.title_bn.ilike(like))
        )
    if min_price is not None:
        query = query.filter(Product.base_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.base_price <= max_price)

    # Rank by featured > seller rating (+admin boost) > product rating > recency.
    pagination = apply_ranking(query).paginate(
        page=page, per_page=PER_PAGE, error_out=False
    )
    if q:
        log_search(q, current_user if current_user.is_authenticated else None,
                   pagination.total)

    # `?partial=1` returns just the product cards — used by the Load More button.
    if request.args.get("partial") == "1":
        return render_template("pages/_product_grid_items.html",
                               products=pagination.items)

    categories = (
        Category.query.filter_by(parent_id=None, is_active=True)
        .order_by(Category.sort_order, Category.name_en).all()
    )
    return render_template(
        "pages/shop.html",
        pagination=pagination, products=pagination.items, categories=categories,
        active_category=active_category, active_brand=active_brand,
        q=q, min_price=min_price, max_price=max_price,
    )


@storefront.route("/store/<slug>/")
def store(slug):
    """A seller's public store page — their products with in-store filters."""
    vendor = VendorProfile.query.filter_by(slug=slug, status=VENDOR_APPROVED).first()
    if vendor is None:
        abort(404)
    _capture_affiliate_ref()

    page = request.args.get("page", 1, type=int)
    category_slug = (request.args.get("category") or "").strip()
    q = (request.args.get("q") or "").strip()
    min_price = request.args.get("min", type=float)
    max_price = request.args.get("max", type=float)

    query = Product.query.filter_by(vendor_id=vendor.id, status=PRODUCT_PUBLISHED)

    # Categories this store actually sells in (for the in-store filter).
    cat_ids = [
        row[0] for row in db.session.query(Product.category_id)
        .filter_by(vendor_id=vendor.id, status=PRODUCT_PUBLISHED).distinct()
    ]
    store_categories = (
        Category.query.filter(Category.id.in_(cat_ids)).order_by(Category.name_en).all()
        if cat_ids else []
    )

    active_category = None
    if category_slug:
        active_category = Category.query.filter_by(slug=category_slug).first()
        if active_category:
            query = query.filter(Product.category_id == active_category.id)
    if q:
        like = f"%{q}%"
        query = query.filter(
            db.or_(Product.title_en.ilike(like), Product.title_bn.ilike(like))
        )
    if min_price is not None:
        query = query.filter(Product.base_price >= min_price)
    if max_price is not None:
        query = query.filter(Product.base_price <= max_price)

    pagination = (
        query.order_by(Product.is_featured.desc(), Product.created_at.desc())
        .paginate(page=page, per_page=PER_PAGE, error_out=False)
    )
    product_count = Product.query.filter_by(
        vendor_id=vendor.id, status=PRODUCT_PUBLISHED
    ).count()
    return render_template(
        "pages/store.html", vendor=vendor, products=pagination.items,
        pagination=pagination, store_categories=store_categories,
        active_category=active_category, q=q, min_price=min_price,
        max_price=max_price, product_count=product_count,
    )


@storefront.route("/search/image/", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def search_by_image():
    """Upload an image to find visually similar products."""
    if request.method == "POST":
        upload = request.files.get("image")
        if upload is None or not upload.filename:
            flash("Please choose an image to search with.", "danger")
            return redirect(url_for("storefront.search_by_image"))
        if not image_search_service.is_available():
            flash("Image search is not ready yet — please try again in a minute.",
                  "warning")
            return redirect(url_for("storefront.search_by_image"))
        matches = image_search_service.search_by_image(upload, limit=24)
        return render_template("pages/image-search.html", matches=matches)
    return render_template("pages/image-search.html", matches=None)


@storefront.route("/search/suggest")
@limiter.limit("60 per minute")
def search_suggest():
    """JSON product-title suggestions for the search-box autocomplete."""
    return jsonify({"suggestions": autocomplete(request.args.get("q", ""))})


@storefront.route("/flash-sales/")
def flash_sales():
    """Live flash sales and their discounted products, with search + price filter."""
    q = (request.args.get("q") or "").strip()
    min_price = request.args.get("min", type=float)
    max_price = request.args.get("max", type=float)

    sales = []
    for sale in live_sales():
        items = []
        for it in sale.items:
            p = it.product
            if p is None or not p.is_published:
                continue
            if q and q.lower() not in (p.title_en or "").lower() \
                    and q.lower() not in (p.title_bn or "").lower():
                continue
            price = float(it.flash_price)
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue
            items.append(it)
        if items:
            # Shallow shim: pass a (sale, items) tuple so the template can iterate.
            sales.append((sale, items))

    return render_template("pages/flash-sales.html",
                           sales=sales, q=q,
                           min_price=min_price, max_price=max_price)


@storefront.route("/product/<slug>/")
def product_detail(slug):
    """Public product detail page."""
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        abort(404)
    _capture_affiliate_ref()
    log_view(product, current_user if current_user.is_authenticated else None)
    # Phase 10: similar (content) + also-viewed (collaborative) recommendations.
    related = similar_products(product, limit=8)
    also_viewed_products = also_viewed(product, limit=6)

    # Review eligibility for the "Write a review" call to action.
    user_review = None
    user_can_review = False
    if current_user.is_authenticated:
        user_review = existing_review(current_user, product)
        user_can_review = can_review(current_user, product)

    # Phase 15 D-1 — delivery sidebar + Sold By panel + Buy Now context.
    from datetime import timedelta
    from app.services.settings_service import get_decimal, get_setting
    shipping_fee = get_decimal("shipping_fee_per_vendor")
    free_shipping_threshold = get_decimal("free_shipping_threshold")
    return_policy_days = int(get_decimal("return_policy_days") or 0)
    warranty_text = get_setting("warranty_default") or "No warranty"

    # Phase 15 D-9 — district-wise ETA + same-city seller badge + buyer
    # prayer-time preference + campaign strip + Hijri date.
    from app.services import delivery_eta_service, campaign_service
    from app.services import bd_calendar_service
    buyer_default_address = None
    if current_user.is_authenticated and current_user.addresses:
        buyer_default_address = next(
            (a for a in current_user.addresses if a.is_default),
            current_user.addresses[0],
        )
    eta_min_days, eta_max_days, eta_district = delivery_eta_service.eta_for_address(
        buyer_default_address,
    )
    # Slow sellers ship later — bake their avg delivery time into the upper bound.
    if product.vendor and product.vendor.avg_delivery_days:
        eta_max_days = max(eta_max_days,
                           int(round(float(product.vendor.avg_delivery_days)) + 1))
    eta_start = datetime.utcnow() + timedelta(days=eta_min_days)
    eta_end = datetime.utcnow() + timedelta(days=eta_max_days)

    # Same-city seller badge (case-insensitive match).
    same_city_seller = False
    if (buyer_default_address and product.vendor
            and (product.vendor.city or "").strip()
            and (buyer_default_address.city or "").strip()):
        same_city_seller = (
            buyer_default_address.city.strip().lower()
            == product.vendor.city.strip().lower()
        )
    prayer_time_pref = (
        bool(buyer_default_address and buyer_default_address.prayer_time_delivery)
    )

    campaign = campaign_service.active_campaign()
    hijri_label = bd_calendar_service.format_hijri_and_gregorian(datetime.utcnow())

    # Phase 15 D-10 — promotional polish: inline flash-sale strip + app QR.
    from app.services import flash_sale_service, app_download_service
    active_flash_sale = flash_sale_service.active_sale_for_product(product)
    app_url = app_download_service.app_download_url()
    app_qr_url = app_download_service.qr_image_url(app_url) if app_url else None

    # "More from <brand>" preview — a few sibling products under the same brand.
    brand_more = []
    if product.brand_id:
        brand_more = (
            Product.query.filter(
                Product.brand_id == product.brand_id,
                Product.status == PRODUCT_PUBLISHED,
                Product.id != product.id,
            ).order_by(Product.is_featured.desc(), Product.id.desc()).limit(6).all()
        )

    # Phase 15 D-2 — public Q&A surface.
    from app.services import qa_service
    qa_questions = qa_service.public_questions(product)
    qa_answered = qa_service.answered_count(product)
    voted_answers = qa_service.voted_answer_ids(
        current_user if current_user.is_authenticated else None, product,
    )

    # Phase 15 D-8 — smart helpers: FBT bundle, cached AI pros/cons.
    from app.services import ai_summary_service
    fbt_products = frequently_bought_together(product, limit=4)
    ai_pros = ai_summary_service.pros(product)
    ai_cons = ai_summary_service.cons(product)

    # Phase 15 D-6 — urgency & inventory signals: record this viewer +
    # compute sold-in-last-24h + pending back-in-stock subscribers.
    from app.services import presence_service, stock_service
    viewer_key = (current_user.id if current_user.is_authenticated
                  else session.get("sid"))
    if viewer_key is None:
        # Anonymous: lazily set a stable session id without depending on
        # Flask's signed-cookie id (which may rotate).
        from secrets import token_hex
        session["sid"] = token_hex(8)
        viewer_key = session["sid"]
    presence_service.record_view(product.id, viewer_key)
    viewing_now = presence_service.active_viewers(product.id)
    sold_24h = stock_service.units_sold_recent(product, hours=24)
    stock_subscriber_count = stock_service.pending_count_for_product(product)

    # Phase 15 D-4 — seller trust stats for the "Why buy from this seller?"
    # card + bilingual verification badges.
    from app.services import vendor_stats_service
    trust = vendor_stats_service.trust_stats(product.vendor)

    # Phase 15 D-7 — chat presence indicator on the Sold-By panel.
    from app.services import presence_service
    from app.services.quick_questions import QUICK_QUESTIONS
    seller_is_online = False
    seller_last_seen = None
    if product.vendor and product.vendor.user_id:
        seller_is_online = presence_service.is_user_online(product.vendor.user_id)
        if not seller_is_online and product.vendor.user is not None:
            seller_last_seen = product.vendor.user.last_seen_at

    # Phase 15 D-5 — money & loyalty inline.
    from app.services import pricing_service, reward_service, referral_service
    from app.services.reward_service import TAKA_PER_POINT
    bulk_tiers = pricing_service.tier_preview(product)
    earn_points_preview = int(product.current_price // TAKA_PER_POINT) if product.current_price else 0
    user_points_balance = 0
    user_points_value = None
    if current_user.is_authenticated:
        user_points_balance = reward_service.balance(current_user)
        if user_points_balance > 0:
            user_points_value = reward_service.points_value(user_points_balance)
    # Affiliate link — only logged-in users; sellers don't promote their own
    # product to themselves.
    affiliate_link = None
    if current_user.is_authenticated and product.vendor \
            and product.vendor.user_id != current_user.id:
        code = referral_service.ensure_code(current_user)
        affiliate_link = url_for(
            "storefront.product_detail", slug=product.slug, ref=code,
            _external=True,
        )
    # Inline coupon — session-scoped preview state lives under this key so it
    # doesn't pollute the checkout-flow coupon (session["checkout_coupon"]).
    coupon_preview = session.get(_PRODUCT_COUPON_SESSION_KEY)
    if coupon_preview and coupon_preview.get("product_id") != product.id:
        # Customer navigated to a different product; clear the preview.
        coupon_preview = None
        session.pop(_PRODUCT_COUPON_SESSION_KEY, None)

    # Phase 15 D-3 — reviews: distribution, sort, star filter, pagination,
    # photo gallery aggregated from ReviewImage rows.
    review_sort = request.args.get("rsort", REVIEW_SORT_NEWEST)
    if review_sort not in REVIEW_SORTS:
        review_sort = REVIEW_SORT_NEWEST
    try:
        review_star = int(request.args.get("rstar")) if request.args.get("rstar") else None
        if review_star not in (1, 2, 3, 4, 5):
            review_star = None
    except (TypeError, ValueError):
        review_star = None
    review_page = request.args.get("rpage", 1, type=int) or 1
    review_dist = rating_distribution(product)
    review_pagination = paginated_reviews(
        product, sort=review_sort, star_filter=review_star, page=review_page,
    )
    review_gallery = review_photos(product, limit=24)

    return render_template(
        "pages/product.html", product=product, related=related,
        also_viewed=also_viewed_products,
        user_review=user_review, user_can_review=user_can_review,
        shipping_fee=shipping_fee,
        free_shipping_threshold=free_shipping_threshold,
        return_policy_days=return_policy_days,
        warranty_text=warranty_text,
        eta_min_days=eta_min_days, eta_max_days=eta_max_days,
        eta_start=eta_start, eta_end=eta_end,
        eta_district=eta_district,
        same_city_seller=same_city_seller,
        prayer_time_pref=prayer_time_pref,
        campaign=campaign, hijri_label=hijri_label,
        active_flash_sale=active_flash_sale,
        app_download_url=app_url, app_qr_url=app_qr_url,
        brand_more=brand_more,
        qa_questions=qa_questions, qa_answered_count=qa_answered,
        voted_answers=voted_answers,
        fbt_products=fbt_products, ai_pros=ai_pros, ai_cons=ai_cons,
        viewing_now=viewing_now, sold_24h=sold_24h,
        stock_subscriber_count=stock_subscriber_count,
        trust=trust,
        seller_is_online=seller_is_online,
        seller_last_seen=seller_last_seen,
        quick_questions=QUICK_QUESTIONS,
        bulk_tiers=bulk_tiers,
        earn_points_preview=earn_points_preview,
        user_points_balance=user_points_balance,
        user_points_value=user_points_value,
        affiliate_link=affiliate_link,
        coupon_preview=coupon_preview,
        review_dist=review_dist, review_sort=review_sort,
        review_star=review_star, review_sorts=REVIEW_SORTS,
        review_sort_labels=REVIEW_SORT_LABELS,
        review_pagination=review_pagination,
        review_gallery=review_gallery,
    )


@storefront.route("/product/<slug>/notify-stock", methods=["POST"])
@limiter.limit("10 per minute")
def product_notify_stock(slug):
    """Subscribe an email for a back-in-stock alert (Phase 15 D-6)."""
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        abort(404)
    from app.services import stock_service
    email = (request.form.get("email") or "").strip()
    user = current_user if current_user.is_authenticated else None
    _, error = stock_service.subscribe(product, user, email)
    if error:
        flash(error, "danger")
    else:
        flash("We'll email you when this product is back in stock.", "success")
    return redirect(url_for("storefront.product_detail", slug=slug) + "#urgency")


@storefront.route("/product/<slug>/apply-coupon", methods=["POST"])
@limiter.limit("20 per minute")
def product_apply_coupon(slug):
    """Inline coupon preview on the product page (Phase 15 D-5 M2).

    Validates the coupon against a one-item preview cart (this product at
    quantity 1). Saves the result in a product-scoped session key — does
    NOT touch the checkout-flow coupon. Customer still needs to apply at
    checkout to actually consume it.
    """
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        abort(404)
    code = (request.form.get("coupon_code") or "").strip()
    action = (request.form.get("action") or "").strip()

    if action == "clear":
        session.pop(_PRODUCT_COUPON_SESSION_KEY, None)
        flash("Coupon cleared.", "info")
        return redirect(url_for("storefront.product_detail", slug=slug) + "#money")

    if not current_user.is_authenticated:
        flash("Please log in to apply a coupon.", "warning")
        return redirect(url_for("auth.login"))

    # Build a 1-item "preview cart" — `validate_coupon` only reads
    # `line_total` and `product` off each item.
    from decimal import Decimal
    from types import SimpleNamespace
    from app.services.coupon_service import validate_coupon
    preview_item = SimpleNamespace(
        product=product,
        line_total=Decimal(product.current_price or 0),
    )
    coupon, discount, error = validate_coupon(code, current_user, [preview_item])
    if error:
        session.pop(_PRODUCT_COUPON_SESSION_KEY, None)
        flash(error, "danger")
    else:
        session[_PRODUCT_COUPON_SESSION_KEY] = {
            "product_id": product.id,
            "code": coupon.code,
            "discount": str(discount),
        }
        flash(f"Coupon '{coupon.code}' would save Tk {discount} on this product "
              "at checkout.", "success")
    return redirect(url_for("storefront.product_detail", slug=slug) + "#money")


@storefront.route("/product/<slug>/qa/ask", methods=["POST"])
def qa_ask(slug):
    """Public: a logged-in user asks a question on a product."""
    if not current_user.is_authenticated:
        flash("Please log in to ask a question.", "warning")
        return redirect(url_for("auth.login", next=request.referrer or "/"))
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        abort(404)
    from app.services import qa_service
    _, error = qa_service.ask_question(
        current_user, product, request.form.get("body", "")
    )
    if error:
        flash(error, "danger")
    else:
        flash("Your question is posted — the seller will answer soon.", "success")
    return redirect(url_for("storefront.product_detail", slug=slug) + "#qa")


@storefront.route("/product/<slug>/qa/answer/<int:answer_id>/helpful",
                  methods=["POST"])
@limiter.limit("30 per minute")
def qa_answer_helpful(slug, answer_id):
    """Toggle a helpful-vote on a Q&A answer (Phase 15 D-8 C6)."""
    if not current_user.is_authenticated:
        flash("Please log in to vote.", "warning")
        return redirect(url_for("auth.login", next=request.referrer or "/"))
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        abort(404)
    from app.models.qa import Answer, Question
    from app.services import qa_service
    answer = db.session.get(Answer, answer_id)
    if (answer is None
            or answer.question is None
            or answer.question.product_id != product.id):
        abort(404)
    qa_service.toggle_helpful(current_user, answer)
    return redirect(url_for("storefront.product_detail", slug=slug) + "#qa")


@storefront.route("/product/<slug>/qa/<int:question_id>/answer", methods=["POST"])
def qa_answer(slug, question_id):
    """Public: anyone logged-in (typically the seller) answers a question."""
    if not current_user.is_authenticated:
        flash("Please log in to answer.", "warning")
        return redirect(url_for("auth.login", next=request.referrer or "/"))
    product = Product.query.filter_by(slug=slug, status=PRODUCT_PUBLISHED).first()
    if product is None:
        abort(404)
    from app.models.qa import Question
    question = db.session.get(Question, question_id)
    if question is None or question.product_id != product.id:
        abort(404)
    from app.services import qa_service
    _, error = qa_service.post_answer(
        current_user, question, request.form.get("body", "")
    )
    if error:
        flash(error, "danger")
    else:
        flash("Your answer is posted.", "success")
    return redirect(url_for("storefront.product_detail", slug=slug) + "#qa")
