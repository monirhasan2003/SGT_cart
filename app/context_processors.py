# app/context_processors.py
from flask import request
from slugify import slugify


# categorys data

def global_categorys():
    categorys = [
        {
            'img' : '/static/assets/img/a-1.png', 
            'title' : 'Mens', 
            'name' : 'Shop Mens', 
        },
        {
            'img' : '/static/assets/img/a-2.png', 
            'title' : 'Kids', 
            'name' : 'Shop Kids', 
        },
        {
            'img' : '/static/assets/img/a-3.png', 
            'title' : 'Womens', 
            'name' : 'Shop Womens', 
        }
    ]
    return {"categorys": categorys}


# products data

def global_products():
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
    return {"products": products}


# reviews data

def global_reviews():
    reviews = [
        {
            'img' : '/static/assets/img/team-1.jpg', 
            'name' : 'Mark Jevenue',
            'title' : 'CEO of Addle',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.',
        },
        {
            'img' : '/static/assets/img/team-2.jpg', 
            'name' : 'Henna Bajaj',
            'title' : 'Aqua Founder',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.',
        },
        {
            'img' : '/static/assets/img/team-3.jpg', 
            'name' : 'John Cenna',
            'title' : 'CEO of Plike',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.',
        },
        {
            'img' : '/static/assets/img/team-4.jpg', 
            'name' : 'Madhu Sharma',
            'title' : 'Team Manager',
            'desc' : 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum.',
        }
    ]
    return {"reviews": reviews}


# blogs data

def global_blogs():
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
    return {"blogs": blogs}


# insta data

def global_insta():
    insta = [
        {
            'img' : '/static/assets/img/i-1.png',
        },
        {
            'img' : '/static/assets/img/i-2.png',
        },
        {
            'img' : '/static/assets/img/i-3.png',
        },
        {
            'img' : '/static/assets/img/i-7.png',
        },
        {
            'img' : '/static/assets/img/i-8.png',
        },
        {
            'img' : '/static/assets/img/i-4.png',
        },
        {
            'img' : '/static/assets/img/i-5.png',
        },
        {
            'img' : '/static/assets/img/i-6.png',
        },
        {
            'img' : '/static/assets/img/i-3.png',
        }
    ]
    return {"insta": insta}


# features data

def global_features():
    features = [
        {
            'icon' : 'fas fa-shopping-basket',
            'name' : 'Free Shipping',
            'title' : 'Capped at $10 per order',
        },
        {
            'icon' : 'far fa-credit-card',
            'name' : 'Secure Payments',
            'title' : 'Up to 6 months installments',
        },
        {
            'icon' : 'fas fa-shield-alt',
            'name' : '15-Days Returns',
            'title' : 'Shop with fully confidence',
        },
        {
            'icon' : 'fas fa-headphones-alt',
            'name' : '24x7 Fully Support',
            'title' : 'Get friendly support',
        }
    ]
    return {"features": features}


# slides data

