from flask import Blueprint, session, render_template, jsonify, request, redirect, url_for, flash
from flask_login import current_user
from slugify import slugify
from flask import render_template, session
from app import csrf
import uuid

main = Blueprint("main", __name__)

@main.context_processor
def inject_slugify():
    return {'slugify': slugify}

@main.context_processor
def inject_cart_wishlist():
    return {
        'cart': session.get('cart', []),
        'wishlist': session.get('wishlist', [])
    }


@main.route("/")
def index():
    """Marketplace homepage — real DB-driven content (Phase 15 Chunk B)."""
    from sqlalchemy import func
    from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
    from app.models.vendor import VendorProfile, VENDOR_APPROVED
    from app.models.banner import HomepageBanner, BANNER_HERO, BANNER_STRIP
    from app.services.search_service import apply_ranking
    from app.services.recommendation_service import best_sellers, for_you
    from app.services.flash_sale_service import live_sales

    # Admin-managed slides + promo strip.
    hero_banners = (HomepageBanner.query
                    .filter_by(kind=BANNER_HERO, is_active=True)
                    .order_by(HomepageBanner.sort_order, HomepageBanner.id).all())
    strip_banners = (HomepageBanner.query
                     .filter_by(kind=BANNER_STRIP, is_active=True)
                     .order_by(HomepageBanner.sort_order, HomepageBanner.id).all())

    # Active categories for the Daraz-style homepage grid — roots first,
    # then immediate sub-categories to fill out a tidy 8-per-row layout.
    roots = (Category.query.filter_by(parent_id=None, is_active=True)
             .order_by(Category.sort_order, Category.name_en).all())
    subs = (Category.query.filter(Category.parent_id.isnot(None),
                                   Category.is_active.is_(True))
            .order_by(Category.sort_order, Category.name_en).all())
    homepage_categories = (roots + subs)[:16]

    flash_sales = live_sales()[:1]
    bests = best_sellers(limit=12)
    new_arrivals = (
        Product.query.filter_by(status=PRODUCT_PUBLISHED)
        .order_by(Product.created_at.desc()).limit(12).all()
    )
    top_rated = (
        apply_ranking(Product.query.filter_by(status=PRODUCT_PUBLISHED))
        .limit(12).all()
    )
    # "For you" — personalised when signed in, random varied mix for guests.
    if current_user.is_authenticated:
        for_you_products = for_you(current_user, limit=12)
    else:
        for_you_products = (
            Product.query.filter_by(status=PRODUCT_PUBLISHED)
            .order_by(func.random()).limit(12).all()
        )

    featured_stores = (
        VendorProfile.query.filter_by(status=VENDOR_APPROVED)
        .order_by(VendorProfile.rating_avg.desc(),
                  VendorProfile.rating_count.desc()).limit(8).all()
    )
    return render_template(
        "pages/index.html",
        hero_banners=hero_banners, strip_banners=strip_banners,
        homepage_categories=homepage_categories,
        flash_sales=flash_sales, bests=bests, new_arrivals=new_arrivals,
        top_rated=top_rated, for_you_products=for_you_products,
        featured_stores=featured_stores,
    )


@main.route("/home-2/")
def home_2():
    return render_template("pages/home-2.html")


@main.route("/home-3/")
def home_3():
    return render_template("pages/home-3.html")


@main.route("/home-4/")
def home_4():
    return render_template("pages/home-4.html")


@main.route("/home-5/")
def home_5():
    return render_template("pages/home-5.html")


@main.route("/home-6/")
def home_6():
    return render_template("pages/home-6.html")


@main.route("/home-7/")
def home_7():
    return render_template("pages/home-7.html")


@main.route("/home-8/")
def home_8():
    return render_template("pages/home-8.html")


@main.route("/home-9/")
def home_9():
    return render_template("pages/home-9.html")


@main.route("/home-10/")
def home_10():
    return render_template("pages/home-10.html")


@main.route("/home-11/")
def home_11():
    return render_template("pages/home-11.html")


@main.route("/home-12/")
def home_12():
    return render_template("pages/home-12.html")


@main.route("/home-13/")
def home_13():
    return render_template("pages/home-13.html")


@main.route("/home-14/")
def home_14():
    return render_template("pages/home-14.html")


@main.route("/home-15/")
def home_15():
    return render_template("pages/home-15.html")


@main.route("/home-16/")
def home_16():
    return render_template("pages/home-16.html")


@main.route("/home-17/")
def home_17():
    return render_template("pages/home-17.html")


# /my-orders/ is served by the `account` blueprint (app/blueprints/account.py)


@main.route('/wishlist/')
def wishlist():
    wishlist = session.get('wishlist', [])
    subtotal = sum(item['price'] * item['quantity'] for item in wishlist)

    return render_template('pages/wishlist.html', wishlist=wishlist, subtotal=subtotal)


# /profile-info/ is now served by the `account` blueprint (app/blueprints/account.py)


# /addresses/ and the address forms are served by the `account` blueprint
# (app/blueprints/account.py) — DB-backed.


@main.route("/add-card/")
def add_card():
    return render_template("pages/add-card.html")


@main.route("/shop-style-1/")
def shop_style_1():
    return render_template("pages/shop-style-1.html")


@main.route("/shop-style-2/")
def shop_style_2():
    return render_template("pages/shop-style-2.html")


@main.route("/shop-style-3/")
def shop_style_3():
    return render_template("pages/shop-style-3.html")


@main.route("/shop-style-4/")
def shop_style_4():
    return render_template("pages/shop-style-4.html")


@main.route("/shop-style-5/")
def shop_style_5():
    return render_template("pages/shop-style-5.html")


@main.route("/shop-list-view/")
def shop_list_view():
    return render_template("pages/shop-list-view.html")


@main.route("/shop-single-v1/")
def shop_list_or_default():
    products = [
        {
            'id' : 1,
            'img' : '/static/assets/img/product/16.png', 
            'title' : 'Women Striped Shirt Dress',
            'price' : 110,
        }
    ]
    product = products[0]
    return render_template("pages/shop-single-v1.html", product=product)


