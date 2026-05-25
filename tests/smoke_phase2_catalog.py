"""Phase 2 smoke test — catalog models + admin category management.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase2_catalog.py <admin_password>
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.extensions import db
from app.models.catalog import Category

ADMIN_EMAIL = "monirhasan2003@gmail.com"
PARENT_NAME = "Smoke Cat Parent"
CHILD_NAME = "Smoke Cat Child"

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def purge(app):
    with app.app_context():
        for nm in (CHILD_NAME, PARENT_NAME):
            for c in Category.query.filter_by(name_en=nm).all():
                db.session.delete(c)
        db.session.commit()


def main():
    admin_password = sys.argv[1] if len(sys.argv) > 1 else ""
    app = create_app("development")
    app.config["WTF_CSRF_ENABLED"] = False
    purge(app)

    with app.app_context():
        seeded = Category.query.count()
        check("Seeded categories present", seeded >= 24, f"{seeded} categories")
        roots = Category.query.filter_by(parent_id=None).count()
        check("Root categories present", roots >= 5, f"{roots} roots")

    with app.test_client() as c:
        c.post("/admin/login", data={"email": ADMIN_EMAIL, "password": admin_password})

        r = c.get("/admin/categories/")
        check("Admin categories page", r.status_code == 200 and b"Electronics" in r.data)

        r = c.get("/admin/categories/create")
        check("New category form", r.status_code == 200)

        # create parent
        r = c.post("/admin/categories/create", data={
            "name_en": PARENT_NAME, "name_bn": "স্মোক",
            "sort_order": "99", "is_active": "on",
        })
        with app.app_context():
            parent = Category.query.filter_by(name_en=PARENT_NAME).first()
            check("Category created", parent is not None and parent.slug != "")
            parent_id = parent.id if parent else None

        # edit parent
        c.post(f"/admin/categories/{parent_id}/edit", data={
            "name_en": PARENT_NAME, "name_bn": "updated", "sort_order": "5", "is_active": "on",
        })
        with app.app_context():
            check("Category edited", db.session.get(Category, parent_id).name_bn == "updated")

        # create child under parent
        r = c.post("/admin/categories/create", data={
            "name_en": CHILD_NAME, "parent_id": str(parent_id), "sort_order": "0", "is_active": "on",
        })
        with app.app_context():
            child = Category.query.filter_by(name_en=CHILD_NAME).first()
            check("Sub-category created", child is not None and child.parent_id == parent_id)
            child_id = child.id if child else None

        # deleting a parent that has children must be blocked
        c.post(f"/admin/categories/{parent_id}/delete")
        with app.app_context():
            check("Delete blocked (has sub-category)",
                  db.session.get(Category, parent_id) is not None)

        # delete child, then parent
        c.post(f"/admin/categories/{child_id}/delete")
        with app.app_context():
            check("Sub-category deleted", db.session.get(Category, child_id) is None)
        c.post(f"/admin/categories/{parent_id}/delete")
        with app.app_context():
            check("Parent category deleted", db.session.get(Category, parent_id) is None)

    # localized() helper
    with app.test_client() as c:
        c.get("/?lang=bn")
    with app.app_context():
        cat = Category(name_en="EN Only", name_bn="", slug="smoke-en-only")
        check("localized() falls back to English", cat.localized_name == "EN Only")

    purge(app)
    passed, total = sum(results), len(results)
    print(f"\n=== Phase 2 catalog smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