def global_slides():
    slides = [
        {
            'img' : '/static/assets/img/banner-2.png',
            'name' : 'Winter Collection',
            'title' : 'New Winter',
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-5.png',
            'name' : 'Winter Collection',
            'title' : 'New Winter',
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-3.png',
            'name' : 'Winter Collection',
            'title' : 'New Winter',
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides": slides}


# categorys2 data

def global_categorys2():
    categorys2 = [
        {
            'img' : '/static/assets/img/b-8.png',
            'title' : "Women Clothes",
            'name' : '3272 Items',
            'btn' : 'Browse Items',
            'style' : 'lg_height',
        },
        {
            'img' : '/static/assets/img/b-5.png',
            'title' : "Men's Wear",
            'name' : '7632 Items',
            'btn' : 'Browse Items',
            'style' : 'md_height',
        }
    ]
    return {"categorys2": categorys2}


# categorys3 data

def global_categorys3():
    categorys3 = [
        {
            'img' : '/static/assets/img/b-3.png',
            'title' : "Kid's Wear",
            'name' : '4072 Items',
            'btn' : 'Browse Items',
            'style' : 'md_height',
        },
        {
            'img' : '/static/assets/img/b-7.png',
            'title' : "Men's Jackets",
            'name' : '9652 Items',
            'btn' : 'Browse Items',
            'style' : 'lg_height',
        }
    ]
    return {"categorys3": categorys3}


# navs data

def global_navs():
    navs = [
        {
            'title' : "All",
            'class' : "",
            'link' : "#all",
            'id' : "all-tab",
            'controls' : "all",
            'selected' : "true",
        },
        {
            'title' : "Men's",
            'class' : "active",
            'link' : "#mens",
            'id' : "mens-tab",
            'controls' : "mens",
            'selected' : "false",
        },
        {
            'title' : "Women",
            'class' : "",
            'link' : "#women",
            'id' : "women-tab",
            'controls' : "women",
            'selected' : "false",
        },
        {
            'title' : "Kids",
            'class' : "",
            'link' : "#kids",
            'id' : "kids-tab",
            'controls' : "kids",
            'selected' : "false",
        }
    ]
    return {"navs": navs}


# products2 data

def global_products2():
    products2 = [
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
        }
    ]
    return {"products2": products2}


# products3 data

def global_products3():
    products3 = [
        {
            'id' : 1,
            'img' : '/static/assets/img/product/1.jpg', 
            'title' : 'Half Running Set',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '32 Reviews',
            'star' : 'filled',
            'style' : 'bg-sale',
            'price' : 119,
        },
        {
            'id' : 4,
            'img' : '/static/assets/img/product/4.jpg', 
            'title' : 'Half Fancy Lady Dress',
            'tag' : 'New',
            'tag1' : '-55%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-new',
            'price' : 110,
        },
        {
            'id' : 5,
            'img' : '/static/assets/img/product/5.jpg', 
            'title' : 'Flix Flox Jeans',
            'tag' : 'Sale',
            'tag1' : '-30%',
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sale',
            'price' : 49,
        },
        {
            'id' : 3,
            'img' : '/static/assets/img/product/3.jpg', 
            'title' : 'Half Running Suit',
            'tag' : 'Sold Out',
            'tag1' : None,
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sold',
            'price' : 80,
        },
        {
            'id' : 2,
            'img' : '/static/assets/img/product/2.jpg', 
            'title' : 'Formal Men Lowers',
            'tag' : 'New',
            'tag1' : '-40%',
            'reviews' : '5 Reviews',
            'star' : 'filled',
            'style' : 'bg-new',
            'price' : 79,
        },
        {
            'id' : 8,
            'img' : '/static/assets/img/product/8.jpg', 
            'title' : 'Formal Fluex Kurti',
            'tag' : 'Sold Out',
            'tag1' : '-60%',
            'reviews' : '15 Reviews',
            'star' : 'filled',
            'style' : 'bg-sold',
            'price' : 129,
        },
        {
            'id' : 7,
            'img' : '/static/assets/img/product/7.jpg', 
            'title' : 'Collot Full Dress',
            'tag' : 'Sale',
            'tag1' : None,
            'reviews' : '0 Reviews',
            'star' : '',
            'style' : 'bg-sale',
            'price' : 120,
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
        }
    ]
    return {"products3": products3}


# slides2 data

def global_slides2():
    slides2 = [
        {
            'img' : '/static/assets/img/banner-24.png',
            'name' : 'Winter Collection',
            'title' : 'New Winter',
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-25.png',
            'name' : 'Winter Collection',
            'title' : 'New Winter',
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-26.png',
            'name' : 'Winter Collection',
            'title' : 'New Winter',
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides2": slides2}


# categories data

def global_categories():
    categories = [
        {
            'img' : '/static/assets/img/fashion.png',
            'title' : "Men's Wear",
        },
        {
            'img' : '/static/assets/img/tshirt.png',
            'title' : "Kid's Wear",
        },
        {
            'img' : '/static/assets/img/accessories.png',
            'title' : "Accessories",
        },
        {
            'img' : '/static/assets/img/sneakers.png',
            'title' : "Men's Shoes",
        },
        {
            'img' : '/static/assets/img/television.png',
            'title' : "Television",
        },
        {
            'img' : '/static/assets/img/pant.png',
            'title' : "Men's Pants",
        }
    ]
    return {"categories": categories}


# trendings data

def global_trendings():
    trendings = [
        {
            'id' : 1,
            'img' : '/static/assets/img/product/1.jpg', 
            'title' : 'Half Running Set',
            'tag' : 'Sale',
            'style' : 'bg-success',
            'price' : '99 - $129',
            'name' : 'color1',
            'id1' : 'white',
            'id2' : 'blue',
            'id3' : 'yellow',
            'id4' : 'pink',
            'check' : '',
        },
        {
            'id' : 2,
            'img' : '/static/assets/img/product/2.jpg', 
            'title' : 'Formal Men Lowers',
            'tag' : 'New',
            'style' : 'bg-info',
            'price' : '99 - $129',
            'name' : 'color2',
            'id1' : 'white2',
            'id2' : 'blue2',
            'id3' : 'yellow2',
            'id4' : 'pink2',
            'check' : '',
        },
        {
            'id' : 3,
            'img' : '/static/assets/img/product/3.jpg', 
            'title' : 'Half Running Suit',
            'tag' : False,
            'style' : '',
            'price' : '99 - $129',
            'name' : 'color3',
            'id1' : 'white3',
            'id2' : 'blue3',
            'id3' : 'yellow3',
            'id4' : 'pink3',
            'check' : '',
        },
        {
            'id' : 4,
            'img' : '/static/assets/img/product/4.jpg', 
            'title' : 'Half Fancy Lady Dress',
            'tag' : 'Hot',
            'style' : 'bg-warning',
            'price' : '99 - $129',
            'name' : 'color4',
            'id1' : 'white4',
            'id2' : 'blue4',
            'id3' : 'yellow4',
            'id4' : 'pink4',
            'check' : '',
        },
        {
            'id' : 5,
            'img' : '/static/assets/img/product/5.jpg', 
            'title' : 'Flix Flox Jeans',
            'tag' : False,
            'style' : '',
            'price' : '99 - $129',
            'name' : 'color5',
            'id1' : 'white5',
            'id2' : 'blue5',
            'id3' : 'yellow5',
            'id4' : 'pink5',
            'check' : '',
        },
        {
            'id' : 6,
            'img' : '/static/assets/img/product/6.jpg', 
            'title' : 'Fancy Salwar Suits',
            'tag' : 'Hot',
            'style' : 'bg-danger',
            'price' : '99 - $129',
            'name' : 'color6',
            'id1' : 'white6',
            'id2' : 'blue6',
            'id3' : 'yellow6',
            'id4' : 'pink6',
            'check' : '',
        },
        {
            'id' : 7,
            'img' : '/static/assets/img/product/7.jpg', 
            'title' : 'Collot Full Dress',
            'tag' : 'Sale',
            'style' : 'bg-success',
            'price' : '99 - $129',
            'name' : 'color7',
            'id1' : 'white7',
            'id2' : 'blue7',
            'id3' : 'yellow7',
            'id4' : 'pink7',
            'check' : '',
        },
        {
            'id' : 8,
            'img' : '/static/assets/img/product/8.jpg', 
            'title' : 'Formal Fluex Kurti',
            'tag' : 'Sale',
            'style' : 'bg-success',
            'price' : '99 - $129',
            'name' : 'color88',
            'id1' : 'white88',
            'id2' : 'blue88',
            'id3' : 'yellow88',
            'id4' : 'pink88',
            'check' : '',
        }
    ]
    return {"trendings": trendings}


# categorys4 data

def global_categorys4():
    categorys4 = [
        {
            'img' : '/static/assets/img/a-7.png', 
            'title' : "Women's",
            'collections' : "5670 Collections",
        },
        {
            'img' : '/static/assets/img/a-9.png', 
            'title' : "Men's",
            'collections' : "3220 Collections",
        },
        {
            'img' : '/static/assets/img/a-8.png', 
            'title' : "Kids",
            'collections' : "7412 Collections",
        },
        {
            'img' : '/static/assets/img/a-10.png', 
            'title' : "Accessories",
            'collections' : "6580 Collections",
        }
    ]
    return {"categorys4": categorys4}


# slides3 data

def global_slides3():
    slides3 = [
        {
            'img' : '/static/assets/img/slide-3.png',
            'name' : 'Winter Collection',
            'title' : "New Winter",
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/slide-4.png',
            'name' : 'Summer Collection',
            'title' : "Women's Fashion",
            'title1' : 'UpTo 30% Off',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/slide-1.png',
            'name' : 'Winter Collection',
            'title' : "New Winter",
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides3": slides3}


# categorys5 data

def global_categorys5():
    categorys5 = [
        {
            'img' : '/static/assets/img/c-22.png',
            'title' : 'Adventure Kille',
            'title1' : 'Goggles',
            'price' : 'Start From $10.99',
            'class' : 'right',
            'style' : 'left lis-top',
        },
        {
            'img' : '/static/assets/img/c-44.png',
            'title' : 'New Styles',
            'title1' : 'iPhones',
            'price' : 'Start From $500.99',
            'class' : 'left',
            'style' : 'right lis-bottom',
        }
    ]
    return {"categorys5": categorys5}


# deals data

def global_deals():
    deals = [
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
            'id' : 15,
            'img' : '/static/assets/img/product/9.jpg', 
            'title' : 'Girls Fit and Flare Dress',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 99,
            'original_price' : None,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 17,
            'img' : '/static/assets/img/product/10.jpg', 
            'title' : 'Boys White T-shirt',
            'tag' : 'New',
            'style' : 'bg-new',
            'price' : 149,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg', 
            'title' : 'Boys yellow-green T-shirt',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'price' : 199,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 19,
            'img' : '/static/assets/img/product/12.jpg', 
            'title' : 'Women White T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 600,
            'original_price' : 666,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 20,
            'img' : '/static/assets/img/product/13.jpg', 
            'title' : 'Boys Shorts',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 110,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 21,
            'img' : '/static/assets/img/product/14.jpg', 
            'title' : 'Boys yellow T-shirt',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 119,
            'original_price' : None,
            'class' : 'ft-medium theme-cl fs-md text-dark',
        }
    ]
    return {"deals": deals}


# banners data

def global_banners():
    banners = [
        {
            'img' : '/static/assets/img/bt-1.png', 
            'title' : 'New Collections',
            'name' : "SHOP MEN'S",
            'class' : 'fs-md',
            'btn' : 'Browse Items',
        },
        {
            'img' : '/static/assets/img/bt-2.png', 
            'title' : 'New Collections',
            'name' : "SHOP WOMEN'S",
            'class' : 'fs-lg',
            'btn' : 'Browse Items',
        }
    ]
    return {"banners": banners}


# banners2 data

def global_banners2():
    banners2 = [
        {
            'img' : '/static/assets/img/b-8.png',
            'off' : 'Up to 30% Off',
            'title' : 'Women Wear',
            'item' : '4232 Items',
            'btn' : 'Browse Items',
        },
        {
            'img' : '/static/assets/img/b-3.png',
            'off' : 'Up to 40% Off',
            'title' : 'Kids Wear',
            'item' : '5615 Items',
            'btn' : 'Browse Items',
        },
        {
            'img' : '/static/assets/img/c-8.png',
            'off' : 'Up to 45% Off',
            'title' : 'Kitchen Accessories',
            'item' : '3215 Items',
            'btn' : 'Browse Items',
        }
    ]
    return {"banners2": banners2}


# products4 data

def global_products4():
    products4 = [
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
            'id' : 17,
            'img' : '/static/assets/img/product/10.jpg',
            'img1' : '/static/assets/img/product/10-a.jpg',
            'title' : 'Boys White T-shirt',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 110,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg',
            'img1' : '/static/assets/img/product/11-a.jpg',
            'title' : 'Boys yellow-green T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 49,
            'original_price' : 90,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 19,
            'img' : '/static/assets/img/product/12.jpg',
            'img1' : '/static/assets/img/product/12-a.jpg',
            'title' : 'Women White T-shirt',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 114,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 20,
            'img' : '/static/assets/img/product/13.jpg',
            'img1' : '/static/assets/img/product/13-a.jpg',
            'title' : 'Boys Shorts',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 120,
            'original_price' : None,
            'class' : 'ft-medium theme-cl fs-md text-dark',
        },
        {
            'id' : 21,
            'img' : '/static/assets/img/product/14.jpg',
            'img1' : '/static/assets/img/product/14-a.jpg',
            'title' : 'Boys yellow T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 129,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        }
    ]
    return {"products4": products4}


# features2 data

def global_features2():
    features2 = [
        {
            'icon' : 'fas fa-shopping-basket',
            'name' : 'Free Shipping',
            'title' : 'Capped at $10 per order',
        },
        {
            'icon' : 'far fa-credit-card',
            'name' : 'Secure Payments',
            'title' : 'Up to 6 months installments',
        },
        {
            'icon' : 'fas fa-shield-alt',
            'name' : '15-Days Returns',
            'title' : 'Shop with fully confidence',
        },
        {
            'icon' : 'fas fa-headphones-alt',
            'name' : '24x7 Fully Support',
            'title' : 'Get friendly support',
        }
    ]
    return {"features2": features2}


# slides4 data

def global_slides4():
    slides4 = [
        {
            'img' : '/static/assets/img/banner-4.png',
            'name' : 'Winter Collection',
            'title' : "New Winter",
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-7.png',
            'name' : 'Summer Collection',
            'title' : "Women's Fashion",
            'title1' : 'UpTo 30% Off',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-11.png',
            'name' : 'Winter Collection',
            'title' : "New Winter",
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides4": slides4}


# categorys6 data

def global_categorys6():
    categorys6 = [
        {
            'img' : '/static/assets/img/b-3.png',
            'title' : "Kid's Wear",
            'item' : '8562 Items',
            'btn' : 'Browse Items',
        },
        {
            'img' : '/static/assets/img/b-5.png',
            'title' : "Men's Wear",
            'item' : '32 Items',
            'btn' : 'Browse Items',
        }
    ]
    return {"categorys6": categorys6}


# slides5 data

def global_slides5():
    slides5 = [
        {
            'img' : '/static/assets/img/banner-3.png',
            'name' : 'Winter Collection',
            'title' : "New Winter",
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-2.png',
            'name' : 'Winter Collection',
            'title' : "New Winter",
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-7.png',
            'name' : 'Winter Collection',
            'title' : "New Winter",
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides5": slides5}


# slides6 data

def global_slides6():
    slides6 = [
        {
            'img' : '/static/assets/img/banner-18.png',
            'name' : 'Save up to 60% off',
            'title' : "The Best Deals",
            'title1' : 'of The Year',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-19.png',
            'name' : 'Mega Sale',
            'title' : "Get up to 50% off",
            'title1' : 'Black Friday',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-20.png',
            'name' : 'Super Sale',
            'title' : "Online",
            'title1' : 'Fashion Shop',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides6": slides6}


# categorys7 data

def global_categorys7():
    categorys7 = [
        {
            'img' : '/static/assets/img/offer-1.png',
            'number' : '50%',
            'name' : 'Off',
            'title' : "Shop For Women's",
        },
        {
            'img' : '/static/assets/img/offer-2.png',
            'number' : '40%',
            'name' : 'Off',
            'title' : "Shop For Men's",
        }
    ]
    return {"categorys7": categorys7}


# slides7 data

def global_slides7():
    slides7 = [
        {
            'img' : '/static/assets/img/banner-13.png',
            'name' : 'Super Sale',
            'title' : 'Classic 2025',
            'title1' : 'Interior Designs',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-14.png',
            'name' : 'Up to 50% Off',
            'title' : 'Modern',
            'title1' : 'Furniture Brans',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-15.png',
            'name' : 'New Collections',
            'title' : 'New Collections',
            'title1' : 'of Armchair',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides7": slides7}


# styles data

def global_styles():
    styles = [
        {
            'img' : '/static/assets/img/c-3.png',
            'title' : 'Arm Chair',
            'item' : '762 Items',
        },
        {
            'img' : '/static/assets/img/c-5.png',
            'title' : 'Dinning Table',
            'item' : '512 Items',
        }
    ]
    return {"styles": styles}


# styles2 data

def global_styles2():
    styles2 = [
        {
            'img' : '/static/assets/img/c-11.png',
            'title' : 'Living Bes',
            'item' : '325 Items',
        },
        {
            'img' : '/static/assets/img/c-12.png',
            'title' : 'Lighting',
            'item' : '712 Items',
        }
    ]
    return {"styles2": styles2}


# insta2 data

def global_insta2():
    insta2 = [
        {
            'img' : '/static/assets/img/p-13.png',
        },
        {
            'img' : '/static/assets/img/p-14.png',
        },
        {
            'img' : '/static/assets/img/p-15.png',
        },
        {
            'img' : '/static/assets/img/p-16.png',
        },
        {
            'img' : '/static/assets/img/p-17.png',
        },
        {
            'img' : '/static/assets/img/p-18.png',
        },
        {
            'img' : '/static/assets/img/p-19.png',
        },
        {
            'img' : '/static/assets/img/p-20.png',
        },
        {
            'img' : '/static/assets/img/p-15.png',
        }
    ]
    return {"insta2": insta2}


# slides8 data

def global_slides8():
    slides8 = [
        {
            'img' : '/static/assets/img/banner-8.png',
            'name' : 'Super Sale',
            'title' : 'Classic 2025',
            'title1' : 'Interior Designs',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-9.png',
            'name' : 'Up to 50% Off',
            'title' : 'Modern',
            'title1' : 'Furniture Brans',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-10.png',
            'name' : 'New Collections',
            'title' : 'New Collections',
            'title1' : 'of Armchair',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides8": slides8}


# styles3 data

def global_styles3():
    styles3 = [
        {
            'img' : '/static/assets/img/c-2.png',
            'title' : 'Wall Designs',
            'item' : '450 Items',
            'style' : 'col-xl-6 col-lg-6 col-md-12 col-sm-12',
        },
        {
            'img' : '/static/assets/img/c-5.png',
            'title' : 'Dinning Table',
            'item' : '620 Items',
            'style' : 'col-xl-6 col-lg-6 col-md-12 col-sm-12',
        },
        {
            'img' : '/static/assets/img/c-12.png',
            'title' : 'Room Lighting',
            'item' : '762 Items',
            'style' : 'col-xl-12 col-lg-12 col-md-12 col-sm-12',
        }
    ]
    return {"styles3": styles3}


# slides9 data

def global_slides9():
    slides9 = [
        {
            'img' : '/static/assets/img/banner-22.png',
            'name' : 'Super Sale',
            'title' : 'Quick Delivery',
            'title1' : 'At Your Door',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-21.png',
            'name' : 'Up to 50% Off',
            'title' : 'Free Home',
            'title1' : 'Delivery in 24h',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-23.png',
            'name' : 'New Collections',
            'title' : 'Healthy Food',
            'title1' : 'Delivery your door',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides9": slides9}


# navs2 data

def global_navs2():
    navs2 = [
        {
            'title' : "All",
            'class' : "active",
            'link' : "#all",
            'id' : "all-tab",
            'controls' : "all",
            'selected' : "true",
        },
        {
            'title' : "Vegetables",
            'class' : "",
            'link' : "#mens",
            'id' : "mens-tab",
            'controls' : "mens",
            'selected' : "false",
        },
        {
            'title' : "Meet",
            'class' : "",
            'link' : "#women",
            'id' : "women-tab",
            'controls' : "women",
            'selected' : "false",
        },
        {
            'title' : "Drink",
            'class' : "",
            'link' : "#kids",
            'id' : "kids-tab",
            'controls' : "kids",
            'selected' : "false",
        }
    ]
    return {"navs2": navs2}


# trendings2 data

def global_trendings2():
    trendings2 = [
        {
            'img' : '/static/assets/img/category/c-1.png',
            'title' : 'Fresh Vegetables',
        },
        {
            'img' : '/static/assets/img/category/c-3.png',
            'title' : 'Dairy',
        },
        {
            'img' : '/static/assets/img/category/c-12.png',
            'title' : 'Noodles & Sauces',
        },
        {
            'img' : '/static/assets/img/category/c-4.png',
            'title' : 'Meat & Seafood',
        },
        {
            'img' : '/static/assets/img/category/c-5.png',
            'title' : 'Fruits',
        },
        {
            'img' : '/static/assets/img/category/c-6.png',
            'title' : 'Grocery & Staples',
        },
        {
            'img' : '/static/assets/img/category/c-7.png',
            'title' : 'Snacks',
        },
        {
            'img' : '/static/assets/img/category/c-8.png',
            'title' : 'Pets care',
        },
        {
            'img' : '/static/assets/img/category/c-9.png',
            'title' : 'Electornics',
        },
        {
            'img' : '/static/assets/img/category/c-10.png',
            'title' : 'Home Care',
        },
        {
            'img' : '/static/assets/img/category/c-2.png',
            'title' : 'Eggs',
        },
        {
            'img' : '/static/assets/img/category/c-11.png',
            'title' : 'Dry Snacks',
        }
    ]
    return {"trendings2": trendings2}


# features3 data

def global_features3():
    features3 = [
        {
            'icon' : 'fas fa-shopping-basket grocery-cl',
            'name' : 'Free Shipping',
            'title' : 'Capped at $10 per order',
        },
        {
            'icon' : 'far fa-credit-card grocery-cl',
            'name' : 'Secure Payments',
            'title' : 'Up to 6 months installments',
        },
        {
            'icon' : 'fas fa-shield-alt grocery-cl',
            'name' : '15-Days Returns',
            'title' : 'Shop with fully confidence',
        },
        {
            'icon' : 'fas fa-headphones-alt grocery-cl',
            'name' : '24x7 Fully Support',
            'title' : 'Get friendly support',
        }
    ]
    return {"features3": features3}


# slides10 data

def global_slides10():
    slides10 = [
        {
            'img' : '/static/assets/img/banner-12.png',
            'name' : 'New Collection',
            'title' : 'The Standard',
            'title1' : 'With Smartness',
            'desc' : "Apple 10 comes with 6.5 inches full HD + High Valume",
            'btn' : 'Buy Now',
            'class' : 'text-light fs-sm ft-ragular mb-0',
            'class1' : 'mb-1 ft-bold lg-heading text-light',
            'class2' : 'trending text-light',
            'style' : 'btn btn-white stretched-links',
        },
        {
            'img' : '/static/assets/img/banner-27.png',
            'name' : 'Super Sale',
            'title' : 'The Standard',
            'title1' : 'With Smartness',
            'desc' : "Xiomi Redmi 10 comes with 6.5 inches full HD + LCD Screen",
            'btn' : 'Shop Now',
            'class' : 'text-light fs-sm ft-ragular mb-0',
            'class1' : 'mb-1 ft-bold lg-heading text-light',
            'class2' : 'trending text-light',
            'style' : 'btn btn-white stretched-links',
        },
        {
            'img' : '/static/assets/img/banner-28.png',
            'name' : 'Winter Collection',
            'title' : 'New Winter',
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
            'class' : 'theme-cl fs-sm ft-ragular mb-0',
            'class1' : 'mb-1 ft-bold lg-heading',
            'class2' : 'trending',
            'style' : 'btn stretched-links borders',
        }
    ]
    return {"slides10": slides10}


# features4 data

def global_features4():
    features4 = [
        {
            'icon' : 'fas fa-shopping-basket',
            'name' : 'Free Shipping',
            'title' : 'Capped at $10 per order',
        },
        {
            'icon' : 'far fa-credit-card',
            'name' : 'Secure Payments',
            'title' : 'Up to 6 months installments',
        },
        {
            'icon' : 'fas fa-shield-alt',
            'name' : '15-Days Returns',
            'title' : 'Shop with fully confidence',
        },
        {
            'icon' : 'fas fa-headphones-alt',
            'name' : '24x7 Fully Support',
            'title' : 'Get friendly support',
        }
    ]
    return {"features4": features4}


# categories2 data

def global_categories2():
    categories2 = [
        {
            'img' : '/static/assets/img/headphones.png', 
            'title' : 'Headphones',
        },
        {
            'img' : '/static/assets/img/watch.png', 
            'title' : 'Watches',
        },
        {
            'img' : '/static/assets/img/washing-machine.png', 
            'title' : 'Washing Machine',
        },
        {
            'img' : '/static/assets/img/cell-phone.png', 
            'title' : 'iPhones',
        },
        {
            'img' : '/static/assets/img/safety-goggles.png', 
            'title' : 'Goggles',
        },
        {
            'img' : '/static/assets/img/camera.png', 
            'title' : 'Video Camera',
        },
        {
            'img' : '/static/assets/img/fashion.png', 
            'title' : "Men's Wear",
        },
        {
            'img' : '/static/assets/img/tshirt.png', 
            'title' : "Kid's Wear",
        },
        {
            'img' : '/static/assets/img/accessories.png', 
            'title' : 'Accessories',
        },
        {
            'img' : '/static/assets/img/sneakers.png', 
            'title' : "Men's Shoes",
        },
        {
            'img' : '/static/assets/img/television.png', 
            'title' : 'Television',
        },
        {
            'img' : '/static/assets/img/pant.png', 
            'title' : "Men's Pants",
        }
    ]
    return {"categories2": categories2}


# sellers data

def global_sellers():
    sellers = [
        {
            'id' : 67,
            'img' : '/static/assets/img/shop/11.png', 
            'title' : 'Apple iPhone 11(White)',
            'name' : 'Mobiles',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 18499,
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
            'id' : 66,
            'img' : '/static/assets/img/shop/10.png', 
            'title' : 'boAt Rockerz 425',
            'name' : 'Headphones',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 1199,
        }
    ]
    return {"sellers": sellers}


# featureds data

def global_featureds():
    featureds = [
        {
            'id' : 68,
            'img' : '/static/assets/img/shop/4.png', 
            'title' : 'Apple iPhone 11(Black)',
            'name' : 'iPhones',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 48900,
        },
        {
            'id' : 69,
            'img' : '/static/assets/img/shop/5.png', 
            'title' : 'Canon EOS Digital Camera',
            'name' : 'Camera',
            'tag' : '-50%',
            'style' : 'bg-danger',
            'price' : 33421,
        },
        {
            'id' : 70,
            'img' : '/static/assets/img/shop/6.png', 
            'title' : 'JBL JR310BT Wireless Headphones',
            'name' : 'Headphones',
            'tag' : 'Sold',
            'style' : 'bg-sold',
            'price' : 12239,
        }
    ]
    return {"featureds": featureds}


# recents data

def global_recents():
    recents = [
        {
            'id' : 71,
            'img' : '/static/assets/img/shop/7.png', 
            'title' : 'Sony 139 Cm Smart LED TV',
            'name' : 'TV/LED',
            'tag' : 'New',
            'style' : 'bg-new',
            'price' : 81830,
        },
        {
            'id' : 72,
            'img' : '/static/assets/img/shop/8.png', 
            'title' : 'Sony WH-CH520 Pink Headphones',
            'name' : 'Headphone',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 4490,
        },
        {
            'id' : 65,
            'img' : '/static/assets/img/shop/9.png', 
            'title' : 'iPhone 13 Pro Max',
            'name' : 'Mobiles',
            'tag' : '-50%',
            'style' : 'bg-danger',
            'price' : 39999,
        }
    ]
    return {"recents": recents}


# brands data

def global_brands():
    brands = [
        {
            'img' : '/static/assets/img/shop-logo-1.png', 
        },
        {
            'img' : '/static/assets/img/shop-logo-2.png', 
        },
        {
            'img' : '/static/assets/img/shop-logo-3.png', 
        },
        {
            'img' : '/static/assets/img/shop-logo-4.png', 
        },
        {
            'img' : '/static/assets/img/shop-logo-5.png', 
        },
        {
            'img' : '/static/assets/img/shop-logo-6.png', 
        },
        {
            'img' : '/static/assets/img/shop-logo-1.png', 
        },
        {
            'img' : '/static/assets/img/shop-logo-2.png', 
        }
    ]
    return {"brands": brands}


# slides11 data

def global_slides11():
    slides11 = [
        {
            'img' : '/static/assets/img/light-banner-1.png',
            'name' : 'New Collection',
            'title' : 'The Standard',
            'title1' : 'With',
            'title2' : 'Smartness',
            'color' : 'theme-cl',
            'desc' : 'Apple 10 comes with 6.5 inches full HD + High Valume',
            'btn' : 'Buy Now',
            'style' : 'btn btn-white stretched-links hover-black',
        },
        {
            'img' : '/static/assets/img/light-banner-2.png',
            'name' : 'Super Sale',
            'title' : 'The Standard',
            'title1' : 'With',
            'title2' : 'Smartness',
            'color' : 'text-success',
            'desc' : 'Xiomi Redmi 10 comes with 6.5 inches full HD + LCD Screen',
            'btn' : 'Shop Now',
            'style' : 'btn btn-white stretched-links hover-black',
        },
        {
            'img' : '/static/assets/img/light-banner-3.png',
            'name' : 'Super Sale',
            'title' : 'The Standard',
            'title1' : 'With',
            'title2' : 'Smartness',
            'color' : '',
            'desc' : 'Xiomi Redmi 10 comes with 6.5 inches full HD + LCD Screen',
            'btn' : 'Shop Now',
            'style' : 'btn theme-bg text-light',
        }
    ]
    return {"slides11": slides11}


# slides12 data

def global_slides12():
    slides12 = [
        {
            'img' : '/static/assets/img/banner-29.png',
            'name' : 'Watch Collection',
            'title' : 'New Sale',
            'title1' : 'Watch Collections',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-30.png',
            'name' : '50% Off Sale',
            'title' : 'Modern Style',
            'title1' : 'Watch Collections',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-24.png',
            'name' : 'Winter Collection',
            'title' : 'New Winter',
            'title1' : 'Collections 2025',
            'desc' : "There's nothing like trend",
            'btn' : 'Shop Now',
        }
    ]
    return {"slides12": slides12}


# slides13 data

def global_slides13():
    slides13 = [
        {
            'img' : '/static/assets/img/banner-3.png',
            'name' : 'New Collection',
            'title' : 'The Standard',
            'title1' : 'With',
            'title2' : 'Smartness',
            'style' : 'theme-cl',
            'desc' : 'Apple 10 comes with 6.5 inches full HD + High Valume',
            'btn' : 'Buy Now',
        },
        {
            'img' : '/static/assets/img/banner-24.png',
            'name' : 'Super Sale',
            'title' : 'The Standard',
            'title1' : 'With',
            'title2' : 'Smartness',
            'style' : 'theme-cl',
            'desc' : 'Xiomi Redmi 10 comes with 6.5 inches full HD + LCD Screen',
            'btn' : 'Shop Now',
        },
        {
            'img' : '/static/assets/img/banner-25.png',
            'name' : 'Super Sale',
            'title' : 'The Standard',
            'title1' : 'With',
            'title2' : 'Smartness',
            'style' : '',
            'desc' : 'Xiomi Redmi 10 comes with 6.5 inches full HD + LCD Screen',
            'btn' : 'Shop Now',
        }
    ]
    return {"slides13": slides13}


# orders data

def global_orders():
    orders = [
        {
            'img' : '/static/assets/img/product/4.jpg',
            'name' : 'Dresses',
            'title' : 'Women Striped Shirt Dress',
            'size' : 'Size: 36',
            'color' : 'Color: Red',
            'price' : 140,
            'status' : 'In Progress',
            'style' : 'text-warning bg-light-warning',
            'date' : '22 September 2025',
        },
        {
            'img' : '/static/assets/img/product/8.jpg',
            'name' : 'Boys',
            'title' : 'Boys Solid Sweatshirt',
            'size' : 'Size: 36',
            'color' : 'Color: Red',
            'price' : 130,
            'status' : 'Completed',
            'style' : 'text-success bg-light-success',
            'date' : '31 May 2025',
        },
        {
            'img' : '/static/assets/img/product/7.jpg',
            'name' : "Men's",
            'title' : 'Printed Straight Kurta',
            'size' : 'Size: 36',
            'color' : 'Color: Red',
            'price' : 130,
            'status' : 'On Hold',
            'style' : 'text-danger bg-light-danger',
            'date' : '22 September 2025',
        }
    ]
    return {"orders": orders}


# orders2 data

def global_orders2():
    orders2 = [
        {
            'img' : '/static/assets/img/product/2.jpg',
            'name' : 'Dresses',
            'title' : 'Women Striped Shirt Dress',
            'size' : 'Size: 36',
            'color' : 'Color: Red',
            'price' : 130,
            'status' : 'Completed',
            'style' : 'text-warning bg-light-warning',
            'date' : '22 May 2025',
        },
        {
            'img' : '/static/assets/img/product/8.jpg',
            'name' : 'Boys',
            'title' : 'Boys Solid Sweatshirt',
            'size' : 'Size: 36',
            'color' : 'Color: Red',
            'price' : 140,
            'status' : 'Completed',
            'style' : 'text-success bg-light-success',
            'date' : '31 May 2025',
        },
        {
            'img' : '/static/assets/img/product/1.jpg',
            'name' : "Men's",
            'title' : 'Printed Straight Kurta',
            'size' : 'Size: 36',
            'color' : 'Color: Red',
            'price' : 230,
            'status' : 'Canceled',
            'style' : 'text-danger bg-light-danger',
            'date' : '22 September 2025',
        }
    ]
    return {"orders2": orders2}


# products5 data

def global_products5():
    products5 = [
        {
            'id' : 19,
            'img' : '/static/assets/img/product/12.jpg', 
            'title' : 'Women White T-shirt',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'price' : 600,
            'original_price' : None,
            'class' : 'fw-medium fs-md text-dark',
        },
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg', 
            'title' : 'Boys yellow-green T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 199,
            'original_price' : 220,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 17,
            'img' : '/static/assets/img/product/10.jpg', 
            'title' : 'Boys White T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 149,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 15,
            'img' : '/static/assets/img/product/9.jpg', 
            'title' : 'Girls Fit and Flare Dress',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 99,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        }
    ]
    return {"products5": products5}


# products6 data

def global_products6():
    products6 = [
        {
            'id' : 5,
            'img' : '/static/assets/img/product/5.jpg',
            'img1' : '/static/assets/img/product/5-a.jpg',
            'title' : 'Flix Flox Jeans',
            'tag' : 'Sold',
            'style' : 'bg-sold',
            'price' : 110,
            'original_price' : 150,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg',
            'img1' : '/static/assets/img/product/11-a.jpg',
            'title' : 'Boys yellow-green T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 199,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 2,
            'img' : '/static/assets/img/product/2.jpg',
            'img1' : '/static/assets/img/product/2-a.jpg',
            'title' : 'Formal Men Lowers',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'price' : 79,
            'original_price' : 129,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 1,
            'img' : '/static/assets/img/product/1.jpg',
            'img1' : '/static/assets/img/product/1-a.jpg',
            'title' : 'Half Running Set',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 119,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        }
    ]
    return {"products6": products6}


# shops data

def global_shops():
    shops = [
        {
            'img' : '/static/assets/img/fashion.png',
            'title' : "Men's Wear",
        },
        {
            'img' : '/static/assets/img/tshirt.png',
            'title' : "Kid's Wear",
        },
        {
            'img' : '/static/assets/img/accessories.png',
            'title' : "Accessories",
        },
        {
            'img' : '/static/assets/img/sneakers.png',
            'title' : "Men's Shoes",
        }
    ]
    return {"shops": shops}


# products7 data

def global_products7():
    products7 = [
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg', 
            'title' : 'Boys yellow-green T-shirt',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : '99 - $129',
            'name' : 'color9',
            'id1' : 'white9',
            'id2' : 'blue9',
            'id3' : 'yellow9',
            'id4' : 'pink9',
            'check' : '',
        },
        {
            'id' : 19,
            'img' : '/static/assets/img/product/12.jpg', 
            'title' : 'Women White T-shirt',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'price' : '99 - $129',
            'name' : 'color10',
            'id1' : 'white10',
            'id2' : 'blue10',
            'id3' : 'yellow10',
            'id4' : 'pink10',
            'check' : '',
        },
        {
            'id' : 20,
            'img' : '/static/assets/img/product/13.jpg', 
            'title' : 'Boys Shorts',
            'tag' : False,
            'style' : '',
            'price' : '99 - $129',
            'name' : 'color11',
            'id1' : 'white11',
            'id2' : 'blue11',
            'id3' : 'yellow11',
            'id4' : 'pink11',
            'check' : '',
        },
        {
            'id' : 21,
            'img' : '/static/assets/img/product/14.jpg', 
            'title' : 'Boys yellow T-shirt',
            'tag' : 'New',
            'style' : 'bg-new',
            'price' : '99 - $129',
            'name' : 'color12',
            'id1' : 'white12',
            'id2' : 'blue12',
            'id3' : 'yellow12',
            'id4' : 'pink12',
            'check' : '',
        }
    ]
    return {"products7": products7}


# products8 data

def global_products8():
    products8 = [
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg', 
            'title' : 'Boys yellow-green T-shirt',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : '99 - $129',
            'name' : 'color9',
            'id1' : 'white9',
            'id2' : 'blue9',
            'id3' : 'yellow9',
            'id4' : 'pink9',
            'check' : '',
        },
        {
            'id' : 19,
            'img' : '/static/assets/img/product/12.jpg', 
            'title' : 'Women White T-shirt',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'price' : '99 - $129',
            'name' : 'color10',
            'id1' : 'white10',
            'id2' : 'blue10',
            'id3' : 'yellow10',
            'id4' : 'pink10',
            'check' : '',
        },
        {
            'id' : 20,
            'img' : '/static/assets/img/product/13.jpg', 
            'title' : 'Boys Shorts',
            'tag' : False,
            'style' : '',
            'price' : '99 - $129',
            'name' : 'color11',
            'id1' : 'white11',
            'id2' : 'blue11',
            'id3' : 'yellow11',
            'id4' : 'pink11',
            'check' : '',
        },
        {
            'id' : 21,
            'img' : '/static/assets/img/product/14.jpg', 
            'title' : 'Boys yellow T-shirt',
            'tag' : 'New',
            'style' : 'bg-new',
            'price' : '99 - $129',
            'name' : 'color12',
            'id1' : 'white12',
            'id2' : 'blue12',
            'id3' : 'yellow12',
            'id4' : 'pink12',
            'check' : '',
        },
        {
            'id' : 4,
            'img' : '/static/assets/img/product/4.jpg', 
            'title' : 'Half Fancy Lady Dress',
            'tag' : 'Hot',
            'style' : 'bg-warning',
            'price' : '99 - $129',
            'name' : 'color4',
            'id1' : 'white4',
            'id2' : 'blue4',
            'id3' : 'yellow4',
            'id4' : 'pink4',
            'check' : '',
        },
        {
            'id' : 5,
            'img' : '/static/assets/img/product/5.jpg', 
            'title' : 'Flix Flox Jeans',
            'tag' : False,
            'style' : '',
            'price' : '99 - $129',
            'name' : 'color5',
            'id1' : 'white5',
            'id2' : 'blue5',
            'id3' : 'yellow5',
            'id4' : 'pink5',
            'check' : '',
        },
        {
            'id' : 6,
            'img' : '/static/assets/img/product/6.jpg', 
            'title' : 'Fancy Salwar Suits',
            'tag' : 'Hot',
            'style' : 'bg-danger',
            'price' : '99 - $129',
            'name' : 'color6',
            'id1' : 'white6',
            'id2' : 'blue6',
            'id3' : 'yellow6',
            'id4' : 'pink6',
            'check' : '',
        },
        {
            'id' : 7,
            'img' : '/static/assets/img/product/7.jpg', 
            'title' : 'Collot Full Dress',
            'tag' : 'Sale',
            'style' : 'bg-success',
            'price' : '99 - $129',
            'name' : 'color7',
            'id1' : 'white7',
            'id2' : 'blue7',
            'id3' : 'yellow7',
            'id4' : 'pink7',
            'check' : '',
        },
        {
            'id' : 8,
            'img' : '/static/assets/img/product/8.jpg', 
            'title' : 'Formal Fluex Kurti',
            'tag' : 'Sale',
            'style' : 'bg-success',
            'price' : '99 - $129',
            'name' : 'color88',
            'id1' : 'white88',
            'id2' : 'blue88',
            'id3' : 'yellow88',
            'id4' : 'pink88',
            'check' : '',
        }
    ]
    return {"products8": products8}


# images data

def global_images():
    images = [
        {
            'img' : '/static/assets/img/product/17.png', 
        },
        {
            'img' : '/static/assets/img/product/18.png', 
        },
        {
            'img' : '/static/assets/img/product/19.png', 
        },
        {
            'img' : '/static/assets/img/product/20.png', 
        },
        {
            'img' : '/static/assets/img/product/21.png', 
        }
    ]
    return {"images": images}


# informations data

def global_informations():
    informations = [
        {
            'name' : 'ID', 
            'title' : '#1253458', 
        },
        {
            'name' : 'SKU', 
            'title' : 'KUM125896', 
        },
        {
            'name' : 'Color', 
            'title' : 'Sky Blue', 
        },
        {
            'name' : 'Size', 
            'title' : 'Xl, 42', 
        },
        {
            'name' : 'Weight', 
            'title' : '450 Gr', 
        }
    ]
    return {"informations": informations}


# reviews2 data

def global_reviews2():
    reviews2 = [
        {
            'img' : '/static/assets/img/team-1.jpg',
            'name' : 'Daniel Rajdesh', 
            'date' : '30 jul 2025', 
            'desc' : 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum',
            'style' : 'single_rev d-flex align-items-start br-bottom py-3',
        },
        {
            'img' : '/static/assets/img/team-2.jpg',
            'name' : 'Seema Gupta', 
            'date' : '30 Aug 2025', 
            'desc' : 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum',
            'style' : 'single_rev d-flex align-items-start br-bottom py-3',
        },
        {
            'img' : '/static/assets/img/team-3.jpg',
            'name' : 'Mark Jugermi', 
            'date' : '10 Oct 2025', 
            'desc' : 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum',
            'style' : 'single_rev d-flex align-items-start br-bottom py-3',
        },
        {
            'img' : '/static/assets/img/team-4.jpg',
            'name' : 'Meena Rajpoot', 
            'date' : '17 Dec 2025', 
            'desc' : 'At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum',
            'style' : 'single_rev d-flex align-items-start py-3',
        }
    ]
    return {"reviews2": reviews2}


# images2 data

def global_images2():
    images2 = [
        {
            'img' : '/static/assets/img/product/16.png', 
        },
        {
            'img' : '/static/assets/img/product/17.png', 
        },
        {
            'img' : '/static/assets/img/product/18.png', 
        },
        {
            'img' : '/static/assets/img/product/19.png', 
        },
        {
            'img' : '/static/assets/img/product/20.png', 
        },
        {
            'img' : '/static/assets/img/product/21.png', 
        }
    ]
    return {"images2": images2}


# colors data

def global_colors():
    colors = [
        {
            'id' : 'white8', 
            'blc' : 'blc7', 
        },
        {
            'id' : 'blue8', 
            'blc' : 'blc2', 
        },
        {
            'id' : 'yellow8', 
            'blc' : 'blc5', 
        },
        {
            'id' : 'pink8', 
            'blc' : 'blc3', 
        },
        {
            'id' : 'red', 
            'blc' : 'blc4', 
        },
        {
            'id' : 'green', 
            'blc' : 'blc6', 
        }
    ]
    return {"colors": colors}


# sizes data

def global_sizes():
    sizes = [
        {
            'id' : '28', 
            'check' : 'checked', 
        },
        {
            'id' : '30', 
            'check' : '', 
        },
        {
            'id' : '32', 
            'check' : '', 
        },
        {
            'id' : '34', 
            'check' : '', 
        },
        {
            'id' : '36', 
            'check' : '', 
        },
        {
            'id' : '38', 
            'check' : '', 
        },
        {
            'id' : '40', 
            'check' : '', 
        },
        {
            'id' : '42', 
            'check' : '', 
        },
        {
            'id' : '44', 
            'check' : '', 
        },
        {
            'id' : '46', 
            'check' : '', 
        },
        {
            'id' : '48', 
            'check' : '', 
        },
        {
            'id' : '50', 
            'check' : '', 
        }
    ]
    return {"sizes": sizes}


# images3 data

def global_images3():
    images3 = [
        {
            'img' : '/static/assets/img/product/4.jpg', 
        },
        {
            'img' : '/static/assets/img/product/6-a.jpg', 
        },
        {
            'img' : '/static/assets/img/product/7.jpg', 
        },
        {
            'img' : '/static/assets/img/product/7-a.jpg', 
        }
    ]
    return {"images3": images3}


# images4 data

def global_images4():
    images4 = [
        {
            'img' : '/static/assets/img/product/4.jpg', 
        },
        {
            'img' : '/static/assets/img/product/6-a.jpg', 
        },
        {
            'img' : '/static/assets/img/product/7.jpg', 
        },
        {
            'img' : '/static/assets/img/product/7-a.jpg', 
        }
    ]
    return {"images4": images4}


# categories3 data

def global_categories3():
    categories3 = [
        {
            'name' : 'Lifestyle',
            'number' : '09',
        },
        {
            'name' : 'Travel',
            'number' : '12',
        },
        {
            'name' : 'Fashion',
            'number' : '19',
        },
        {
            'name' : 'Branding',
            'number' : '17',
        },
        {
            'name' : 'Music',
            'number' : '10',
        }
    ]
    return {"categories3": categories3}


# posts data

def global_posts():
    posts = [
        {
            'img' : '/static/assets/img/bl-1.png',
            'title' : 'Alonso Kelina Falao Asiano Pero',
            'time' : '10 Min ago',
        },
        {
            'img' : '/static/assets/img/bl-2.png',
            'title' : 'It is a long established fact that a reader',
            'time' : '2 Hours ago',
        },
        {
            'img' : '/static/assets/img/bl-3.png',
            'title' : 'Many desktop publish packages and web',
            'time' : '4 Hours ago',
        },
        {
            'img' : '/static/assets/img/bl-1.png',
            'title' : 'Various versions have evolved over the years',
            'time' : '7 Hours ago',
        },
        {
            'img' : '/static/assets/img/bl-2.png',
            'title' : 'Photo booth anim 8-bit PBR 3 wolf moon.',
            'time' : '3 Days ago',
        }
    ]
    return {"posts": posts}


# links data

def global_links():
    links = [
        {
            'title' : 'Alert',
            'class' : 'active',
            'id' : 'v-alert-tab',
            'link' : '#v-alert',
            'controls' : 'v-alert',
            'selected' : 'true',
        },
        {
            'title' : 'Avaters',
            'class' : '',
            'id' : 'v-avaters-tab',
            'link' : '#v-avaters',
            'controls' : 'v-avaters',
            'selected' : 'false',
        },
        {
            'title' : 'Badges',
            'class' : '',
            'id' : 'v-badges-tab',
            'link' : '#v-badges',
            'controls' : 'v-badges',
            'selected' : 'false',
        },
        {
            'title' : 'Breadcrumb',
            'class' : '',
            'id' : 'v-breadcrumb-tab',
            'link' : '#v-breadcrumb',
            'controls' : 'v-breadcrumb',
            'selected' : 'false',
        },
        {
            'title' : 'Buttons',
            'class' : '',
            'id' : 'v-buttons-tab',
            'link' : '#v-buttons',
            'controls' : 'v-buttons',
            'selected' : 'false',
        },
        {
            'title' : 'Form',
            'class' : '',
            'id' : 'v-form-tab',
            'link' : '#v-form',
            'controls' : 'v-form',
            'selected' : 'false',
        },
        {
            'title' : 'Lists',
            'class' : '',
            'id' : 'v-lists-tab',
            'link' : '#v-lists',
            'controls' : 'v-lists',
            'selected' : 'false',
        },
        {
            'title' : 'Tabs',
            'class' : '',
            'id' : 'v-tabss-tab',
            'link' : '#v-tabss',
            'controls' : 'v-tabss',
            'selected' : 'false',
        },
        {
            'title' : 'Accordion',
            'class' : '',
            'id' : 'v-accordions-tab',
            'link' : '#v-accordions',
            'controls' : 'v-accordions',
            'selected' : 'false',
        },
        {
            'title' : 'Pagination',
            'class' : '',
            'id' : 'v-pagination-tab',
            'link' : '#v-pagination',
            'controls' : 'v-pagination',
            'selected' : 'false',
        },
        {
            'title' : 'Typography',
            'class' : '',
            'id' : 'v-typography-tab',
            'link' : '#v-typography',
            'controls' : 'v-typography',
            'selected' : 'false',
        },
        {
            'title' : 'Progressbar',
            'class' : '',
            'id' : 'v-progressbar-tab',
            'link' : '#v-progressbar',
            'controls' : 'v-progressbar',
            'selected' : 'false',
        },
        {
            'title' : 'Utility',
            'class' : '',
            'id' : 'v-utility-tab',
            'link' : '#v-utility',
            'controls' : 'v-utility',
            'selected' : 'false',
        }
    ]
    return {"links": links}


# alerts data

def global_alerts():
    alerts = [
        {
            'title' : 'This is a primary alert—check it out!',
            'class' : 'primary',
        },
        {
            'title' : 'This is a secondary alert—check it out!',
            'class' : 'secondary',
        },
        {
            'title' : 'This is a success alert—check it out!',
            'class' : 'success',
        },
        {
            'title' : 'This is a danger alert—check it out!',
            'class' : 'danger',
        },
        {
            'title' : 'This is a info alert—check it out!',
            'class' : 'info',
        },
        {
            'title' : 'This is a light alert—check it out!',
            'class' : 'light',
        },
        {
            'title' : 'This is a dark alert—check it out!',
            'class' : 'dark',
        }
    ]
    return {"alerts": alerts}


# avatars data

def global_avatars():
    avatars = [
        {
            'class' : 'avatar avatar-xxl',
        },
        {
            'class' : 'avatar avatar-xl',
        },
        {
            'class' : 'avatar avatar-lg',
        },
        {
            'class' : 'avatar',
        },
        {
            'class' : 'avatar avatar-sm',
        },
        {
            'class' : 'avatar avatar-xs',
        }
    ]
    return {"avatars": avatars}


# badges data

def global_badges():
    badges = [
        {
            'title' : 'Primary',
            'class' : 'primary',
        },
        {
            'title' : 'Secondary',
            'class' : 'secondary',
        },
        {
            'title' : 'Success',
            'class' : 'success',
        },
        {
            'title' : 'Danger',
            'class' : 'danger',
        },
        {
            'title' : 'Warning',
            'class' : 'warning',
        },
        {
            'title' : 'Info',
            'class' : 'info',
        },
        {
            'title' : 'Light',
            'class' : 'light',
        },
        {
            'title' : 'Dark',
            'class' : 'dark',
        }
    ]
    return {"badges": badges}


# badges2 data

def global_badges2():
    badges2 = [
        {
            'title' : 'Primary',
            'class' : 'primary one',
        },
        {
            'title' : 'Secondary',
            'class' : 'secondary two',
        },
        {
            'title' : 'Success',
            'class' : 'success three',
        },
        {
            'title' : 'Danger',
            'class' : 'danger four',
        },
        {
            'title' : 'Warning',
            'class' : 'warning five',
        },
        {
            'title' : 'Info',
            'class' : 'info six',
        },
        {
            'title' : 'Light',
            'class' : 'light seven',
        },
        {
            'title' : 'Dark',
            'class' : 'dark eight',
        }
    ]
    return {"badges2": badges2}


# buttons data

def global_buttons():
    buttons = [
        {
            'title' : 'Primary',
            'class' : 'primary',
        },
        {
            'title' : 'Secondary',
            'class' : 'secondary',
        },
        {
            'title' : 'Success',
            'class' : 'success',
        },
        {
            'title' : 'Danger',
            'class' : 'danger',
        },
        {
            'title' : 'Warning',
            'class' : 'warning',
        },
        {
            'title' : 'Info',
            'class' : 'info',
        },
        {
            'title' : 'Light',
            'class' : 'light',
        },
        {
            'title' : 'Dark',
            'class' : 'dark',
        }
    ]
    return {"buttons": buttons}


# progressbars data

def global_progressbars():
    progressbars = [
        {
            'style' : 'progress mb-3',
            'class' : 'dark',
            'width' : '12%',
            'valuenow' : '12',
        },
        {
            'style' : 'progress mb-3',
            'class' : 'success',
            'width' : '25%',
            'valuenow' : '25',
        },
        {
            'style' : 'progress mb-3',
            'class' : 'info',
            'width' : '50%',
            'valuenow' : '50',
        },
        {
            'style' : 'progress mb-3',
            'class' : 'warning',
            'width' : '75%',
            'valuenow' : '75',
        },
        {
            'style' : 'progress',
            'class' : 'danger',
            'width' : '100%',
            'valuenow' : '100',
        }
    ]
    return {"progressbars": progressbars}


# products9 data

def global_products9():
    products9 = [
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
            'id' : 17,
            'img' : '/static/assets/img/product/10.jpg',
            'img1' : '/static/assets/img/product/10-a.jpg',
            'title' : 'Boys White T-shirt',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 110,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg',
            'img1' : '/static/assets/img/product/11-a.jpg',
            'title' : 'Boys yellow-green T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 49,
            'original_price' : 90,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 19,
            'img' : '/static/assets/img/product/12.jpg',
            'img1' : '/static/assets/img/product/12-a.jpg',
            'title' : 'Women White T-shirt',
            'tag' : 'Hot',
            'style' : 'bg-hot',
            'price' : 114,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 20,
            'img' : '/static/assets/img/product/13.jpg',
            'img1' : '/static/assets/img/product/13-a.jpg',
            'title' : 'Boys Shorts',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 120,
            'original_price' : None,
            'class' : 'ft-medium theme-cl fs-md text-dark',
        },
        {
            'id' : 21,
            'img' : '/static/assets/img/product/14.jpg',
            'img1' : '/static/assets/img/product/14-a.jpg',
            'title' : 'Boys yellow T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 129,
            'original_price' : 149,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 5,
            'img' : '/static/assets/img/product/5.jpg',
            'img1' : '/static/assets/img/product/5-a.jpg',
            'title' : 'Flix Flox Jeans',
            'tag' : 'Sold',
            'style' : 'bg-sold',
            'price' : 110,
            'original_price' : 150,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 18,
            'img' : '/static/assets/img/product/11.jpg',
            'img1' : '/static/assets/img/product/11-a.jpg',
            'title' : 'Boys yellow-green T-shirt',
            'tag' : False,
            'style' : '',
            'price' : 199,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        },
        {
            'id' : 2,
            'img' : '/static/assets/img/product/2.jpg',
            'img1' : '/static/assets/img/product/2-a.jpg',
            'title' : 'Formal Men Lowers',
            'tag' : 'Sold Out',
            'style' : 'bg-sold',
            'price' : 79,
            'original_price' : 129,
            'class' : 'ft-medium theme-cl fs-md',
        },
        {
            'id' : 1,
            'img' : '/static/assets/img/product/1.jpg',
            'img1' : '/static/assets/img/product/1-a.jpg',
            'title' : 'Half Running Set',
            'tag' : 'Sale',
            'style' : 'bg-sale',
            'price' : 119,
            'original_price' : None,
            'class' : 'ft-medium fs-md text-dark',
        }
    ]
    return {"products9": products9}