@main.route("/shop-single-v1/<string:title>/")
def shop_single_v1(title):
    products = [
        {
            'id' : 1,
            'img' : '/static/assets/img/product/1.jpg', 
            'title' : 'Half Running Set',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 119,
            'original_price' : None,
            'class' : 'fw-medium fs-md text-dark',
        },
        {
            'id' : 2,
            'img' : '/static/assets/img/product/2.jpg', 
            'title' : 'Formal Men Lowers',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'price' : 79,
            'original_price' : 129,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 3,
            'img' : '/static/assets/img/product/3.jpg', 
            'title' : 'Half Running Suit',
            'tag' : False,
            'style' : '',
            'price' : 80,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 4,
            'img' : '/static/assets/img/product/4.jpg', 
            'title' : 'Half Fancy Lady Dress',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 110,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 5,
            'img' : '/static/assets/img/product/5.jpg', 
            'title' : 'Flix Flox Jeans',
            'tag' : False,
            'style' : '',
            'price' : 49,
            'original_price' : 90,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 6,
            'img' : '/static/assets/img/product/6.jpg', 
            'title' : 'Fancy Salwar Suits',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 114,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 7,
            'img' : '/static/assets/img/product/7.jpg', 
            'title' : 'Collot Full Dress',
            'tag' : 'Sale',
            'style' : 'bg-new',
            'price' : 120,
            'original_price' : None,
            'class' : 'ft-medium theme-cl fs-md text-dark',
        },
        {
            'id' : 8,
            'img' : '/static/assets/img/product/8.jpg', 
            'title' : 'Formal Fluex Kurti',
            'tag' : False,
            'style' : '',
            'price' : 129,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 9,
            'img' : '/static/assets/img/product/2.jpg', 
            'title' : 'Women Striped Shirt Dress',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '5 Reviews',
            'star' : 'filled',
            'style' : 'bg-sale',
            'price' : 129,
        },
        {
            'id' : 10,
            'img' : '/static/assets/img/product/3.jpg', 
            'title' : 'Boys Solid Sweatshirt',
            'tag' : 'Sold Out',
            'tag1' : '-40%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sold',
            'price' : 129,
        },
        {
            'id' : 11,
            'img' : '/static/assets/img/product/1.jpg', 
            'title' : 'Girls Floral Print Jumpsuit',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '32 Reviews',
            'star' : 'filled',
            'style' : 'bg-sale',
            'price' : 99,
        },
        {
            'id' : 12,
            'img' : '/static/assets/img/product/6.jpg', 
            'title' : 'Girls Solid A-Line Dress',
            'tag' : 'New',
            'tag1' : '-55%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-new',
            'price' : 149,
        },
        {
            'id' : 13,
            'img' : '/static/assets/img/product/7.jpg', 
            'title' : 'Printed Straight Kurta',
            'tag' : 'New',
            'tag1' : '-30%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-new',
            'price' : 199,
        },
        {
            'id' : 14,
            'img' : '/static/assets/img/product/3.jpg', 
            'title' : 'Women Printed A-Line Dress',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '42 Reviews',
            'star' : 'filled',
            'style' : 'bg-sale',
            'price' : 110,
        },
        {
            'id' : 15,
            'img' : '/static/assets/img/product/9.jpg', 
            'title' : 'Girls Fit and Flare Dress',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sale',
            'price' : 99,
        },
        {
            'id' : 16,
            'img' : '/static/assets/img/product/6.jpg', 
            'title' : 'Girls Self Design Jumpsuit',
            'tag' : 'New',
            'tag1' : '-60%',
            'reviews' : '15 Reviews',
            'star' : 'filled',
            'style' : 'bg-new',
            'price' : 119,
        },
        {
            'id' : 17,
            'img' : '/static/assets/img/product/10.jpg', 
            'title' : 'Boys White T-shirt',
            'tag' : 'New',
            'tag1' : '-55%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-new',
            'price' : 149,
        },
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg', 
            'title' : 'Boys yellow-green T-shirt',
            'tag' : 'Sale',
            'tag1' : '-30%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sale',
            'price' : 199,
        },
        {
            'id' : 19,
            'img' : '/static/assets/img/product/12.jpg', 
            'title' : 'Women White T-shirt',
            'tag' : 'Sold Out',
            'tag1' : None,
            'reviews' : '42 Reviews',
            'star' : 'filled',
            'style' : 'bg-sold',
            'price' : 600,
        },
        {
            'id' : 20,
            'img' : '/static/assets/img/product/13.jpg', 
            'title' : 'Boys Shorts',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sale',
            'price' : 110,
        },
        {
            'id' : 21,
            'img' : '/static/assets/img/product/14.jpg', 
            'title' : 'Boys yellow T-shirt',
            'tag' : 'New',
            'tag1' : '-60%',
            'reviews' : '15 Reviews',
            'star' : 'filled',
            'style' : 'bg-new',
            'price' : 119,
        },
        {
            'id' : 22,
            'img' : '/static/assets/img/product/15.png', 
            'title' : 'Women Straight Pants',
            'tag' : 'Hot',
            'tag1' : None,
            'reviews' : '5 Reviews',
            'star' : 'filled',
            'style' : 'bg-hot',
            'price' : '99 - $129',
        },
        {
            'id' : 23,
            'img' : '/static/assets/img/product/16.png', 
            'title' : 'Yellow One-piece',
            'tag' : 'Sold Out',
            'tag1' : '-40%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sold',
            'price' : '129',
        },
        {
            'id' : 24,
            'img' : '/static/assets/img/product/17.png', 
            'title' : 'Skinny Jeans',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '32 Reviews',
            'star' : 'filled',
            'style' : 'bg-sale',
            'price' : '99 - $129',
        },
        {
            'id' : 25,
            'img' : '/static/assets/img/product/18.png', 
            'title' : 'Mini Skirts',
            'tag' : 'New',
            'tag1' : '-55%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-new',
            'price' : '50 - $149',
        },
        {
            'id' : 26,
            'img' : '/static/assets/img/product/19.png', 
            'title' : 'Straight-Leg Jeans',
            'tag' : 'Hot',
            'tag1' : '-30%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-hot',
            'price' : '199',
        },
        {
            'id' : 27,
            'img' : '/static/assets/img/product/20.png', 
            'title' : 'Westside Denim Shorts',
            'tag' : 'New',
            'tag1' : None,
            'reviews' : '42 Reviews',
            'star' : 'filled',
            'style' : 'bg-new',
            'price' : '110 - $600',
        },
        {
            'id' : 28,
            'img' : '/static/assets/img/product/21.png', 
            'title' : 'Flare Maxi Dress',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sale',
            'price' : '99 - $110',
        },
        {
            'id' : 29,
            'img' : '/static/assets/img/product/22.png', 
            'title' : 'T Shirt Mockup Gray',
            'tag' : 'Sold Out',
            'tag1' : '-60%',
            'reviews' : '15 Reviews',
            'star' : 'filled',
            'style' : 'bg-sold',
            'price' : '119',
        },
        {
            'id' : 30,
            'img' : '/static/assets/img/product/7.jpg',
            'img1' : '/static/assets/img/product/7-a.jpg',
            'title' : 'Beautiful Design Dress',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 99,
            'original_price' : 129,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 31,
            'img' : '/static/assets/img/product/8.jpg',
            'img1' : '/static/assets/img/product/8-a.jpg',
            'title' : 'women Down Jacket',
            'tag' : 'New',
            'style' : 'bg-new',
            'price' : 79,
            'original_price' : 129,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 32,
            'img' : '/static/assets/img/product/9.jpg',
            'img1' : '/static/assets/img/product/9-a.jpg',
            'title' : 'women rompers',
            'tag' : False,
            'style' : '',
            'price' : 80,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 33,
            'img' : '/static/assets/img/product/a.jpg', 
            'title' : 'Homer Vase',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 119,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 34,
            'img' : '/static/assets/img/product/b.jpg', 
            'title' : 'Sala Vase',
            'tag' : 'New',
            'style' : 'bg-new',
            'price' : 79,
            'original_price' : 129,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 35,
            'img' : '/static/assets/img/product/c.jpg', 
            'title' : 'Corbin Vase',
            'tag' : False,
            'style' : '',
            'price' : 80,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 36,
            'img' : '/static/assets/img/product/d.jpg', 
            'title' : 'Penny Vase',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 110,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 37,
            'img' : '/static/assets/img/product/e.jpg', 
            'title' : 'Chika Vase',
            'tag' : False,
            'style' : '',
            'price' : 49,
            'original_price' : 90,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 38,
            'img' : '/static/assets/img/product/e.jpg', 
            'title' : 'Little Fatty Vase',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 114,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 39,
            'img' : '/static/assets/img/product/f.jpg', 
            'title' : 'Arc Vessel',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 120,
            'original_price' : None,
            'class' : 'ft-medium theme-cl fs-md text-dark',
        },
        {
            'id' : 40,
            'img' : '/static/assets/img/product/g.jpg', 
            'title' : 'Tubular Vase',
            'tag' : False,
            'style' : '',
            'price' : 129,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 41,
            'img' : '/static/assets/img/furniture/1.png', 
            'title' : 'Armchair',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 119,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 42,
            'img' : '/static/assets/img/furniture/2.png', 
            'title' : 'Rocking Chair',
            'tag' : 'New',
            'style' : 'bg-new',
            'price' : 79,
            'original_price' : 129,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 43,
            'img' : '/static/assets/img/furniture/3.png', 
            'title' : 'Desk Chair',
            'tag' : False,
            'style' : '',
            'price' : 80,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 44,
            'img' : '/static/assets/img/furniture/4.png', 
            'title' : 'Dining Chair',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 110,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 45,
            'img' : '/static/assets/img/furniture/5.png', 
            'title' : 'Folding Chair',
            'tag' : False,
            'style' : '',
            'price' : 49,
            'original_price' : 90,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 46,
            'img' : '/static/assets/img/furniture/6.png', 
            'title' : 'Lounge Chair',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 114,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 47,
            'img' : '/static/assets/img/furniture/7.png', 
            'title' : 'Wingback Chair',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 120,
            'original_price' : None,
            'class' : 'ft-medium theme-cl fs-md text-dark',
        },
        {
            'id' : 48,
            'img' : '/static/assets/img/furniture/8.png', 
            'title' : 'Barrel Chair',
            'tag' : False,
            'style' : '',
            'price' : 129,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 49,
            'img' : '/static/assets/img/grocery/1.png', 
            'title' : 'Garden radish',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'reviews' : '5 Reviews',
            'price' : 33,
        },
        {
            'id' : 50,
            'img' : '/static/assets/img/grocery/2.png', 
            'title' : 'Broccoli',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'reviews' : '5 Reviews',
            'price' : 99,
        },
        {
            'id' : 51,
            'img' : '/static/assets/img/grocery/3.png', 
            'title' : 'Hybrid Tomato',
            'tag' : '-50%',
            'style' : 'bg-danger',
            'reviews' : '5 Reviews',
            'price' : 30,
        },
        {
            'id' : 52,
            'img' : '/static/assets/img/grocery/4.png', 
            'title' : 'Spinach',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'reviews' : '5 Reviews',
            'price' : 24,
        },
        {
            'id' : 53,
            'img' : '/static/assets/img/grocery/5.png', 
            'title' : 'Green Cucumber',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'reviews' : '5 Reviews',
            'price' : 40,
        },
        {
            'id' : 54,
            'img' : '/static/assets/img/grocery/6.png', 
            'title' : 'French Beans',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'reviews' : '5 Reviews',
            'price' : 44,
        },
        {
            'id' : 55,
            'img' : '/static/assets/img/grocery/7.png', 
            'title' : 'Beetroot',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'reviews' : '5 Reviews',
            'price' : 16,
        },
        {
            'id' : 56,
            'img' : '/static/assets/img/grocery/8.png', 
            'title' : 'Horseradish',
            'tag' : '-25%',
            'style' : 'bg-danger',
            'reviews' : '5 Reviews',
            'price' : 100,
        },
        {
            'id' : 57,
            'img' : '/static/assets/img/grocery/9.png', 
            'title' : 'Leek',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'reviews' : '5 Reviews',
            'price' : 72,
        },
        {
            'id' : 58,
            'img' : '/static/assets/img/grocery/10.png', 
            'title' : 'Green Peas',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'reviews' : '5 Reviews',
            'price' : 65,
        },
        {
            'id' : 59,
            'img' : '/static/assets/img/grocery/11.png', 
            'title' : 'Ginger',
            'tag' : '-50%',
            'style' : 'bg-danger',
            'reviews' : '5 Reviews',
            'price' : 19,
        },
        {
            'id' : 60,
            'img' : '/static/assets/img/grocery/12.png', 
            'title' : 'Garlic',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'reviews' : '5 Reviews',
            'price' : 48,
        },
        {
            'id' : 61,
            'img' : '/static/assets/img/grocery/13.png', 
            'title' : 'Purple Brinjal',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'reviews' : '5 Reviews',
            'price' : 23,
        },
        {
            'id' : 62,
            'img' : '/static/assets/img/grocery/14.png', 
            'title' : 'Green Capsicum',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'reviews' : '5 Reviews',
            'price' : 29,
        },
        {
            'id' : 63,
            'img' : '/static/assets/img/grocery/15.png', 
            'title' : 'Orange Carrot',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'reviews' : '5 Reviews',
            'price' : 16,
        },
        {
            'id' : 64,
            'img' : '/static/assets/img/grocery/16.png', 
            'title' : 'Cabbage',
            'tag' : '-25%',
            'style' : 'bg-danger',
            'reviews' : '5 Reviews',
            'price' : 21,
        },
        {
            'id' : 65,
            'img' : '/static/assets/img/shop/9.png', 
            'title' : 'iPhone 13 Pro Max',
            'name' : 'Mobiles',
            'tag' : 'Sale',
            'tag1' : None,
            'style' : 'bg-sale',
            'rating' : 'filled',
            'price' : 39999,
        },
        {
            'id' : 66,
            'img' : '/static/assets/img/shop/10.png', 
            'title' : 'boAt Rockerz 425',
            'name' : 'Headphones',
            'tag' : 'New',
            'tag1' : '-40%',
            'style' : 'bg-new',
            'rating' : '',
            'price' : 1199,
        },
        {
            'id' : 67,
            'img' : '/static/assets/img/shop/11.png', 
            'title' : 'Apple iPhone 11(White)',
            'name' : 'Mobiles',
            'tag' : 'Sold Out',
            'tag1' : None,
            'style' : 'bg-sold',
            'rating' : 'filled',
            'price' : 18499,
        },
        {
            'id' : 68,
            'img' : '/static/assets/img/shop/4.png', 
            'title' : 'Apple iPhone 11(Black)',
            'name' : 'Mobiles',
            'tag' : 'New',
            'tag1' : '-55%',
            'style' : 'bg-new',
            'rating' : '',
            'price' : 48900,
        },
        {
            'id' : 69,
            'img' : '/static/assets/img/shop/5.png', 
            'title' : 'Canon EOS Digital Camera',
            'name' : 'Camera',
            'tag' : 'Sale',
            'tag1' : '-30%',
            'style' : 'bg-sale',
            'rating' : '',
            'price' : 33421,
        },
        {
            'id' : 70,
            'img' : '/static/assets/img/shop/6.png', 
            'title' : 'JBL JR310BT Wireless Headphones',
            'name' : 'Headphone',
            'tag' : 'New',
            'tag1' : None,
            'style' : 'bg-new',
            'rating' : 'filled',
            'price' : 12239,
        },
        {
            'id' : 71,
            'img' : '/static/assets/img/shop/7.png', 
            'title' : 'Sony 139 Cm Smart LED TV',
            'name' : 'TV/LCD',
            'tag' : 'Sale',
            'tag1' : None,
            'style' : 'bg-sale',
            'rating' : '',
            'price' : 81830,
        },
        {
            'id' : 72,
            'img' : '/static/assets/img/shop/8.png', 
            'title' : 'Sony WH-CH520 Pink Headphones',
            'name' : 'Headphone',
            'tag' : 'Sold Out',
            'tag1' : '-60%',
            'style' : 'bg-sold',
            'rating' : 'filled',
            'price' : 4490,
        },
        {
            'id' : 73,
            'img' : '/static/assets/img/shop/2.png', 
            'title' : 'iBenzer Macbook Air 13',
            'name' : 'Laptop',
            'tag' : '-50%',
            'style' : 'bg-danger',
            'price' : 58990,
        },
        {
            'id' : 74,
            'img' : '/static/assets/img/shop/14.png', 
            'title' : 'Tissot Tradition Powermatic',
            'name' : 'watch',
            'tag' : 'Sale',
            'tag1' : None,
            'style' : 'bg-sale',
            'rating' : 'filled',
            'price' : 49849,
        },
        {
            'id' : 75,
            'img' : '/static/assets/img/shop/15.png', 
            'title' : 'Tissot Men TRADITION',
            'name' : 'watch',
            'tag' : 'New',
            'tag1' : '-40%',
            'style' : 'bg-new',
            'rating' : '',
            'price' : 57850,
        },
        {
            'id' : 76,
            'img' : '/static/assets/img/shop/17.png', 
            'title' : 'IWC Portugieser Perpetual Watch',
            'name' : 'watch',
            'tag' : 'Sold Out',
            'tag1' : None,
            'style' : 'bg-sold',
            'rating' : 'filled',
            'price' : 44640,
        },
        {
            'id' : 77,
            'img' : '/static/assets/img/shop/18.png', 
            'title' : 'Michael Kors Men Runway Black Watch',
            'name' : 'watch',
            'tag' : 'Hot',
            'tag1' : '-55%',
            'style' : 'bg-hot',
            'rating' : '',
            'price' : 17706,
        },
        {
            'id' : 78,
            'img' : '/static/assets/img/shop/19.png', 
            'title' : 'Rolex Cosmograph Daytona Watch',
            'name' : 'watch',
            'tag' : 'Sale',
            'tag1' : '-30%',
            'style' : 'bg-sale',
            'rating' : '',
            'price' : 45492,
        },
        {
            'id' : 79,
            'img' : '/static/assets/img/shop/20.png', 
            'title' : "Movado Men's Bold Fusion Analog Watch",
            'name' : 'watch',
            'tag' : 'New',
            'tag1' : None,
            'style' : 'bg-new',
            'rating' : 'filled',
            'price' : 67125,
        },
        {
            'id' : 80,
            'img' : '/static/assets/img/shop/21.png', 
            'title' : 'Philipp Plein Men Stainless Steel Strap Watch',
            'name' : 'watch',
            'tag' : 'Sold',
            'tag1' : None,
            'style' : 'bg-sold',
            'rating' : '',
            'price' : 68400,
        },
        {
            'id' : 81,
            'img' : '/static/assets/img/shop/16.png', 
            'title' : 'Victorinox Men Green Dial Maverick Watch',
            'name' : 'watch',
            'tag' : 'New',
            'tag1' : '-60%',
            'style' : 'bg-new',
            'rating' : 'filled',
            'price' : 58395,
        }
    ]
    selected_product = next((product for product in products if slugify(product['title']) == title), None)

    if selected_product:
        return render_template('pages/shop-single-v1.html', product=selected_product)
    else:
        return "product not found", 404
    
    
