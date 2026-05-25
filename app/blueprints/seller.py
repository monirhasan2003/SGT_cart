"""Seller area — Phase 1.

Dashboard + shop verification (KYC). A seller submits trade-license / NID
documents and shop details; an admin reviews them before approving the shop.
Full product management, orders and analytics arrive in Phase 2 / Phase 5.
"""
from datetime import datetime
from decimal import Decimal

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from slugify import slugify

from app.extensions import db
from app.models.catalog import (
    Product, ProductVariant, ProductImage, ProductSpec, ProductPriceTier,
    Category,
    PRODUCT_DRAFT, PRODUCT_PENDING, PRODUCT_PUBLISHED, PRODUCT_REJECTED,
)
from app.models.order import SubOrder, SUBORDER_STATUSES, SUBORDER_DELIVERED
from app.models.review import Review
from app.models.marketing import Coupon, COUPON_VENDOR, FlashSale, FlashSaleItem
from app.services import flash_sale_service
from app.models.wallet import PayoutRequest
from app.services.coupon_service import parse_coupon_form, coupon_form_dict
from app.services.analytics_service import seller_metrics
from app.services.wallet_service import get_or_create_wallet, hold_for_payout
from app.services.order_service import update_suborder_status
from app.utils.decorators import seller_required, approved_vendor_required
from app.utils.uploads import save_upload, is_allowed_doc, has_file

seller = Blueprint("seller", __name__, url_prefix="/seller")

BUSINESS_TYPES = ("Individual", "Company")


@seller.route("/")
@login_required
@seller_required
def dashboard():
    return render_template("seller/dashboard.html", profile=current_user.vendor_profile)


@seller.route("/verification", methods=["GET", "POST"])
@login_required
@seller_required
def verification():
    """Submit / update shop verification documents (KYC)."""
    profile = current_user.vendor_profile
    if profile is None:
        flash("Seller profile not found.", "danger")
        return redirect(url_for("seller.dashboard"))

    if profile.is_approved:
        flash("Your shop is already approved — verification cannot be changed.", "info")
        return redirect(url_for("seller.dashboard"))

    if request.method == "POST":
        business_type = (request.form.get("business_type") or "").strip()
        address = (request.form.get("address") or "").strip()
        city = (request.form.get("city") or "").strip()
        trade_license_no = (request.form.get("trade_license_no") or "").strip()
        nid_number = (request.form.get("nid_number") or "").strip()
        description = (request.form.get("description_en") or "").strip()

        tl_file = request.files.get("trade_license_doc")
        nid_file = request.files.get("nid_doc")

        errors = []
        if business_type not in BUSINESS_TYPES:
            errors.append("Please select a valid business type.")
        if not address:
            errors.append("Shop address is required.")
        if not city:
            errors.append("City is required.")
        if not trade_license_no:
            errors.append("Trade license number is required.")
        if not nid_number:
            errors.append("NID number is required.")
        if has_file(tl_file) and not is_allowed_doc(tl_file.filename):
            errors.append("Trade license file must be a PDF, JPG or PNG.")
        if has_file(nid_file) and not is_allowed_doc(nid_file.filename):
            errors.append("NID file must be a PDF, JPG or PNG.")
        if not has_file(tl_file) and not profile.trade_license_doc:
            errors.append("Please upload the trade license document.")
        if not has_file(nid_file) and not profile.nid_doc:
            errors.append("Please upload the NID document.")

        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("seller/verification.html", profile=profile, form=request.form)

        profile.business_type = business_type
        profile.address = address
        profile.city = city
        profile.trade_license_no = trade_license_no
        profile.nid_number = nid_number
        if description:
            profile.description_en = description

        tl_path = save_upload(tl_file, "vendor_docs")
        if tl_path:
            profile.trade_license_doc = tl_path
        nid_path = save_upload(nid_file, "vendor_docs")
        if nid_path:
            profile.nid_doc = nid_path

        profile.verification_submitted_at = datetime.utcnow()
        db.session.commit()
        flash("Verification details submitted. An admin will review your shop.", "success")
        return redirect(url_for("seller.dashboard"))

    return render_template(
        "seller/verification.html", profile=profile, form={}, business_types=BUSINESS_TYPES
    )


