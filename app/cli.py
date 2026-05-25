"""Custom Flask CLI commands.

Usage:
    flask --app run create-admin
"""
import os

import click

from app.extensions import db
from app.models.user import User, ROLE_ADMIN


def register_cli(app):
    """Attach custom commands to the Flask app."""

    @app.cli.command("create-admin")
    @click.option("--email", prompt="Admin email", help="Super-admin email address.")
    @click.option("--name", prompt="Admin name", default="Administrator",
                  help="Display name.")
    @click.option("--password", prompt="Admin password", hide_input=True,
                  confirmation_prompt=True, help="Super-admin password.")
    def create_admin(email, name, password):
        """Create (or promote) the super-admin account."""
        email = email.strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            user.role = ROLE_ADMIN
            user.name = name
            user.set_password(password)
            user.is_active = True
            user.is_email_verified = True
            click.echo(f"  Updated existing user '{email}' -> admin.")
        else:
            user = User(
                name=name, email=email, role=ROLE_ADMIN,
                is_active=True, is_email_verified=True,
            )
            user.set_password(password)
            db.session.add(user)
            click.echo(f"  Created admin '{email}'.")
        db.session.commit()
        click.echo("  Done. Admins log in with password only (no OTP).")

    @app.cli.command("seed-catalog")
    def seed_catalog():
        """Seed a starter category tree (safe to run repeatedly)."""
        from slugify import slugify
        from app.models.catalog import Category

        tree = {
            "Electronics": ["Mobiles", "Laptops", "Headphones", "Cameras", "Televisions"],
            "Fashion": ["Men's Wear", "Women's Wear", "Kids Wear", "Shoes", "Watches"],
            "Home & Living": ["Furniture", "Kitchen", "Home Decor"],
            "Grocery": ["Vegetables", "Fruits", "Beverages"],
            "Health & Beauty": ["Skincare", "Makeup", "Personal Care"],
        }
        created = 0
        for order, (parent_name, children) in enumerate(tree.items()):
            parent = Category.query.filter_by(slug=slugify(parent_name)).first()
            if parent is None:
                parent = Category(
                    name_en=parent_name, slug=slugify(parent_name), sort_order=order
                )
                db.session.add(parent)
                db.session.flush()
                created += 1
            for c_order, child_name in enumerate(children):
                child_slug = slugify(f"{parent_name}-{child_name}")
                if Category.query.filter_by(slug=child_slug).first() is None:
                    db.session.add(Category(
                        name_en=child_name, slug=child_slug,
                        parent_id=parent.id, sort_order=c_order,
                    ))
                    created += 1
        db.session.commit()
        click.echo(f"  Seeded catalog — {created} categories created.")

    @app.cli.command("seed-products")
    def seed_products():
        """Seed a demo store with sample published products (safe to re-run)."""
        from datetime import datetime
        from slugify import slugify
        from app.models.user import User, ROLE_SELLER
        from app.models.vendor import VendorProfile, VENDOR_APPROVED
        from app.models.catalog import Category, Product, ProductImage, PRODUCT_PUBLISHED

        email = "demo.seller@sgtcart.com"
        user = User.query.filter_by(email=email).first()
        if user is None:
            user = User(name="SGT Demo Store", email=email, role=ROLE_SELLER,
                        is_active=True, is_email_verified=True)
            user.set_password("demo1234")
            db.session.add(user)
            db.session.flush()
        vendor = VendorProfile.query.filter_by(user_id=user.id).first()
        if vendor is None:
            vendor = VendorProfile(
                user_id=user.id, shop_name_en="SGT Demo Store", slug="sgt-demo-store",
                status=VENDOR_APPROVED, verification_submitted_at=datetime.utcnow(),
            )
            db.session.add(vendor)
            db.session.flush()

        samples = [
            ("iPhone 13 Pro Max", "Mobiles", 139999, 129999, "assets/img/shop/9.png"),
            ("boAt Rockerz Headphones", "Headphones", 2499, 1899, "assets/img/shop/10.png"),
            ("Apple iPhone 11", "Mobiles", 58900, 54900, "assets/img/shop/11.png"),
            ("Canon EOS Digital Camera", "Cameras", 64999, None, "assets/img/shop/5.png"),
            ("JBL Wireless Headphones", "Headphones", 12239, 9999, "assets/img/shop/6.png"),
            ("Sony Smart LED TV", "Televisions", 81830, 74999, "assets/img/shop/7.png"),
            ("Men Casual Shirt", "Men's Wear", 1499, 999, "assets/img/product/2.jpg"),
            ("Women Summer Dress", "Women's Wear", 2199, 1799, "assets/img/product/4.jpg"),
            ("Tissot Tradition Watch", "Watches", 49849, None, "assets/img/shop/14.png"),
            ("Kids Cartoon T-shirt", "Kids Wear", 599, 449, "assets/img/product/10.jpg"),
        ]
        created = 0
        for title, cat_name, price, discount, image in samples:
            slug = slugify(title)
            if Product.query.filter_by(slug=slug).first():
                continue
            category = Category.query.filter_by(name_en=cat_name).first()
            if category is None:
                continue
            product = Product(
                vendor_id=vendor.id, category_id=category.id,
                title_en=title, slug=slug,
                description_en=f"{title} — a quality product from SGT Demo Store.",
                base_price=price, discount_price=discount, stock=50,
                sku=slug.upper()[:12], thumbnail=image, status=PRODUCT_PUBLISHED,
            )
            db.session.add(product)
            db.session.flush()
            db.session.add(ProductImage(
                product_id=product.id, image_path=image, is_primary=True, sort_order=0
            ))
            created += 1
        db.session.commit()
        click.echo(f"  Seeded {created} demo products into 'SGT Demo Store'.")

    @app.cli.command("seed-demo")
    def seed_demo():
        """Populate the site with 10 demo sellers, ~60 products across every
        category, a running flash sale, and three hero banners — so the
        homepage and dashboards look like a real store. Safe to re-run."""
        from datetime import datetime, timedelta
        from decimal import Decimal
        from random import choice, randint, sample, uniform
        from slugify import slugify
        from PIL import Image, ImageDraw, ImageFont

        from app.models.user import User, ROLE_SELLER
        from app.models.vendor import VendorProfile, VENDOR_APPROVED
        from app.models.catalog import (
            Category, Product, ProductImage, PRODUCT_PUBLISHED,
        )
        from app.models.marketing import FlashSale, FlashSaleItem
        from app.models.banner import HomepageBanner, BANNER_HERO, BANNER_STRIP

        # ----------------------------------------------------------------
        # 1. categories — make sure the standard tree exists
        # ----------------------------------------------------------------
        click.echo("• Ensuring category tree…")
        tree = {
            "Electronics": ["Mobiles", "Laptops", "Headphones",
                            "Cameras", "Televisions"],
            "Fashion":     ["Men's Wear", "Women's Wear", "Kids Wear",
                            "Shoes", "Watches"],
            "Home & Living": ["Furniture", "Kitchen", "Home Decor"],
            "Grocery":      ["Vegetables", "Fruits", "Beverages"],
            "Health & Beauty": ["Skincare", "Makeup", "Personal Care"],
        }
        cat_by_name = {}
        for o, (parent_name, children) in enumerate(tree.items()):
            parent = Category.query.filter_by(slug=slugify(parent_name)).first()
            if parent is None:
                parent = Category(name_en=parent_name,
                                  slug=slugify(parent_name), sort_order=o)
                db.session.add(parent)
                db.session.flush()
            cat_by_name[parent_name] = parent
            for co, c in enumerate(children):
                cs = slugify(f"{parent_name}-{c}")
                child = Category.query.filter_by(slug=cs).first()
                if child is None:
                    child = Category(name_en=c, slug=cs,
                                     parent_id=parent.id, sort_order=co)
                    db.session.add(child)
                    db.session.flush()
                cat_by_name[c] = child

        # ----------------------------------------------------------------
        # 2. demo sellers
        # ----------------------------------------------------------------
        demo_sellers = [
            ("Tech World",      "demo.techworld@sgt.bd",
             ["Mobiles", "Laptops", "Headphones"]),
            ("Camera Pro",      "demo.camerapro@sgt.bd",
             ["Cameras", "Televisions"]),
            ("Fashion Hub",     "demo.fashionhub@sgt.bd",
             ["Men's Wear", "Women's Wear"]),
            ("Shoe Palace",     "demo.shoepalace@sgt.bd",
             ["Shoes", "Watches"]),
            ("Kids Corner",     "demo.kidscorner@sgt.bd",
             ["Kids Wear"]),
            ("Home Essentials", "demo.homeess@sgt.bd",
             ["Furniture", "Home Decor"]),
            ("Kitchen King",    "demo.kitchenking@sgt.bd",
             ["Kitchen"]),
            ("Fresh Mart",      "demo.freshmart@sgt.bd",
             ["Vegetables", "Fruits"]),
            ("Daily Drinks",    "demo.dailydrinks@sgt.bd",
             ["Beverages"]),
            ("Glow Beauty",     "demo.glowbeauty@sgt.bd",
             ["Skincare", "Makeup", "Personal Care"]),
        ]
        click.echo("• Ensuring demo sellers…")
        # Generate a circular initials-on-colour logo per shop so the
        # Featured Stores grid shows real imagery rather than placeholder icons.
        logos_dir = os.path.join(app.root_path, "static", "shop_logos")
        os.makedirs(logos_dir, exist_ok=True)

        LOGO_PALETTE = [
            (29, 78, 216), (219, 39, 119), (22, 163, 74),
            (234, 88, 12), (147, 51, 234), (8, 145, 178),
            (202, 138, 4), (220, 38, 38), (15, 118, 110),
            (124, 58, 237),
        ]

        def _initials(name):
            parts = [p for p in name.split() if p]
            if len(parts) >= 2:
                return (parts[0][0] + parts[1][0]).upper()
            return name[:2].upper()

        def _draw_logo(path, name, colour, size=256):
            img = Image.new("RGB", (size, size), (255, 255, 255))
            draw = ImageDraw.Draw(img)
            # Solid colored circle.
            draw.ellipse([(0, 0), (size, size)], fill=colour)
            text = _initials(name)
            try:
                font = ImageFont.truetype("arialbd.ttf", int(size * 0.42))
            except Exception:
                font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((size - tw) / 2 - bbox[0],
                       (size - th) / 2 - bbox[1] - 4),
                      text, fill=(255, 255, 255), font=font)
            img.save(path, "PNG")

        vendor_by_name = {}
        for idx, (shop_name, email, _) in enumerate(demo_sellers):
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(name=shop_name, email=email, role=ROLE_SELLER,
                            is_active=True, is_email_verified=True)
                user.set_password("demo1234")
                db.session.add(user)
                db.session.flush()
            vendor = VendorProfile.query.filter_by(user_id=user.id).first()
            if vendor is None:
                vendor = VendorProfile(
                    user_id=user.id, shop_name_en=shop_name,
                    slug=slugify(shop_name), status=VENDOR_APPROVED,
                    verification_submitted_at=datetime.utcnow(),
                    rating_avg=Decimal(f"{uniform(3.6, 4.9):.2f}"),
                    rating_count=randint(20, 200),
                )
                db.session.add(vendor)
                db.session.flush()
            # Always make sure the logo file exists for this shop and the
            # vendor record points to it (safe to re-run).
            logo_file = f"{vendor.slug}.png"
            logo_path = os.path.join(logos_dir, logo_file)
            if not os.path.exists(logo_path):
                _draw_logo(logo_path, shop_name,
                           LOGO_PALETTE[idx % len(LOGO_PALETTE)])
            vendor.logo = f"shop_logos/{logo_file}"
            vendor_by_name[shop_name] = vendor
        db.session.commit()

        # ----------------------------------------------------------------
        # 3. products — realistic BD names & prices, cycled images
        # ----------------------------------------------------------------
        catalog = {
            "Mobiles": [
                ("Samsung Galaxy A55 5G",                   45000, 39999),
                ("Xiaomi Redmi Note 13 Pro",                29500, 26000),
                ("iPhone 13 (Refurbished)",                 75000, None),
                ("Realme C67 4G",                           18999, 16500),
            ],
            "Laptops": [
                ("Asus VivoBook 15 (i5, 12th Gen)",         78000, 72000),
                ("HP Pavilion x360 Convertible",           110000, 99000),
                ("Lenovo IdeaPad Slim 3",                   62000, None),
            ],
            "Headphones": [
                ("Boult Audio Wireless Earbuds",             1850, 1499),
                ("JBL Tune 510BT",                           5200, 3999),
                ("Sennheiser HD 300 Wired",                  7900, None),
            ],
            "Cameras": [
                ("Canon EOS 1500D DSLR Kit",                48000, 42500),
                ("Sony ZV-1F Vlog Camera",                  75000, None),
                ("GoPro HERO12 Black",                      55000, 49999),
            ],
            "Televisions": [
                ("Walton 43-inch FHD Smart TV",             32000, 28500),
                ('Sony BRAVIA 50" 4K Google TV',           115000, None),
                ('Singer 32" HD LED TV',                    22500, 19999),
            ],
            "Men's Wear": [
                ("Premium Cotton Panjabi (Eid Collection)",  1900, 1399),
                ("Solid Casual Shirt (Slim Fit)",            1200, None),
                ("Formal Two-Piece Suit",                    8500, 6999),
                ("Polo T-Shirt (Pack of 2)",                 1450, 1099),
            ],
            "Women's Wear": [
                ("Three-Piece Unstitched Lawn Set",          2800, 1999),
                ("Cotton Saree with Blouse Piece",           2400, 1850),
                ("Embroidered Kameez (Eid Special)",         3500, 2799),
            ],
            "Kids Wear": [
                ("Cartoon Print Cotton T-Shirt",              450, 349),
                ("Boys' Denim Jeans (5-8 Yrs)",               990, None),
                ("Girls' Frock with Bow",                    1250, 899),
            ],
            "Shoes": [
                ("Bata Formal Leather Shoes",                2500, 1999),
                ("Apex Sneakers (Men's)",                    2199, None),
                ("Walkmate Sandals",                          950, 749),
            ],
            "Watches": [
                ("Casio MTP-1314 Analog",                    3850, 3299),
                ("Titan Karishma (Women's)",                 4500, None),
                ("Q&Q Sports Digital",                        980, 749),
            ],
            "Furniture": [
                ("Wooden Computer Table",                    5800, 4899),
                ("3-Seater Fabric Sofa",                    22000, 18500),
                ("Single Bed (Otobi style)",                 9500, None),
            ],
            "Home Decor": [
                ("LED String Lights (10m)",                   390, 249),
                ("Wall Clock — Modern Minimalist",            780, None),
                ("Decorative Wall Art Set",                  1450, 1099),
            ],
            "Kitchen": [
                ("Non-stick Frying Pan (24cm)",               890, 699),
                ("Pressure Cooker 5L",                       1850, None),
                ("Stainless Steel Knife Set",                 950, 749),
            ],
            "Vegetables": [
                ("Fresh Carrots (1 kg)",                       80, None),
                ("Cabbage (per piece)",                         65, 49),
                ("Mixed Vegetables Pack (3 kg)",              280, 229),
            ],
            "Fruits": [
                ("Bangladeshi Mango (Himsagar, 1 kg)",        180, 149),
                ("Imported Red Apple (1 kg)",                 360, None),
                ("Bananas (1 dozen)",                           90, 75),
            ],
            "Beverages": [
                ("Tang Orange Drink Mix (750 g)",             395, None),
                ("Rooh Afza Concentrate (750 ml)",            390, 349),
                ("Coffee Mate Beans 250g",                    650, 549),
            ],
            "Skincare": [
                ("Pond's Bright Beauty Cream 50g",            285, 219),
                ("Garnier Men Acno Fight Face Wash",          280, None),
                ("Vaseline Healthy Bright Lotion 400ml",      480, 399),
            ],
            "Makeup": [
                ("Maybelline Fit Me Foundation",             1100, 899),
                ("Lakme Eyeconic Kajal",                      450, None),
                ("L'Oreal Paris Color Riche Lipstick",        890, 749),
            ],
            "Personal Care": [
                ("Dove Beauty Bar Soap (4-pack)",             380, 299),
                ("Colgate Total Toothpaste 200g",             190, None),
                ("Gillette Mach 3 Razor",                     490, 399),
            ],
        }

        # Theme images we cycle through so every demo product has a picture.
        theme_images = [
            "assets/img/shop/9.png", "assets/img/shop/5.png",
            "assets/img/shop/6.png", "assets/img/shop/7.png",
            "assets/img/shop/10.png", "assets/img/shop/11.png",
            "assets/img/shop/14.png", "assets/img/product/2.jpg",
            "assets/img/product/4.jpg", "assets/img/product/10.jpg",
        ]

        # Map each category to the seller that owns it.
        owner_of_category = {}
        for shop_name, _, cats in demo_sellers:
            for c in cats:
                owner_of_category[c] = vendor_by_name[shop_name]

        click.echo("• Seeding products…")
        new_products = []
        image_index = 0
        for cat_name, items in catalog.items():
            cat = cat_by_name.get(cat_name)
            vendor = owner_of_category.get(cat_name)
            if cat is None or vendor is None:
                continue
            for title, base_price, discount_price in items:
                slug = slugify(f"{vendor.slug}-{title}")[:200]
                if Product.query.filter_by(slug=slug).first() is not None:
                    continue
                img = theme_images[image_index % len(theme_images)]
                image_index += 1
                product = Product(
                    vendor_id=vendor.id, category_id=cat.id,
                    title_en=title, slug=slug,
                    description_en=(
                        f"{title} — sold by {vendor.shop_name_en}. Genuine "
                        "product, fast delivery across Bangladesh, easy returns "
                        "within 7 days. Cash on Delivery available."
                    ),
                    base_price=Decimal(str(base_price)),
                    discount_price=Decimal(str(discount_price)) if discount_price else None,
                    sku=slug.upper().replace("-", "")[:14],
                    stock=randint(8, 60), thumbnail=img,
                    status=PRODUCT_PUBLISHED,
                    rating_avg=Decimal(f"{uniform(3.5, 5.0):.2f}"),
                    rating_count=randint(0, 40),
                    is_featured=(randint(1, 6) == 1),
                )
                db.session.add(product)
                db.session.flush()
                db.session.add(ProductImage(
                    product_id=product.id, image_path=img,
                    is_primary=True, sort_order=0,
                ))
                new_products.append(product)
        db.session.commit()
        click.echo(f"  Added {len(new_products)} products.")

        # ----------------------------------------------------------------
        # 4. one demo flash sale across several sellers
        # ----------------------------------------------------------------
        flash_title = "SGT Mega Eid Sale"
        sale = FlashSale.query.filter_by(slug=slugify(flash_title)).first()
        if sale is None:
            sale = FlashSale(
                title=flash_title, slug=slugify(flash_title),
                description="Hand-picked deals from your favourite stores — "
                            "limited time only.",
                starts_at=datetime.utcnow() - timedelta(days=1),
                ends_at=datetime.utcnow() + timedelta(days=14),
                is_active=False,
            )
            db.session.add(sale)
            db.session.flush()

        if not sale.items:
            # pick 8 products from a mix of categories that have a discount_price
            published = (Product.query.filter_by(status=PRODUCT_PUBLISHED)
                         .filter(Product.discount_price.isnot(None)).all())
            chosen = sample(published, min(8, len(published))) if published else []
            for p in chosen:
                flash_price = (p.discount_price * Decimal("0.85")).quantize(Decimal("0.01"))
                item = FlashSaleItem(flash_sale_id=sale.id, product_id=p.id,
                                     flash_price=flash_price)
                item.product = p
                item.original_discount_price = p.discount_price
                p.discount_price = flash_price
                db.session.add(item)
            sale.is_active = True
            db.session.commit()
            click.echo(f"  Activated flash sale with {len(chosen)} items.")
        else:
            click.echo("  Flash sale already exists — left unchanged.")

        # ----------------------------------------------------------------
        # 5. three demo banners (hero + strip)
        # ----------------------------------------------------------------
        banners_dir = os.path.join(app.root_path, "static", "banners")
        os.makedirs(banners_dir, exist_ok=True)

        def _draw_banner(path, headline, sub, gradient, size=(1200, 420)):
            img = Image.new("RGB", size, gradient[0])
            draw = ImageDraw.Draw(img)
            # vertical gradient
            for y in range(size[1]):
                r = int(gradient[0][0] + (gradient[1][0] - gradient[0][0]) * y / size[1])
                g = int(gradient[0][1] + (gradient[1][1] - gradient[0][1]) * y / size[1])
                b = int(gradient[0][2] + (gradient[1][2] - gradient[0][2]) * y / size[1])
                draw.line([(0, y), (size[0], y)], fill=(r, g, b))
            try:
                big = ImageFont.truetype("arialbd.ttf", 64)
                med = ImageFont.truetype("arial.ttf", 28)
            except Exception:
                big = med = ImageFont.load_default()
            draw.text((60, size[1] // 2 - 60), headline, fill=(255, 255, 255), font=big)
            draw.text((60, size[1] // 2 + 20), sub, fill=(245, 245, 245), font=med)
            img.save(path)

        demo_banners = [
            ("hero", 10, "demo-hero-1.png",
             "Mega Eid Sale", "Up to 60% off across every category",
             ((220, 38, 38), (15, 23, 42)), (1200, 420),
             "Shop the sale", "/flash-sales/"),
            ("hero", 20, "demo-hero-2.png",
             "Become a Seller", "Open your shop in 1-2 days. Sell to all of Bangladesh.",
             ((15, 23, 42), (37, 99, 235)), (1200, 420),
             "Start selling", "/sell/"),
            ("hero", 30, "demo-hero-3.png",
             "Free Cash on Delivery", "On orders above ৳999 — every district covered.",
             ((22, 163, 74), (15, 118, 110)), (1200, 420),
             "Shop now", "/shop/"),
            ("strip", 10, "demo-strip-1.png",
             "Daily Essentials at 50% Off",
             "Groceries, beauty, kitchen — refilled every morning.",
             ((22, 163, 74), (217, 119, 6)), (1200, 180),
             "Browse deals", "/shop/?category=grocery"),
        ]
        new_banners = 0
        for kind, sort_order, fname, headline, sub, grad, size, btn_t, btn_u in demo_banners:
            existing = HomepageBanner.query.filter_by(image_path=f"banners/{fname}").first()
            if existing is not None:
                continue
            _draw_banner(os.path.join(banners_dir, fname),
                         headline, sub, grad, size)
            db.session.add(HomepageBanner(
                kind=kind, image_path=f"banners/{fname}",
                headline=headline, subheadline=sub,
                button_text=btn_t, button_url=btn_u,
                sort_order=sort_order, is_active=True,
            ))
            new_banners += 1
        db.session.commit()
        click.echo(f"  Added {new_banners} homepage banners.")

        click.echo("Done — visit / to see the demo store.")

    @app.cli.command("recompute-vendor-stats")
    def recompute_vendor_stats_cmd():
        """Refresh every vendor's avg_delivery_days + cancel_rate from order
        history. Safe to run nightly via cron."""
        from app.services.vendor_stats_service import recompute_all
        n = recompute_all()
        click.echo(f"  Recomputed stats for {n} vendor(s).")

    @app.cli.command("process-payouts")
    @click.option("--min-hours", default=None, type=int,
                  help="Grace period before a pending payout is auto-approved.")
    def process_payouts(min_hours):
        """Auto-approve payout requests that have been pending long enough."""
        from app.services.payout_service import process_due_payouts
        approved = process_due_payouts(min_hours=min_hours)
        click.echo(f"  Auto-payouts: {approved} approved.")

    @app.cli.command("embed-products")
    def embed_products():
        """Generate CLIP image embeddings for every published product.

        First run downloads the model (~600 MB) and may take a few minutes.
        """
        from app.services import image_search_service

        if not image_search_service.is_available():
            click.echo("  CLIP model is not available — install sentence-transformers.")
            return
        done, skipped = image_search_service.embed_all_published(verbose=True)
        db.session.commit()
        click.echo(f"  Embeddings refreshed — {done} done, {skipped} skipped.")

    @app.cli.command("scan-abandoned-carts")
    @click.option("--hours", default=None, type=int,
                  help="Idle hours before a cart counts as abandoned.")
    def scan_abandoned_carts(hours):
        """Detect abandoned carts and email recovery reminders.

        Intended for a scheduler (cron / Celery beat) — safe to run often.
        """
        from app.services import abandoned_cart_service

        idle = hours or abandoned_cart_service.IDLE_HOURS
        detected, sent = abandoned_cart_service.scan(idle_hours=idle)
        click.echo(f"  Abandoned-cart scan: {detected} found, "
                   f"{sent} reminder email(s) sent.")

    @app.cli.command("refresh-ai-summaries")
    def refresh_ai_summaries():
        """Recompute the cached AI pros/cons summary for every published
        product (Phase 15 D-8). Run nightly via cron."""
        from app.services import ai_summary_service
        n = ai_summary_service.refresh_all_published()
        click.echo(f"  Refreshed AI summaries for {n} published product(s).")

    @app.cli.command("optimize-banners")
    @click.option("--max-width", default=1600, type=int,
                  help="Cap the banner width in pixels.")
    @click.option("--quality", default=85, type=int,
                  help="JPEG quality (1-95).")
    def optimize_banners(max_width, quality):
        """Re-compress every HomepageBanner image in-place.

        Use after introducing the upload-time resizer so that already
        uploaded multi-megabyte PNG banners get shrunk to the same
        bandwidth budget as new uploads. Updates the DB row to point at
        the new file when the format changes (PNG -> JPG)."""
        from PIL import Image, ImageOps
        from app.models.banner import HomepageBanner

        uploads_root = app.config["UPLOAD_FOLDER"]
        static_root = os.path.join(app.root_path, "static")

        banners = HomepageBanner.query.all()
        shrunk = unchanged = missing = errors = 0
        for b in banners:
            if not b.image_path:
                continue
            src_path = os.path.join(static_root, b.image_path)
            if not os.path.exists(src_path):
                missing += 1
                continue
            old_size = os.path.getsize(src_path)
            try:
                img = Image.open(src_path)
                img = ImageOps.exif_transpose(img)
                # Banners are full-bleed hero images — transparency is
                # meaningless on the homepage, so flatten alpha onto a
                # white background and always save as JPEG. That brings
                # 6-7 MB RGBA PNGs down to ~150-300 KB.
                use_jpeg = True
                if img.mode != "RGB":
                    if img.mode in ("RGBA", "LA"):
                        bg = Image.new("RGB", img.size, (255, 255, 255))
                        bg.paste(img, mask=img.split()[-1])
                        img = bg
                    else:
                        img = img.convert("RGB")
                w, h = img.size
                if w > max_width:
                    h = int(h * (max_width / w))
                    w = max_width
                    img = img.resize((w, h), Image.LANCZOS)

                # Always keep files inside uploads/banners/ regardless of
                # where they currently live; that's where new admin
                # uploads go via save_image_upload.
                import uuid as _uuid
                out_dir = os.path.join(uploads_root, "banners")
                os.makedirs(out_dir, exist_ok=True)
                out_ext = "jpg" if use_jpeg else "png"
                fname = f"{_uuid.uuid4().hex}.{out_ext}"
                out_path = os.path.join(out_dir, fname)
                save_kwargs = ({"format": "JPEG", "quality": quality,
                                "optimize": True, "progressive": True}
                               if use_jpeg
                               else {"format": "PNG", "optimize": True})
                img.save(out_path, **save_kwargs)
                new_size = os.path.getsize(out_path)

                if new_size >= old_size:
                    os.remove(out_path)
                    unchanged += 1
                    continue

                b.image_path = f"uploads/banners/{fname}"
                shrunk += 1
                click.echo(
                    f"  {b.kind:5}  {old_size // 1024:>5} KB -> "
                    f"{new_size // 1024:>5} KB  ({b.headline or '(no headline)'})"
                )
            except Exception as exc:  # noqa: BLE001 — keep going
                errors += 1
                click.echo(f"  ! {src_path} — {exc}")
        db.session.commit()
        click.echo(
            f"Banners — {shrunk} shrunk, {unchanged} already small enough, "
            f"{missing} missing, {errors} errors."
        )

    @app.cli.command("seed-static-pages")
    @click.option("--overwrite", is_flag=True,
                  help="Replace content for slugs that already exist.")
    def seed_static_pages(overwrite):
        """Seed the 16 footer pages that were 404'ing.

        Each row is admin-editable from /admin/static-pages/. Safe to
        re-run — existing rows are kept unless --overwrite is passed.
        """
        import json as _json
        from datetime import datetime as _dt
        from app.models.static_page import StaticPage
        from app.static_page_content import FOOTER_PAGES

        added = updated = skipped = 0
        for entry in FOOTER_PAGES:
            slug = entry["slug"]
            row = StaticPage.query.filter_by(slug=slug).first()
            if row is not None and not overwrite:
                skipped += 1
                continue
            if row is None:
                row = StaticPage(slug=slug)
                db.session.add(row)
                added += 1
            else:
                updated += 1
            row.title = entry["title"]
            row.subtitle = entry.get("subtitle")
            row.section = entry.get("section", "Misc")
            row.contact_email = entry.get(
                "contact_email", "support@sgtcart.com")
            row.body_html = entry["body_html"]
            row.toc_json = _json.dumps(entry.get("toc", []), ensure_ascii=False)
            row.faq_json = _json.dumps(entry.get("faq", []), ensure_ascii=False)
            row.related_json = _json.dumps(
                entry.get("related", []), ensure_ascii=False)
            row.version = entry.get("version", "v1.0")
            row.reviewed_at = _dt.utcnow()
            row.is_published = True
            row.sort_order = entry.get("sort_order", 0)
        db.session.commit()
        click.echo(
            f"  Static pages — {added} added, {updated} updated, "
            f"{skipped} skipped (already existed).")

    @app.cli.command("seed-district-eta")
    def seed_district_eta():
        """Seed the district delivery-ETA table (Phase 15 D-9)."""
        from app.models.district import DistrictEta
        from app.services.delivery_eta_service import SEED_DISTRICTS
        added = updated = 0
        for name, min_d, max_d in SEED_DISTRICTS:
            row = DistrictEta.query.filter(
                DistrictEta.district.ilike(name)
            ).first()
            if row is None:
                db.session.add(DistrictEta(
                    district=name, min_days=min_d, max_days=max_d,
                ))
                added += 1
            else:
                row.min_days = min_d
                row.max_days = max_d
                updated += 1
        db.session.commit()
        click.echo(f"  Seeded district ETAs — {added} added, {updated} updated.")