@main.route("/shop-single-v2/")
def shop_single_v2():
    return render_template("pages/shop-single-v2.html")


@main.route("/shop-single-v3/")
def shop_single_v3():
    return render_template("pages/shop-single-v3.html")


@main.route("/shop-single-v4/")
def shop_single_v4():
    return render_template("pages/shop-single-v4.html")
    

@main.route('/shoping-cart/')
def shoping_cart():
    cart = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    tax = round(subtotal * 0.10, 2)
    total = round(subtotal + tax, 2)
    quantity_range = range(1, 11)

    return render_template(
        'pages/shoping-cart.html',
        cart=cart,
        subtotal=subtotal,
        tax=tax,
        total=total,
        quantity_range=quantity_range
    )
    

@main.route("/checkout/")
def checkout():
    cart = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    tax = round(subtotal * 0.10, 2)
    total = round(subtotal + tax, 2)
    quantity_range = range(1, 11)

    return render_template(
        'pages/checkout.html',
        cart=cart,
        subtotal=subtotal,
        tax=tax,
        total=total,
        quantity_range=quantity_range
    )


@main.route("/complete-order/")
def complete_order():
    return render_template("pages/complete-order.html")


@main.route("/blog/")
def blog():
    return render_template("pages/blog.html")


@main.route("/blog-detail/")
def blog_list_or_default():
    blogs = [
        {
            'id' : 1,
            'img' : '/static/assets/img/bl-2.png',
            'title' : "Lorem ipsum dolor sit amet, cons pisicing elit, sed do.",
        }
    ]
    blog = blogs[0]
    return render_template("pages/blog-detail.html", blog=blog)


