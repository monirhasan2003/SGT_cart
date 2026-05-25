"""Phase 15 (Chunk B v3b) smoke test — vendor delivery / cancel ranking.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase15b_ranking.py
"""
import os
import sys
from datetime import datetime, timedelta
from decimal import Decimal

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User, Address
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.cart import CartItem
from app.models.order import (
    Order, SubOrder, SubOrderEvent,
    SUBORDER_DELIVERED, SUBORDER_CANCELLED,
)
from app.models.marketing import RewardLedger
from app.models.analytics import ProductView
from app.models.notification import Notification
from app.services.vendor_stats_service import recompute_vendor_stats, recompute_all
from app.services.search_service import apply_ranking
from app.services.order_service import place_order, update_suborder_status

CUSTOMER = "smoke_p15b3b_customer@example.com"
SELLER_A = "smoke_p15b3b_seller_a@example.com"
SELLER_B = "smoke_p15b3b_seller_b@example.com"
CAT_SLUG = "smoke-p15b3b-cat"
PASSWORD = "test1234"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for email in (CUSTOMER, SELLER_A, SELLER_B):
            u = User.query.filter_by(email=email).first()
            if not u:
                continue
            RewardLedger.query.filter_by(user_id=u.id).delete()
            for o in Order.query.filter_by(customer_id=u.id).all():
                db.session.delete(o)
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                # also delete any orphan sub_orders directly referencing vp
                for s in SubOrder.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(s)
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    ProductView.query.filter_by(product_id=p.id).delete()
                    db.session.delete(p)
        db.session.flush()
        for email in (CUSTOMER, SELLER_A, SELLER_B):
            u = User.query.filter_by(email=email).first()
            if u:
                db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()


def seed(app):
    with app.app_context():
        cat = Category(name_en="P15 v3b Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        customer = User(name="P15 Customer", email=CUSTOMER, role="customer",
                        is_active=True)
        customer.set_password(PASSWORD)
        sa = User(name="P15 Seller A", email=SELLER_A, role="seller", is_active=True)
        sa.set_password(PASSWORD)
        sb = User(name="P15 Seller B", email=SELLER_B, role="seller", is_active=True)
        sb.set_password(PASSWORD)
        db.session.add_all([customer, sa, sb])
        db.session.flush()
        db.session.add(Address(user_id=customer.id, full_name="P15 Customer",
                               phone="0170", address_line="x", city="Dhaka",
                               is_default=True))
        # Both vendors start with identical seller rating to isolate the
        # delivery / cancel signals as the differentiator.
        vp_a = VendorProfile(user_id=sa.id, shop_name_en="P15 Fast Shop",
                             slug="p15-fast-shop", status=VENDOR_APPROVED,
                             commission_rate=10,
                             rating_avg=Decimal("4.00"), rating_count=5)
        vp_b = VendorProfile(user_id=sb.id, shop_name_en="P15 Slow Shop",
                             slug="p15-slow-shop", status=VENDOR_APPROVED,
                             commission_rate=10,
                             rating_avg=Decimal("4.00"), rating_count=5)
        db.session.add_all([vp_a, vp_b])
        db.session.flush()
        prod_a = Product(vendor_id=vp_a.id, category_id=cat.id,
                         title_en="P15 v3b Product A", slug="p15-v3b-product-a",
                         base_price=100, stock=99, status=PRODUCT_PUBLISHED)
        prod_b = Product(vendor_id=vp_b.id, category_id=cat.id,
                         title_en="P15 v3b Product B", slug="p15-v3b-product-b",
                         base_price=100, stock=99, status=PRODUCT_PUBLISHED)
        db.session.add_all([prod_a, prod_b])
        db.session.commit()
        return {
            "customer_id": customer.id,
            "vendor_a": vp_a.id, "vendor_b": vp_b.id,
            "prod_a": prod_a.id, "prod_b": prod_b.id,
        }