@seller.route("/payout", methods=["GET", "POST"])
@login_required
@seller_required
def payout():
    """Payout settings — where the seller receives money from the platform."""
    profile = current_user.vendor_profile
    if profile is None:
        flash("Seller profile not found.", "danger")
        return redirect(url_for("seller.dashboard"))

    if request.method == "POST":
        bank_account_name = (request.form.get("bank_account_name") or "").strip()
        bank_account_number = (request.form.get("bank_account_number") or "").strip()
        bank_name = (request.form.get("bank_name") or "").strip()
        bkash_number = (request.form.get("bkash_number") or "").strip()
        nagad_number = (request.form.get("nagad_number") or "").strip()

        if not (bank_account_number or bkash_number or nagad_number):
            flash("Please provide at least one payout method (bank, bKash or Nagad).", "danger")
            return render_template("seller/payout.html", profile=profile, form=request.form)

        profile.bank_account_name = bank_account_name
        profile.bank_account_number = bank_account_number
        profile.bank_name = bank_name
        profile.bkash_number = bkash_number
        profile.nagad_number = nagad_number
        db.session.commit()
        flash("Payout settings saved successfully.", "success")
        return redirect(url_for("seller.dashboard"))

    return render_template("seller/payout.html", profile=profile, form={})


@seller.route("/shop/", methods=["GET", "POST"])
@login_required
@seller_required
def shop():
    """Edit the public store profile — name, description, logo, banner."""
    profile = current_user.vendor_profile
    if profile is None:
        flash("Seller profile not found.", "danger")
        return redirect(url_for("seller.dashboard"))

    if request.method == "POST":
        shop_name_en = (request.form.get("shop_name_en") or "").strip()
        if not shop_name_en:
            flash("Shop name (English) is required.", "danger")
            return render_template("seller/shop.html", profile=profile)

        profile.shop_name_en = shop_name_en
        profile.shop_name_bn = (request.form.get("shop_name_bn") or "").strip() or None
        profile.description_en = (request.form.get("description_en") or "").strip() or None
        profile.description_bn = (request.form.get("description_bn") or "").strip() or None

        logo = save_upload(request.files.get("logo"), "vendor_logos")
        if logo:
            profile.logo = logo
        banner = save_upload(request.files.get("banner"), "vendor_banners")
        if banner:
            profile.banner = banner

        db.session.commit()
        flash("Shop profile updated.", "success")
        return redirect(url_for("seller.shop"))

    return render_template("seller/shop.html", profile=profile)


# ==========================================================================
# product management  (requires an approved vendor)
# ==========================================================================
def _category_options():
    """Flat (id, label) list of active categories for a <select>."""
    options = []
    roots = (Category.query.filter_by(parent_id=None, is_active=True)
             .order_by(Category.sort_order, Category.name_en).all())
    for root in roots:
        options.append((root.id, root.name_en))
        children = sorted(root.children, key=lambda c: (c.sort_order, c.name_en))
        for child in children:
            if child.is_active:
                options.append((child.id, f"— {child.name_en}"))
    return options


def _unique_product_slug(title):
    base = slugify(title) or "product"
    slug, i = base, 2
    while Product.query.filter_by(slug=slug).first() is not None:
        slug = f"{base}-{i}"
        i += 1
    return slug


def _own_product_or_404(product_id):
    """Fetch a product, ensuring it belongs to the current seller."""
    product = db.session.get(Product, product_id)
    if product is None:
        abort(404)
    if product.vendor_id != current_user.vendor_profile.id:
        abort(403)
    return product