@main.route("/blog-detail/<string:title>/")
def blog_detail(title):
    blogs = [
        {
            'id' : 1,
            'img' : '/static/assets/img/bl-1.png',
            'date' : '26 Sep 2025',
            'title' : "Let's start bring sale on this saummer vacation.",
            'desc' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis",
        },
        {
            'id' : 2,
            'img' : '/static/assets/img/bl-2.png',
            'date' : '17 July 2025',
            'title' : "collect moments, not things",
            'desc' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis",
        },
        {
            'id' : 3,
            'img' : '/static/assets/img/bl-3.png',
            'date' : '10 Aug 2025',
            'title' : "Always take the scenic route",
            'desc' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis",
        },
        {
            'id' : 4,
            'img' : '/static/assets/img/a-8.png',
            'date' : '26 Sep 2025',
            'title' : "Collecting Memories",
            'desc' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis",
        },
        {
            'id' : 5,
            'img' : '/static/assets/img/a-9.png',
            'date' : '17 July 2025',
            'title' : "Focus on Experiences",
            'desc' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis",
        },
        {
            'id' : 6,
            'img' : '/static/assets/img/a-10.png',
            'date' : '10 Aug 2025',
            'title' : "Living in the Now",
            'desc' : "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis",
        }
    ]
    selected_blog = next((blog for blog in blogs if slugify(blog['title']) == title), None)

    if selected_blog:
        return render_template('pages/blog-detail.html', blog=selected_blog)
    else:
        return "blog not found", 404


