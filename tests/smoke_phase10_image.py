"""Phase 10 (Chunk C) smoke test — CLIP image search.

First run will download the `clip-ViT-B-32` weights (~600 MB) the first time
the model is loaded; later runs are fast.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase10_image.py
"""
import io
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.vendor import VendorProfile, VENDOR_APPROVED
from app.models.catalog import Category, Product, PRODUCT_PUBLISHED
from app.models.embedding import ProductEmbedding
from app.services import image_search_service

SELLER = "smoke_p10c_seller@example.com"
PASSWORD = "test1234"
CAT_SLUG = "smoke-p10c-cat"
RED_FILE = "uploads/p10c_red.png"
BLUE_FILE = "uploads/p10c_blue.png"
results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def make_image(static_dir, rel_path, color, size=(256, 256)):
    from PIL import Image
    full = os.path.join(static_dir, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    Image.new("RGB", size, color).save(full)
    return full


def png_bytes(color, size=(256, 256)):
    from PIL import Image
    buf = io.BytesIO()
    Image.new("RGB", size, color).save(buf, format="PNG")
    return buf.getvalue()


def purge(app):
    with app.app_context():
        u = User.query.filter_by(email=SELLER).first()
        if u:
            vp = VendorProfile.query.filter_by(user_id=u.id).first()
            if vp:
                for p in Product.query.filter_by(vendor_id=vp.id).all():
                    db.session.delete(p)   # cascades the embedding row
            db.session.delete(u)
        cat = Category.query.filter_by(slug=CAT_SLUG).first()
        if cat:
            db.session.delete(cat)
        db.session.commit()
    # Remove test PNGs
    static_dir = os.path.join(app.root_path, "static")
    for rel in (RED_FILE, BLUE_FILE):
        full = os.path.join(static_dir, rel)
        if os.path.exists(full):
            os.remove(full)


def seed(app):
    with app.app_context():
        static_dir = os.path.join(app.root_path, "static")
        make_image(static_dir, RED_FILE, "red")
        make_image(static_dir, BLUE_FILE, "blue")

        cat = Category(name_en="Smoke P10C Cat", slug=CAT_SLUG, is_active=True)
        db.session.add(cat)
        seller = User(name="P10C Seller", email=SELLER, role="seller", is_active=True)
        seller.set_password(PASSWORD)
        db.session.add(seller)
        db.session.flush()
        vp = VendorProfile(user_id=seller.id, shop_name_en="P10C Store",
                           slug="p10c-store", status=VENDOR_APPROVED, commission_rate=10)
        db.session.add(vp)
        db.session.flush()
        red = Product(vendor_id=vp.id, category_id=cat.id, title_en="P10C Red Square",
                      slug="p10c-red-square", base_price=200, stock=10,
                      thumbnail=RED_FILE, status=PRODUCT_PUBLISHED)
        blue = Product(vendor_id=vp.id, category_id=cat.id, title_en="P10C Blue Square",
                       slug="p10c-blue-square", base_price=200, stock=10,
                       thumbnail=BLUE_FILE, status=PRODUCT_PUBLISHED)
        db.session.add_all([red, blue])
        db.session.commit()
        return {"red_id": red.id, "blue_id": blue.id,
                "red_slug": red.slug, "blue_slug": blue.slug}


def main():
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)
    ids = seed(app)

    # ====================================================================
    # model availability + embedding
    # ====================================================================
    with app.app_context():
        check("CLIP model loads", image_search_service.is_available())

        done, _ = image_search_service.embed_all_published(verbose=False)
        db.session.commit()
        check("embed_all_published embeds at least both test products", done >= 2)
        ours = ProductEmbedding.query.filter(
            ProductEmbedding.product_id.in_([ids["red_id"], ids["blue_id"]])
        ).all()
        check("both test products have float32 embeddings",
              len(ours) == 2 and all(len(e.embedding) == 512 * 4 for e in ours))

    # ====================================================================
    # search by image — service layer
    # ====================================================================
    with app.app_context():
        results_list = image_search_service.search_by_image(png_bytes("red"), limit=5)
        check("search returns ranked products",
              len(results_list) >= 2)
        top = results_list[0]
        check("the red image surfaces the Red Square first",
              top[0].slug == "p10c-red-square" and top[1] > 0.8)
        # blue should be present but with a lower score
        red_score = next(s for p, s in results_list if p.slug == "p10c-red-square")
        blue_score = next(s for p, s in results_list if p.slug == "p10c-blue-square")
        check("red image scores higher for red product than blue",
              red_score > blue_score)

    # ====================================================================
    # REST API
    # ====================================================================
    with app.test_client() as c:
        r = c.post("/api/v1/search/image",
                   data={"image": (io.BytesIO(png_bytes("blue")), "q.png")},
                   content_type="multipart/form-data")
        body = r.get_json() or {}
        prods = body.get("products", [])
        check("API /search/image returns matches",
              r.status_code == 200 and len(prods) >= 2)
        check("API top match for a blue query is the Blue Square",
              prods and prods[0]["slug"] == "p10c-blue-square")
        check("API result carries a similarity score",
              prods and "similarity" in prods[0])

        # missing image -> 400
        r = c.post("/api/v1/search/image", data={},
                   content_type="multipart/form-data")
        check("API rejects a request with no image (400)", r.status_code == 400)

    # ====================================================================
    # web — form + results page
    # ====================================================================
    with app.test_client() as c:
        r = c.get("/search/image/")
        check("web search-by-image form renders",
              r.status_code == 200 and b"Search by Image" in r.data)

        r = c.post("/search/image/",
                   data={"image": (io.BytesIO(png_bytes("red")), "q.png")},
                   content_type="multipart/form-data")
        check("web search-by-image returns the matching product",
              r.status_code == 200 and b"p10c-red-square" in r.data
              and b"% match" in r.data)

    # ====================================================================
    # voice + image search entry points in the search overlay
    # ====================================================================
    with app.test_client() as c:
        r = c.get("/")
        check("search overlay exposes voice (mic) + image-search buttons",
              r.status_code == 200 and b"micBtn" in r.data
              and b"Search by image" in r.data)

    purge(app)
    print("(test data cleaned up)")
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 10 image search smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