def _read_product_form():
    """Parse + validate the product core fields. Returns (data, errors)."""
    f = request.form
    title_en = (f.get("title_en") or "").strip()
    title_bn = (f.get("title_bn") or "").strip()
    category_id = (f.get("category_id") or "").strip()
    base_price = (f.get("base_price") or "0").strip()
    discount_price = (f.get("discount_price") or "").strip()
    stock = (f.get("stock") or "0").strip()

    errors = []
    if not title_en:
        errors.append("Product title (English) is required.")
    if not category_id.isdigit() or db.session.get(Category, int(category_id)) is None:
        errors.append("Please select a valid category.")

    try:
        base_price_v = float(base_price)
        if base_price_v < 0:
            raise ValueError
    except ValueError:
        base_price_v = None
        errors.append("Base price must be a valid non-negative number.")

    discount_v = None
    if discount_price:
        try:
            discount_v = float(discount_price)
            if discount_v < 0:
                raise ValueError
        except ValueError:
            errors.append("Discount price must be a valid number.")

    data = {
        "title_en": title_en,
        "title_bn": title_bn or None,
        "category_id": int(category_id) if category_id.isdigit() else None,
        "description_en": (f.get("description_en") or "").strip() or None,
        "description_bn": (f.get("description_bn") or "").strip() or None,
        "base_price": base_price_v if base_price_v is not None else 0,
        "discount_price": discount_v,
        "sku": (f.get("sku") or "").strip() or None,
        "stock": int(stock) if stock.lstrip("-").isdigit() else 0,
    }
    return data, errors


@seller.route("/products/")
@approved_vendor_required
def products():
    items = (Product.query.filter_by(vendor_id=current_user.vendor_profile.id)
             .order_by(Product.id.desc()).all())
    return render_template("seller/products.html", products=items)


@seller.route("/products/create", methods=["GET", "POST"])
@approved_vendor_required
def product_create():
    if request.method == "POST":
        data, errors = _read_product_form()
        if errors:
            for err in errors:
                flash(err, "danger")
            return render_template("seller/product_form.html",
                                   categories=_category_options(), form=request.form)

        product = Product(
            vendor_id=current_user.vendor_profile.id,
            slug=_unique_product_slug(data["title_en"]),
            status=PRODUCT_DRAFT,
            **data,
        )
        db.session.add(product)
        db.session.flush()

        order = 0
        for file in request.files.getlist("images"):
            path = save_upload(file, "products")
            if path:
                db.session.add(ProductImage(
                    product_id=product.id, image_path=path,
                    is_primary=(order == 0), sort_order=order,
                ))
                if order == 0:
                    product.thumbnail = path
                order += 1

        db.session.commit()
        flash("Product created as a draft. Add images & variants, then submit for review.",
              "success")
        return redirect(url_for("seller.product_edit", product_id=product.id))

    return render_template("seller/product_form.html",
                           categories=_category_options(), form={})


@seller.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@approved_vendor_required
def product_edit(product_id):
    product = _own_product_or_404(product_id)
    if request.method == "POST":
        data, errors = _read_product_form()
        if errors:
            for err in errors:
                flash(err, "danger")
        else:
            # Phase 15 D-6 — detect a 0 → positive stock transition so we
            # can fire back-in-stock notifications below.
            was_out_of_stock = (product.stock or 0) <= 0
            for key, value in data.items():
                setattr(product, key, value)
            db.session.commit()
            if was_out_of_stock and (product.stock or 0) > 0:
                from app.services.stock_service import notify_back_in_stock
                sent = notify_back_in_stock(product)
                if sent:
                    flash(f"Notified {sent} subscriber(s) that it's back in stock.",
                          "info")
            flash("Product updated.", "success")
        return redirect(url_for("seller.product_edit", product_id=product.id))
    return render_template("seller/product_edit.html",
                           product=product, categories=_category_options())