@main.route("/about-us/")
def about_us():
    return render_template("pages/about-us.html")


# /contact/ is now served by the `pages` blueprint with the upgraded shell
# (see app/blueprints/pages.py). Legacy KUMO route removed in Phase 15
# footer Wave 1 to avoid intercepting the new template.


@main.route("/email-confirmation/")
def email_confirmation():
    return render_template("pages/email-confirmation.html")


@main.route("/email-cart/")
def email_cart():
    return render_template("pages/email-cart.html")


@main.route("/email-offers/")
def email_offers():
    return render_template("pages/email-offers.html")


@main.route("/email-order-success/")
def email_order_success():
    return render_template("pages/email-order-success.html")


@main.route("/email-gift-voucher/")
def email_gift_voucher():
    return render_template("pages/email-gift-voucher.html")


@main.route("/email-reset-password/")
def email_reset_password():
    return render_template("pages/email-reset-password.html")


@main.route("/email-item-review/")
def email_item_review():
    return render_template("pages/email-item-review.html")


@main.route("/comingsoon/")
def comingsoon():
    return render_template("pages/comingsoon.html")


@main.route("/maintenance/")
def maintenance():
    return render_template("pages/maintenance.html")


@main.route("/404/")
def Notfound():
    return render_template("pages/404.html")


# /login/, /signup/, /forgot-password/ (plus /verify-otp/, /reset-password/,
# /logout/) are now served by the `auth` blueprint Ã¢â‚¬â€ see app/blueprints/auth.py


# /privacy/ and /faq/ are now served by the `pages` blueprint with the
# upgraded shell (see app/blueprints/pages.py). Legacy KUMO routes removed
# in Phase 15 footer Wave 1 to avoid intercepting the new templates.


@main.route("/docs/")
def docs():
    return render_template("pages/docs.html")


@main.route("/shop-grid-3/")
def shop_grid_3():
    return render_template("pages/shop-grid-3.html")


@main.route("/shop-list-sidebar/")
def shop_list_sidebar():
    return render_template("pages/shop-list-sidebar.html")
    

# quickview data
    