def _history(vendor_id, customer_id, delivered_count, delivery_days,
             cancelled_count=0):
    """Forge sub-order history with known timing."""
    now = datetime.utcnow()
    for i in range(delivered_count):
        order = Order(customer_id=customer_id, order_number=f"P15B-{vendor_id}-D-{i}",
                      payment_method="cod", payment_status="pending",
                      ship_name="x", ship_phone="x", ship_address_line="x",
                      ship_city="x", subtotal=100, total_amount=100)
        db.session.add(order)
        db.session.flush()
        created = now - timedelta(days=delivery_days + i)
        sub = SubOrder(order_id=order.id, vendor_id=vendor_id, subtotal=100,
                       status=SUBORDER_DELIVERED)
        sub.created_at = created
        db.session.add(sub)
        db.session.flush()
        ev = SubOrderEvent(sub_order_id=sub.id, status=SUBORDER_DELIVERED)
        ev.created_at = created + timedelta(days=delivery_days)
        db.session.add(ev)
    for i in range(cancelled_count):
        order = Order(customer_id=customer_id, order_number=f"P15B-{vendor_id}-C-{i}",
                      payment_method="cod", payment_status="pending",
                      ship_name="x", ship_phone="x", ship_address_line="x",
                      ship_city="x", subtotal=100, total_amount=100)
        db.session.add(order)
        db.session.flush()
        db.session.add(SubOrder(order_id=order.id, vendor_id=vendor_id,
                                subtotal=100, status=SUBORDER_CANCELLED))
    db.session.commit()


def main():
    app = create_app("development")
    purge(app)
    ids = seed(app)

    # ====================================================================
    # forge history: A fast (1 day, no cancels), B slow (5 days, 1 cancel of 4)
    # ====================================================================
    with app.app_context():
        _history(ids["vendor_a"], ids["customer_id"],
                 delivered_count=3, delivery_days=1)
        _history(ids["vendor_b"], ids["customer_id"],
                 delivered_count=3, delivery_days=5, cancelled_count=1)

    # ====================================================================
    # recompute_vendor_stats
    # ====================================================================
    with app.app_context():
        vp_a = db.session.get(VendorProfile, ids["vendor_a"])
        vp_b = db.session.get(VendorProfile, ids["vendor_b"])
        recompute_vendor_stats(vp_a)
        recompute_vendor_stats(vp_b)
        db.session.commit()

        vp_a = db.session.get(VendorProfile, ids["vendor_a"])
        vp_b = db.session.get(VendorProfile, ids["vendor_b"])
        check("fast vendor avg_delivery_days ~ 1",
              abs(float(vp_a.avg_delivery_days) - 1.0) < 0.05,
              f"got {vp_a.avg_delivery_days}")
        check("fast vendor cancel_rate = 0",
              float(vp_a.cancel_rate) == 0.0)
        check("slow vendor avg_delivery_days ~ 5",
              abs(float(vp_b.avg_delivery_days) - 5.0) < 0.05,
              f"got {vp_b.avg_delivery_days}")
        check("slow vendor cancel_rate = 0.25 (1 of 4)",
              abs(float(vp_b.cancel_rate) - 0.25) < 0.001,
              f"got {vp_b.cancel_rate}")

    # ====================================================================
    # apply_ranking — fast vendor's product comes first despite equal rating
    # ====================================================================
    with app.app_context():
        q = Product.query.filter(
            Product.id.in_([ids["prod_a"], ids["prod_b"]]),
            Product.status == PRODUCT_PUBLISHED,
        )
        ranked = apply_ranking(q).all()
        check("ranking surfaces fast / low-cancel vendor first",
              ranked and ranked[0].id == ids["prod_a"],
              detail=str([p.slug for p in ranked]))

    # ====================================================================
    # recompute_all CLI helper updates every vendor
    # ====================================================================
    with app.app_context():
        n = recompute_all()
        check("recompute_all touches at least the 2 test vendors",
              n >= 2)

    # ====================================================================
    # hook: update_suborder_status auto-refreshes vendor stats
    # ====================================================================
    with app.app_context():
        # Zero out vendor A stats, place + deliver a fresh order, expect refresh.
        vp_a = db.session.get(VendorProfile, ids["vendor_a"])
        vp_a.avg_delivery_days = Decimal("0")
        db.session.commit()
        customer = db.session.get(User, ids["customer_id"])
        address = Address.query.filter_by(user_id=customer.id).first()
        db.session.add(CartItem(user_id=customer.id, product_id=ids["prod_a"],
                                quantity=1))
        db.session.commit()
        order = place_order(customer, address, "cod")
        sub = order.suborders[0]
        update_suborder_status(sub, SUBORDER_DELIVERED)
        db.session.commit()
        vp_a = db.session.get(VendorProfile, ids["vendor_a"])
        check("update_suborder_status refreshes vendor stats",
              float(vp_a.avg_delivery_days) > 0)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 15 Chunk B v3b ranking smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