@seller.route("/products/<int:product_id>/delete", methods=["POST"])
@approved_vendor_required
def product_delete(product_id):
    product = _own_product_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("seller.products"))


@seller.route("/products/<int:product_id>/images", methods=["POST"])
@approved_vendor_required
def product_add_images(product_id):
    product = _own_product_or_404(product_id)
    start = len(product.images)
    added = 0
    for file in request.files.getlist("images"):
        path = save_upload(file, "products")
        if path:
            db.session.add(ProductImage(
                product_id=product.id, image_path=path,
                is_primary=(start + added == 0), sort_order=start + added,
            ))
            if start + added == 0:
                product.thumbnail = path
            added += 1
    db.session.commit()
    flash(f"{added} image(s) added." if added else "No valid images uploaded.",
          "success" if added else "danger")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/images/<int:image_id>/primary", methods=["POST"])
@approved_vendor_required
def product_image_primary(product_id, image_id):
    product = _own_product_or_404(product_id)
    for img in product.images:
        img.is_primary = (img.id == image_id)
        if img.is_primary:
            product.thumbnail = img.image_path
    db.session.commit()
    flash("Primary image updated.", "success")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/images/<int:image_id>/delete", methods=["POST"])
@approved_vendor_required
def product_image_delete(product_id, image_id):
    product = _own_product_or_404(product_id)
    image = db.session.get(ProductImage, image_id)
    if image and image.product_id == product.id:
        was_primary = image.is_primary
        db.session.delete(image)
        db.session.flush()
        remaining = [i for i in product.images if i.id != image_id]
        if was_primary and remaining:
            remaining[0].is_primary = True
            product.thumbnail = remaining[0].image_path
        elif not remaining:
            product.thumbnail = None
        db.session.commit()
        flash("Image removed.", "success")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/variants", methods=["POST"])
@approved_vendor_required
def product_add_variant(product_id):
    product = _own_product_or_404(product_id)
    size = (request.form.get("size") or "").strip()
    color = (request.form.get("color") or "").strip()
    price = (request.form.get("price") or "").strip()
    stock = (request.form.get("stock") or "0").strip()

    if not size and not color:
        flash("A variant needs at least a size or a colour.", "danger")
    else:
        try:
            price_v = float(price) if price else None
        except ValueError:
            price_v = None
        db.session.add(ProductVariant(
            product_id=product.id, size=size or None, color=color or None,
            price=price_v, stock=int(stock) if stock.isdigit() else 0,
        ))
        db.session.commit()
        flash("Variant added.", "success")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/variants/<int:variant_id>/delete", methods=["POST"])
@approved_vendor_required
def product_variant_delete(product_id, variant_id):
    product = _own_product_or_404(product_id)
    variant = db.session.get(ProductVariant, variant_id)
    if variant and variant.product_id == product.id:
        db.session.delete(variant)
        db.session.commit()
        flash("Variant removed.", "success")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/specs", methods=["POST"])
@approved_vendor_required
def product_add_spec(product_id):
    """Append a key-value specification row to the product (Phase 15 D-2)."""
    product = _own_product_or_404(product_id)
    label = (request.form.get("label") or "").strip()
    value = (request.form.get("value") or "").strip()
    if not label or not value:
        flash("A specification needs both a label and a value.", "danger")
    else:
        next_order = len(product.specs)
        db.session.add(ProductSpec(
            product_id=product.id, label=label[:120], value=value[:500],
            sort_order=next_order,
        ))
        db.session.commit()
        flash("Specification added.", "success")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/specs/<int:spec_id>/delete", methods=["POST"])
@approved_vendor_required
def product_delete_spec(product_id, spec_id):
    product = _own_product_or_404(product_id)
    spec = db.session.get(ProductSpec, spec_id)
    if spec and spec.product_id == product.id:
        db.session.delete(spec)
        db.session.commit()
        flash("Specification removed.", "success")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/tiers", methods=["POST"])