PRODUCTS = {
    1 : {
        'id' : 1,
        'img' : '/static/assets/img/product/1.jpg', 
        'title' : 'Half Running Set',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'price' : 119,
        'original_price' : None,
        'class' : 'fw-medium fs-md text-dark',
    },
    2 : {
        'id' : 2,
        'img' : '/static/assets/img/product/2.jpg', 
        'title' : 'Formal Men Lowers',
        'tag' : 'Sold Out',
        'style' : 'bg-sold',
        'price' : 79,
        'original_price' : 129,
        'class' : 'ft-medium theme-cl fs-md',
    },
    3 : {
        'id' : 3,
        'img' : '/static/assets/img/product/3.jpg', 
        'title' : 'Half Running Suit',
        'tag' : False,
        'style' : '',
        'price' : 80,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    4 : {
        'id' : 4,
        'img' : '/static/assets/img/product/4.jpg', 
        'title' : 'Half Fancy Lady Dress',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'price' : 110,
        'original_price' : 149,
        'class' : 'ft-medium theme-cl fs-md',
    },
    5 : {
        'id' : 5,
        'img' : '/static/assets/img/product/5.jpg', 
        'title' : 'Flix Flox Jeans',
        'tag' : False,
        'style' : '',
        'price' : 49,
        'original_price' : 90,
        'class' : 'ft-medium theme-cl fs-md',
    },
    6 : {
        'id' : 6,
        'img' : '/static/assets/img/product/6.jpg', 
        'title' : 'Fancy Salwar Suits',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'price' : 114,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    7 : {
        'id' : 7,
        'img' : '/static/assets/img/product/7.jpg', 
        'title' : 'Collot Full Dress',
        'tag' : 'Sale',
        'style' : 'bg-new',
        'price' : 120,
        'original_price' : None,
        'class' : 'ft-medium theme-cl fs-md text-dark',
    },
    8 : {
        'id' : 8,
        'img' : '/static/assets/img/product/8.jpg', 
        'title' : 'Formal Fluex Kurti',
        'tag' : False,
        'style' : '',
        'price' : 129,
        'original_price' : 149,
        'class' : 'ft-medium theme-cl fs-md',
    },
    9 : {
        'id' : 9,
        'img' : '/static/assets/img/product/2.jpg', 
        'title' : 'Women Striped Shirt Dress',
        'tag' : 'Sale',
        'tag1' : None,
        'reviews' : '5 Reviews',
        'star' : 'filled',
        'style' : 'bg-sale',
        'price' : 129,
    },
    10 : {
        'id' : 10,
        'img' : '/static/assets/img/product/3.jpg', 
        'title' : 'Boys Solid Sweatshirt',
        'tag' : 'Sold Out',
        'tag1' : '-40%',
        'reviews' : '0 Reviews',
        'star' : '',
        'style' : 'bg-sold',
        'price' : 129,
    },
    11 : {
        'id' : 11,
        'img' : '/static/assets/img/product/1.jpg', 
        'title' : 'Girls Floral Print Jumpsuit',
        'tag' : 'Sale',
        'tag1' : None,
        'reviews' : '32 Reviews',
        'star' : 'filled',
        'style' : 'bg-sale',
        'price' : 99,
    },
    12 : {
        'id' : 12,
        'img' : '/static/assets/img/product/6.jpg', 
        'title' : 'Girls Solid A-Line Dress',
        'tag' : 'New',
        'tag1' : '-55%',
        'reviews' : '0 Reviews',
        'star' : '',
        'style' : 'bg-new',
        'price' : 149,
    },
    13 : {
        'id' : 13,
        'img' : '/static/assets/img/product/7.jpg', 
        'title' : 'Printed Straight Kurta',
        'tag' : 'New',
        'tag1' : '-30%',
        'reviews' : '0 Reviews',
        'star' : '',
        'style' : 'bg-new',
        'price' : 199,
    },
    14 : {
        'id' : 14,
        'img' : '/static/assets/img/product/3.jpg', 
        'title' : 'Women Printed A-Line Dress',
        'tag' : 'Sale',
        'tag1' : None,
        'reviews' : '42 Reviews',
        'star' : 'filled',
        'style' : 'bg-sale',
        'price' : 110,
    },
    15 : {
        'id' : 15,
        'img' : '/static/assets/img/product/9.jpg', 
        'title' : 'Girls Fit and Flare Dress',
        'tag' : 'Sale',
        'tag1' : None,
        'reviews' : '0 Reviews',
        'star' : '',
        'style' : 'bg-sale',
        'price' : 99,
    },
    16 : {
        'id' : 16,
        'img' : '/static/assets/img/product/6.jpg', 
        'title' : 'Girls Self Design Jumpsuit',
        'tag' : 'New',
        'tag1' : '-60%',
        'reviews' : '15 Reviews',
        'star' : 'filled',
        'style' : 'bg-new',
        'price' : 119,
    },
    17 : {
        'id' : 17,
        'img' : '/static/assets/img/product/10.jpg', 
        'title' : 'Boys White T-shirt',
        'tag' : 'New',
        'tag1' : '-55%',
        'reviews' : '0 Reviews',
        'star' : '',
        'style' : 'bg-new',
        'price' : 149,
    },
    18 : {
        'id' : 18,
        'img' : '/static/assets/img/product/11.jpg', 
        'title' : 'Boys yellow-green T-shirt',
        'tag' : 'Sale',
        'tag1' : '-30%',
        'reviews' : '0 Reviews',
        'star' : '',
        'style' : 'bg-sale',
        'price' : 199,
    },
    19 : {
        'id' : 19,
        'img' : '/static/assets/img/product/12.jpg', 
        'title' : 'Women White T-shirt',
        'tag' : 'Sold Out',
        'tag1' : None,
        'reviews' : '42 Reviews',
        'star' : 'filled',
        'style' : 'bg-sold',
        'price' : 600,
    },
    20 : {
        'id' : 20,
        'img' : '/static/assets/img/product/13.jpg', 
        'title' : 'Boys Shorts',
        'tag' : 'Sale',
        'tag1' : None,
        'reviews' : '0 Reviews',
        'star' : '',
        'style' : 'bg-sale',
        'price' : 110,
    },
    21 : {
        'id' : 21,
        'img' : '/static/assets/img/product/14.jpg', 
        'title' : 'Boys yellow T-shirt',
        'tag' : 'New',
        'tag1' : '-60%',
        'reviews' : '15 Reviews',
        'star' : 'filled',
        'style' : 'bg-new',
        'price' : 119,
    },
    30 : {
        'id' : 30,
        'img' : '/static/assets/img/product/7.jpg',
        'img1' : '/static/assets/img/product/7-a.jpg',
        'title' : 'Beautiful Design Dress',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'price' : 99,
        'original_price' : 129,
        'class' : 'ft-medium theme-cl fs-md',
    },
    31 : {
        'id' : 31,
        'img' : '/static/assets/img/product/8.jpg',
        'img1' : '/static/assets/img/product/8-a.jpg',
        'title' : 'women Down Jacket',
        'tag' : 'New',
        'style' : 'bg-new',
        'price' : 79,
        'original_price' : 129,
        'class' : 'ft-medium theme-cl fs-md',
    },
    32 : {
        'id' : 32,
        'img' : '/static/assets/img/product/9.jpg',
        'img1' : '/static/assets/img/product/9-a.jpg',
        'title' : 'women rompers',
        'tag' : False,
        'style' : '',
        'price' : 80,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    33 : {
        'id' : 33,
        'img' : '/static/assets/img/product/a.jpg', 
        'title' : 'Homer Vase',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'price' : 119,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    34 : {
        'id' : 34,
        'img' : '/static/assets/img/product/b.jpg', 
        'title' : 'Sala Vase',
        'tag' : 'New',
        'style' : 'bg-new',
        'price' : 79,
        'original_price' : 129,
        'class' : 'ft-medium theme-cl fs-md',
    },
    35 : {
        'id' : 35,
        'img' : '/static/assets/img/product/c.jpg', 
        'title' : 'Corbin Vase',
        'tag' : False,
        'style' : '',
        'price' : 80,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    36 : {
        'id' : 36,
        'img' : '/static/assets/img/product/d.jpg', 
        'title' : 'Penny Vase',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'price' : 110,
        'original_price' : 149,
        'class' : 'ft-medium theme-cl fs-md',
    },
    37 : {
        'id' : 37,
        'img' : '/static/assets/img/product/e.jpg', 
        'title' : 'Chika Vase',
        'tag' : False,
        'style' : '',
        'price' : 49,
        'original_price' : 90,
        'class' : 'ft-medium theme-cl fs-md',
    },
    38 : {
        'id' : 38,
        'img' : '/static/assets/img/product/e.jpg', 
        'title' : 'Little Fatty Vase',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'price' : 114,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    39 : {
        'id' : 39,
        'img' : '/static/assets/img/product/f.jpg', 
        'title' : 'Arc Vessel',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'price' : 120,
        'original_price' : None,
        'class' : 'ft-medium theme-cl fs-md text-dark',
    },
    40 : {
        'id' : 40,
        'img' : '/static/assets/img/product/g.jpg', 
        'title' : 'Tubular Vase',
        'tag' : False,
        'style' : '',
        'price' : 129,
        'original_price' : 149,
        'class' : 'ft-medium theme-cl fs-md',
    },
    41 : {
        'id' : 41,
        'img' : '/static/assets/img/furniture/1.png', 
        'title' : 'Armchair',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'price' : 119,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    42 : {
        'id' : 42,
        'img' : '/static/assets/img/furniture/2.png', 
        'title' : 'Rocking Chair',
        'tag' : 'New',
        'style' : 'bg-new',
        'price' : 79,
        'original_price' : 129,
        'class' : 'ft-medium theme-cl fs-md',
    },
    43 : {
        'id' : 43,
        'img' : '/static/assets/img/furniture/3.png', 
        'title' : 'Desk Chair',
        'tag' : False,
        'style' : '',
        'price' : 80,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    44 : {
        'id' : 44,
        'img' : '/static/assets/img/furniture/4.png', 
        'title' : 'Dining Chair',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'price' : 110,
        'original_price' : 149,
        'class' : 'ft-medium theme-cl fs-md',
    },
    45 : {
        'id' : 45,
        'img' : '/static/assets/img/furniture/5.png', 
        'title' : 'Folding Chair',
        'tag' : False,
        'style' : '',
        'price' : 49,
        'original_price' : 90,
        'class' : 'ft-medium theme-cl fs-md',
    },
    46 : {
        'id' : 46,
        'img' : '/static/assets/img/furniture/6.png', 
        'title' : 'Lounge Chair',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'price' : 114,
        'original_price' : None,
        'class' : 'ft-medium fs-md text-dark',
    },
    47 : {
        'id' : 47,
        'img' : '/static/assets/img/furniture/7.png', 
        'title' : 'Wingback Chair',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'price' : 120,
        'original_price' : None,
        'class' : 'ft-medium theme-cl fs-md text-dark',
    },
    48 : {
        'id' : 48,
        'img' : '/static/assets/img/furniture/8.png', 
        'title' : 'Barrel Chair',
        'tag' : False,
        'style' : '',
        'price' : 129,
        'original_price' : 149,
        'class' : 'ft-medium theme-cl fs-md',
    },
    49 : {
        'id' : 49,
        'img' : '/static/assets/img/grocery/1.png', 
        'title' : 'Garden radish',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'reviews' : '5 Reviews',
        'price' : 33,
    },
    50 : {
        'id' : 50,
        'img' : '/static/assets/img/grocery/2.png', 
        'title' : 'Broccoli',
        'tag' : 'Sold Out',
        'style' : 'bg-sold',
        'reviews' : '5 Reviews',
        'price' : 99,
    },
    51 : {
        'id' : 51,
        'img' : '/static/assets/img/grocery/3.png', 
        'title' : 'Hybrid Tomato',
        'tag' : '-50%',
        'style' : 'bg-danger',
        'reviews' : '5 Reviews',
        'price' : 30,
    },
    52 : {
        'id' : 52,
        'img' : '/static/assets/img/grocery/4.png', 
        'title' : 'Spinach',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'reviews' : '5 Reviews',
        'price' : 24,
    },
    53 : {
        'id' : 53,
        'img' : '/static/assets/img/grocery/5.png', 
        'title' : 'Green Cucumber',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'reviews' : '5 Reviews',
        'price' : 40,
    },
    54 : {
        'id' : 54,
        'img' : '/static/assets/img/grocery/6.png', 
        'title' : 'French Beans',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'reviews' : '5 Reviews',
        'price' : 44,
    },
    55 : {
        'id' : 55,
        'img' : '/static/assets/img/grocery/7.png', 
        'title' : 'Beetroot',
        'tag' : 'Sold Out',
        'style' : 'bg-sold',
        'reviews' : '5 Reviews',
        'price' : 16,
    },
    56 : {
        'id' : 56,
        'img' : '/static/assets/img/grocery/8.png', 
        'title' : 'Horseradish',
        'tag' : '-25%',
        'style' : 'bg-danger',
        'reviews' : '5 Reviews',
        'price' : 100,
    },
    57 : {
        'id' : 57,
        'img' : '/static/assets/img/grocery/9.png', 
        'title' : 'Leek',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'reviews' : '5 Reviews',
        'price' : 72,
    },
    58 : {
        'id' : 58,
        'img' : '/static/assets/img/grocery/10.png', 
        'title' : 'Green Peas',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'reviews' : '5 Reviews',
        'price' : 65,
    },
    59 : {
        'id' : 59,
        'img' : '/static/assets/img/grocery/11.png', 
        'title' : 'Ginger',
        'tag' : '-50%',
        'style' : 'bg-danger',
        'reviews' : '5 Reviews',
        'price' : 19,
    },
    60 : {
        'id' : 60,
        'img' : '/static/assets/img/grocery/12.png', 
        'title' : 'Garlic',
        'tag' : 'Sold Out',
        'style' : 'bg-sold',
        'reviews' : '5 Reviews',
        'price' : 48,
    },
    61 : {
        'id' : 61,
        'img' : '/static/assets/img/grocery/13.png', 
        'title' : 'Purple Brinjal',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'reviews' : '5 Reviews',
        'price' : 23,
    },
    62 : {
        'id' : 62,
        'img' : '/static/assets/img/grocery/14.png', 
        'title' : 'Green Capsicum',
        'tag' : 'Hot',
        'style' : 'bg-hot',
        'reviews' : '5 Reviews',
        'price' : 29,
    },
    63 : {
        'id' : 63,
        'img' : '/static/assets/img/grocery/15.png', 
        'title' : 'Orange Carrot',
        'tag' : 'Sale',
        'style' : 'bg-sale',
        'reviews' : '5 Reviews',
        'price' : 16,
    },
    64 : {
        'id' : 64,
        'img' : '/static/assets/img/grocery/16.png', 
        'title' : 'Cabbage',
        'tag' : '-25%',
        'style' : 'bg-danger',
        'reviews' : '5 Reviews',
        'price' : 21,
    },
    65 : {
        'id' : 65,
        'img' : '/static/assets/img/shop/9.png', 
        'title' : 'iPhone 13 Pro Max',
        'name' : 'Mobiles',
        'tag' : 'Sale',
        'tag1' : None,
        'style' : 'bg-sale',
        'rating' : 'filled',
        'price' : 39999,
    },
    66 : {
        'id' : 66,
        'img' : '/static/assets/img/shop/10.png', 
        'title' : 'boAt Rockerz 425',
        'name' : 'Headphones',
        'tag' : 'New',
        'tag1' : '-40%',
        'style' : 'bg-new',
        'rating' : '',
        'price' : 1199,
    },
    67 : {
        'id' : 67,
        'img' : '/static/assets/img/shop/11.png', 
        'title' : 'Apple iPhone 11(White)',
        'name' : 'Mobiles',
        'tag' : 'Sold Out',
        'tag1' : None,
        'style' : 'bg-sold',
        'rating' : 'filled',
        'price' : 18499,
    },
    68 : {
        'id' : 68,
        'img' : '/static/assets/img/shop/4.png', 
        'title' : 'Apple iPhone 11(Black)',
        'name' : 'Mobiles',
        'tag' : 'New',
        'tag1' : '-55%',
        'style' : 'bg-new',
        'rating' : '',
        'price' : 48900,
    },
    69 : {
        'id' : 69,
        'img' : '/static/assets/img/shop/5.png', 
        'title' : 'Canon EOS Digital Camera',
        'name' : 'Camera',
        'tag' : 'Sale',
        'tag1' : '-30%',
        'style' : 'bg-sale',
        'rating' : '',
        'price' : 33421,
    },
    70 : {
        'id' : 70,
        'img' : '/static/assets/img/shop/6.png', 
        'title' : 'JBL JR310BT Wireless Headphones',
        'name' : 'Headphone',
        'tag' : 'New',
        'tag1' : None,
        'style' : 'bg-new',
        'rating' : 'filled',
        'price' : 12239,
    },
    71 : {
        'id' : 71,
        'img' : '/static/assets/img/shop/7.png', 
        'title' : 'Sony 139 Cm Smart LED TV',
        'name' : 'TV/LCD',
        'tag' : 'Sale',
        'tag1' : None,
        'style' : 'bg-sale',
        'rating' : '',
        'price' : 81830,
    },
    72 : {
        'id' : 72,
        'img' : '/static/assets/img/shop/8.png', 
        'title' : 'Sony WH-CH520 Pink Headphones',
        'name' : 'Headphone',
        'tag' : 'Sold Out',
        'tag1' : '-60%',
        'style' : 'bg-sold',
        'rating' : 'filled',
        'price' : 4490,
    },
    74 : {
        'id' : 74,
        'img' : '/static/assets/img/shop/14.png', 
        'title' : 'Tissot Tradition Powermatic',
        'name' : 'watch',
        'tag' : 'Sale',
        'tag1' : None,
        'style' : 'bg-sale',
        'rating' : 'filled',
        'price' : 49849,
    },
    75 : {
        'id' : 75,
        'img' : '/static/assets/img/shop/15.png', 
        'title' : 'Tissot Men TRADITION',
        'name' : 'watch',
        'tag' : 'New',
        'tag1' : '-40%',
        'style' : 'bg-new',
        'rating' : '',
        'price' : 57850,
    },
    76 : {
        'id' : 76,
        'img' : '/static/assets/img/shop/17.png', 
        'title' : 'IWC Portugieser Perpetual Watch',
        'name' : 'watch',
        'tag' : 'Sold Out',
        'tag1' : None,
        'style' : 'bg-sold',
        'rating' : 'filled',
        'price' : 44640,
    },
    77 : {
        'id' : 77,
        'img' : '/static/assets/img/shop/18.png', 
        'title' : 'Michael Kors Men Runway Black Watch',
        'name' : 'watch',
        'tag' : 'Hot',
        'tag1' : '-55%',
        'style' : 'bg-hot',
        'rating' : '',
        'price' : 17706,
    },
    78 : {
        'id' : 78,
        'img' : '/static/assets/img/shop/19.png', 
        'title' : 'Rolex Cosmograph Daytona Watch',
        'name' : 'watch',
        'tag' : 'Sale',
        'tag1' : '-30%',
        'style' : 'bg-sale',
        'rating' : '',
        'price' : 45492,
    },
    79 : {
        'id' : 79,
        'img' : '/static/assets/img/shop/20.png', 
        'title' : "Movado Men's Bold Fusion Analog Watch",
        'name' : 'watch',
        'tag' : 'New',
        'tag1' : None,
        'style' : 'bg-new',
        'rating' : 'filled',
        'price' : 67125,
    },
    80 : {
        'id' : 80,
        'img' : '/static/assets/img/shop/21.png', 
        'title' : 'Philipp Plein Men Stainless Steel Strap Watch',
        'name' : 'watch',
        'tag' : 'Sold',
        'tag1' : None,
        'style' : 'bg-sold',
        'rating' : '',
        'price' : 68400,
    },
    81 : {
        'id' : 81,
        'img' : '/static/assets/img/shop/16.png', 
        'title' : 'Victorinox Men Green Dial Maverick Watch',
        'name' : 'watch',
        'tag' : 'New',
        'tag1' : '-60%',
        'style' : 'bg-new',
        'rating' : 'filled',
        'price' : 58395,
    },
}


@main.route('/product/<int:id>')
def product_detail_json(id):
    product = PRODUCTS.get(id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product)




# Add-Card

MONTHS = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]

YEARS = list(range(2025, 2031))


@main.route('/payment-method/')
def payment_method():
    cards = session.get('cards', [])
    return render_template('pages/payment-method.html', cards=cards)


@main.route('/add-card')
def add_card_form():
    edit_id = request.args.get('edit_id')
    edit_card = None
    cards = session.get('cards', [])

    if edit_id:
        for card in cards:
            if card['id'] == edit_id:
                edit_card = card
                break

    return render_template('pages/add-card.html', editCard=edit_card, edit_id=edit_id, months=MONTHS, years=YEARS)


@main.route('/store-card', methods=['POST'])
def store_card():
    data = request.form.to_dict()
    errors = []

    required_fields = ['card_holder', 'card_number', 'expire_month', 'expire_year', 'cvc', 'ak-2']
    for field in required_fields:
        if not data.get(field):
            field_name = field.replace('-', ' ').capitalize()
            errors.append(f"{field_name} is required.")

    if errors:
        for error in errors:
            flash(error, 'danger')

        edit_id = data.get('edit_id')
        return render_template('pages/add-card.html', editCard=data, edit_id=edit_id, months=MONTHS, years=YEARS)

    cards = session.get('cards', [])
    edit_id = data.get('edit_id')

    if edit_id:
        for i, card in enumerate(cards):
            if card['id'] == edit_id:
                cards[i] = {**card, **data, 'id': edit_id}
                break
    else:
        data['id'] = str(uuid.uuid4())
        cards.append(data)

    session['cards'] = cards
    flash("Card saved successfully.", "success")
    return redirect(url_for('main.payment_method'))


@main.route('/delete-card/<string:id>')
def delete_card(id):
    cards = session.get('cards', [])
    cards = [card for card in cards if card['id'] != id]
    session['cards'] = cards
    flash("Card deleted successfully.", "success")
    return redirect(url_for('main.payment_method'))