@approved_vendor_required
def product_add_tier(product_id):
    """Add a bulk-pricing tier row to the product (Phase 15 D-5 M4)."""
    product = _own_product_or_404(product_id)
    qty_raw = (request.form.get("min_quantity") or "").strip()
    pct_raw = (request.form.get("discount_pct") or "").strip()
    try:
        qty = int(qty_raw)
        pct = Decimal(pct_raw)
    except Exception:  # noqa: BLE001
        qty, pct = 0, Decimal("0")
    if qty < 2:
        flash("Bulk-tier quantity must be 2 or more.", "danger")
    elif pct <= 0 or pct >= 100:
        flash("Discount percent must be between 0 and 100.", "danger")
    elif any(t.min_quantity == qty for t in product.price_tiers):
        flash(f"A tier at quantity {qty} already exists.", "warning")
    else:
        db.session.add(ProductPriceTier(
            product_id=product.id, min_quantity=qty, discount_pct=pct,
        ))
        db.session.commit()
        flash(f"Bulk tier added: {qty}-pack at {pct}% off.", "success")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/tiers/<int:tier_id>/delete", methods=["POST"])
@approved_vendor_required
def product_delete_tier(product_id, tier_id):
    product = _own_product_or_404(product_id)
    tier = db.session.get(ProductPriceTier, tier_id)
    if tier and tier.product_id == product.id:
        db.session.delete(tier)
        db.session.commit()
        flash("Bulk tier removed.", "success")
    return redirect(url_for("seller.product_edit", product_id=product.id))


@seller.route("/products/<int:product_id>/submit", methods=["POST"])
@approved_vendor_required
def product_submit(product_id):
    product = _own_product_or_404(product_id)
    if not product.images:
        flash("Add at least one product image before submitting for review.", "danger")
    elif product.status in (PRODUCT_DRAFT, PRODUCT_REJECTED):
        product.status = PRODUCT_PENDING
        db.session.commit()
        flash("Product submitted for review. An admin will publish it shortly.", "success")
    else:
        flash("This product has already been submitted.", "info")
    return redirect(url_for("seller.product_edit", product_id=product.id))


# ==========================================================================
# order fulfilment  (the vendor's slice of customer orders)
# ==========================================================================
def _own_suborder_or_404(sub_order_id):
    sub = db.session.get(SubOrder, sub_order_id)
    if sub is None:
        abort(404)
    if sub.vendor_id != current_user.vendor_profile.id:
        abort(403)
    return sub


@seller.route("/orders/")
@approved_vendor_required
def orders():
    subs = (SubOrder.query.filter_by(vendor_id=current_user.vendor_profile.id)
            .order_by(SubOrder.id.desc()).all())
    return render_template("seller/orders.html", suborders=subs)


@seller.route("/orders/<int:sub_order_id>/")
@approved_vendor_required
def order_detail(sub_order_id):
    sub = _own_suborder_or_404(sub_order_id)
    return render_template("seller/order_detail.html", sub=sub, statuses=SUBORDER_STATUSES)


@seller.route("/orders/<int:sub_order_id>/status", methods=["POST"])
@approved_vendor_required
def order_status(sub_order_id):
    sub = _own_suborder_or_404(sub_order_id)
    new_status = request.form.get("status", "")
    if new_status in SUBORDER_STATUSES:
        # Centralised: records tracking event, settles wallet, notifies customer.
        update_suborder_status(sub, new_status)
        db.session.commit()
        flash(f"Order status updated to '{new_status}'.", "success")
    else:
        flash("Invalid status.", "danger")
    return redirect(url_for("seller.order_detail", sub_order_id=sub.id))


# ==========================================================================
# earnings & payout requests
# ==========================================================================
@seller.route("/earnings/", methods=["GET", "POST"])
@approved_vendor_required
def earnings():
    vp = current_user.vendor_profile
    wallet = get_or_create_wallet(vp.id)
    db.session.commit()

    if request.method == "POST":
        method = (request.form.get("method") or "").strip()
        try:
            amount = Decimal((request.form.get("amount") or "0").strip())
        except Exception:  # noqa: BLE001
            amount = Decimal("0")
        account_detail = {
            "bkash": vp.bkash_number or "",
            "nagad": vp.nagad_number or "",
            "bank": f"{vp.bank_name or ''} {vp.bank_account_number or ''}".strip(),
        }.get(method, "")

        if amount <= 0:
            flash("Enter a valid payout amount.", "danger")
        elif amount > Decimal(str(wallet.available_balance or 0)):
            flash("Amount exceeds your available balance.", "danger")
        elif method not in ("bkash", "nagad", "bank"):
            flash("Select a payout method.", "danger")
        elif not account_detail.strip():
            flash("Set up that payout method in Payout Settings first.", "danger")
        else:
            hold_for_payout(vp.id, amount)
            db.session.add(PayoutRequest(
                vendor_id=vp.id, amount=amount, method=method,
                account_detail=account_detail.strip(),
            ))
            db.session.commit()
            flash("Payout request submitted — an admin will review it.", "success")
        return redirect(url_for("seller.earnings"))

    subs = SubOrder.query.filter_by(vendor_id=vp.id).all()
    stats = {
        "orders": len(subs),
        "total_sales": sum((s.subtotal for s in subs), Decimal("0")),
        "total_commission": sum((s.commission_amount for s in subs), Decimal("0")),
    }
    payout_requests = (
        PayoutRequest.query.filter_by(vendor_id=vp.id)
        .order_by(PayoutRequest.id.desc()).all()
    )
    return render_template("seller/earnings.html", wallet=wallet, stats=stats,
                           payout_requests=payout_requests, profile=vp)


# ==========================================================================
# customer reviews on this seller's products
# ==========================================================================
@seller.route("/analytics/")
@approved_vendor_required
def analytics():
    """Sales metrics, top products & a simple forecast (Phase 11)."""
    days = max(7, min(365, request.args.get("days", 30, type=int) or 30))
    metrics = seller_metrics(current_user.vendor_profile, days=days)
    return render_template("seller/analytics.html",
                           metrics=metrics, days=days,
                           profile=current_user.vendor_profile)


@seller.route("/reviews/")
@approved_vendor_required
def reviews():
    vp = current_user.vendor_profile
    items = (
        Review.query.join(Product, Review.product_id == Product.id)
        .filter(Product.vendor_id == vp.id)
        .order_by(Review.id.desc()).all()
    )
    return render_template("seller/reviews.html", reviews=items, profile=vp)


# ==========================================================================
# store coupons (valid only on this seller's items)
# ==========================================================================
def _own_coupon_or_404(coupon_id):
    coupon = db.session.get(Coupon, coupon_id)
    if coupon is None or coupon.vendor_id != current_user.vendor_profile.id:
        abort(404)
    return coupon


@seller.route("/coupons/")
@approved_vendor_required
def coupons():
    items = (Coupon.query.filter_by(vendor_id=current_user.vendor_profile.id)
             .order_by(Coupon.id.desc()).all())
    return render_template("seller/coupons.html", coupons=items)


@seller.route("/coupons/new", methods=["GET", "POST"])
@approved_vendor_required
def coupon_create():
    if request.method == "POST":
        data, errors = parse_coupon_form(request.form)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("seller/coupon_form.html",
                                   form=request.form, coupon=None)
        db.session.add(Coupon(scope=COUPON_VENDOR,
                              vendor_id=current_user.vendor_profile.id, **data))
        db.session.commit()
        flash(f"Coupon '{data['code']}' created.", "success")
        return redirect(url_for("seller.coupons"))
    return render_template("seller/coupon_form.html", form={}, coupon=None)


@seller.route("/coupons/<int:coupon_id>/edit", methods=["GET", "POST"])
@approved_vendor_required
def coupon_edit(coupon_id):
    coupon = _own_coupon_or_404(coupon_id)
    if request.method == "POST":
        data, errors = parse_coupon_form(request.form, existing=coupon)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template("seller/coupon_form.html",
                                   form=request.form, coupon=coupon)
        for key, value in data.items():
            setattr(coupon, key, value)
        db.session.commit()
        flash("Coupon updated.", "success")
        return redirect(url_for("seller.coupons"))
    return render_template("seller/coupon_form.html",
                           form=coupon_form_dict(coupon), coupon=coupon)


@seller.route("/coupons/<int:coupon_id>/delete", methods=["POST"])
@approved_vendor_required
def coupon_delete(coupon_id):
    coupon = _own_coupon_or_404(coupon_id)
    db.session.delete(coupon)
    db.session.commit()
    flash("Coupon deleted.", "info")
    return redirect(url_for("seller.coupons"))


# --------------------------------------------------------------------------
# seller-led flash sales (Phase 15 Chunk C)
# --------------------------------------------------------------------------
def _own_flash_sale_or_404(sale_id):
    sale = db.session.get(FlashSale, sale_id)
    if sale is None or sale.vendor_id != current_user.vendor_profile.id:
        abort(404)
    return sale


def _unique_flash_slug(title):
    base = slugify(title) or "flash-sale"
    slug, i = base, 2
    while FlashSale.query.filter_by(slug=slug).first() is not None:
        slug = f"{base}-{i}"
        i += 1
    return slug


def _parse_dt(value):
    value = (value or "").strip()
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        return None


@seller.route("/flash-sales/")
@approved_vendor_required
def flash_sales():
    sales = (FlashSale.query
             .filter_by(vendor_id=current_user.vendor_profile.id)
             .order_by(FlashSale.id.desc()).all())
    return render_template("seller/flash_sales.html", sales=sales)


@seller.route("/flash-sales/new", methods=["POST"])
@approved_vendor_required
def flash_sale_create():
    title = (request.form.get("title") or "").strip()
    if not title:
        flash("A flash sale title is required.", "danger")
        return redirect(url_for("seller.flash_sales"))
    sale = FlashSale(
        title=title, slug=_unique_flash_slug(title),
        description=(request.form.get("description") or "").strip() or None,
        starts_at=_parse_dt(request.form.get("starts_at")),
        ends_at=_parse_dt(request.form.get("ends_at")),
        vendor_id=current_user.vendor_profile.id,
    )
    db.session.add(sale)
    db.session.commit()
    flash("Flash sale created — add your products to it.", "success")
    return redirect(url_for("seller.flash_sale_detail", sale_id=sale.id))


@seller.route("/flash-sales/<int:sale_id>/")
@approved_vendor_required
def flash_sale_detail(sale_id):
    sale = _own_flash_sale_or_404(sale_id)
    # Only the seller's own published products are listable.
    products = (Product.query
                .filter_by(vendor_id=current_user.vendor_profile.id,
                           status=PRODUCT_PUBLISHED)
                .order_by(Product.title_en).all())
    return render_template("seller/flash_sale_detail.html",
                           sale=sale, products=products)


@seller.route("/flash-sales/<int:sale_id>/items", methods=["POST"])
@approved_vendor_required
def flash_sale_add_item(sale_id):
    sale = _own_flash_sale_or_404(sale_id)
    product = db.session.get(Product, request.form.get("product_id", type=int))
    try:
        price = Decimal((request.form.get("flash_price") or "0").strip())
    except Exception:  # noqa: BLE001
        price = Decimal("0")

    if product is None or product.vendor_id != current_user.vendor_profile.id:
        flash("Please choose one of your own products.", "danger")
    elif price <= 0 or price >= product.base_price:
        flash("Flash price must be greater than 0 and lower than the regular price.",
              "danger")
    elif any(it.product_id == product.id for it in sale.items):
        flash("That product is already in this sale.", "warning")
    elif flash_sale_service.product_on_active_sale(product.id, exclude_sale_id=sale.id):
        flash("That product is already on another active flash sale.", "danger")
    else:
        flash_sale_service.add_item(sale, product, price)
        db.session.commit()
        flash("Product added to your flash sale.", "success")
    return redirect(url_for("seller.flash_sale_detail", sale_id=sale.id))


@seller.route("/flash-sales/items/<int:item_id>/delete", methods=["POST"])
@approved_vendor_required
def flash_sale_remove_item(item_id):
    item = db.session.get(FlashSaleItem, item_id) or abort(404)
    sale = item.flash_sale
    if sale is None or sale.vendor_id != current_user.vendor_profile.id:
        abort(404)
    sale_id = sale.id
    flash_sale_service.remove_item(item)
    db.session.commit()
    flash("Product removed from your flash sale.", "info")
    return redirect(url_for("seller.flash_sale_detail", sale_id=sale_id))


@seller.route("/flash-sales/<int:sale_id>/activate", methods=["POST"])
@approved_vendor_required
def flash_sale_activate(sale_id):
    sale = _own_flash_sale_or_404(sale_id)
    if not sale.items:
        flash("Add at least one product before launching the sale.", "warning")
    elif any(flash_sale_service.product_on_active_sale(
            it.product_id, exclude_sale_id=sale.id) for it in sale.items):
        flash("Some products are already on another active flash sale.", "danger")
    else:
        flash_sale_service.activate(sale)
        db.session.commit()
        flash("Your flash sale is live — discounted prices applied.", "success")
    return redirect(url_for("seller.flash_sale_detail", sale_id=sale.id))


@seller.route("/flash-sales/<int:sale_id>/deactivate", methods=["POST"])
@approved_vendor_required
def flash_sale_deactivate(sale_id):
    sale = _own_flash_sale_or_404(sale_id)
    flash_sale_service.deactivate(sale)
    db.session.commit()
    flash("Flash sale ended — original prices restored.", "info")
    return redirect(url_for("seller.flash_sale_detail", sale_id=sale.id))


@seller.route("/flash-sales/<int:sale_id>/delete", methods=["POST"])
@approved_vendor_required
def flash_sale_delete(sale_id):
    sale = _own_flash_sale_or_404(sale_id)
    if sale.is_active:
        flash_sale_service.deactivate(sale)
    db.session.delete(sale)
    db.session.commit()
    flash("Flash sale deleted.", "info")
    return redirect(url_for("seller.flash_sales"))


# --------------------------------------------------------------------------
# store promotion banner (Phase 15 Chunk C)
# --------------------------------------------------------------------------
@seller.route("/store-promo/", methods=["GET", "POST"])
@approved_vendor_required
def store_promo():
    """Edit the marketing banner shown atop the seller's public store page."""
    profile = current_user.vendor_profile
    if request.method == "POST":
        action = request.form.get("action", "")
        if action == "clear":
            profile.promo_banner_text = None
            profile.promo_banner_image = None
            profile.promo_until = None
            db.session.commit()
            flash("Store promotion cleared.", "info")
            return redirect(url_for("seller.store_promo"))

        text = (request.form.get("promo_banner_text") or "").strip() or None
        until = _parse_dt(request.form.get("promo_until"))
        uploaded = save_upload(request.files.get("promo_banner_image"),
                               "store_promos")
        if uploaded:
            profile.promo_banner_image = uploaded
        profile.promo_banner_text = text
        profile.promo_until = until
        if not (profile.promo_banner_text or profile.promo_banner_image):
            flash("Add at least a tagline or a banner image.", "danger")
        else:
            db.session.commit()
            flash("Store promotion saved.", "success")
        return redirect(url_for("seller.store_promo"))

    return render_template("seller/store_promo.html", profile=profile)
