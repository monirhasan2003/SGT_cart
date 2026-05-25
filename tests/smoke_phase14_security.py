"""Phase 14 (Chunk A) smoke test — security headers, CSRF, rate limits,
production secret-key guard.

Run:  venv\\Scripts\\python.exe tests\\smoke_phase14_security.py
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app

results = []


def check(name, ok, detail=""):
    results.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  -- {detail}" if detail else ""))


def main():
    # ====================================================================
    # security response headers (dev config)
    # ====================================================================
    app = create_app("development")
    with app.test_client() as c:
        r = c.get("/")
        h = r.headers
        check("Content-Security-Policy header present",
              "default-src 'self'" in (h.get("Content-Security-Policy") or ""))
        check("script-src allows the CDNs our pages load",
              "cdn.jsdelivr.net" in (h.get("Content-Security-Policy") or "")
              and "cdn.socket.io" in (h.get("Content-Security-Policy") or ""))
        check("X-Frame-Options is SAMEORIGIN",
              h.get("X-Frame-Options") == "SAMEORIGIN")
        check("X-Content-Type-Options is nosniff",
              h.get("X-Content-Type-Options") == "nosniff")
        check("Referrer-Policy set", h.get("Referrer-Policy") == "same-origin")
        check("Permissions-Policy keeps mic/camera same-origin",
              "microphone=(self)" in (h.get("Permissions-Policy") or "")
              and "geolocation=()" in (h.get("Permissions-Policy") or ""))
        check("HSTS is NOT sent in DEBUG (dev / plain HTTP)",
              "Strict-Transport-Security" not in h)

    # ====================================================================
    # CSRF is enforced on web forms (no token -> 400)
    # ====================================================================
    app = create_app("development")
    with app.test_client() as c:
        r = c.post("/signup/", data={"first_name": "x", "email": "x@y.z",
                                     "password": "abcdef", "confirm_password": "abcdef"})
        check("POST without CSRF token is rejected (400)", r.status_code == 400)

    # ====================================================================
    # rate limit kicks in on a tightly-limited endpoint
    # ====================================================================
    app = create_app("development")
    with app.test_client() as c:
        # /search/suggest is limited to 60/min — hammer it past the cap.
        statuses = [c.get("/search/suggest?q=widget").status_code for _ in range(65)]
        check("rate limit returns 429 once the cap is hit",
              429 in statuses,
              detail=f"last statuses: {statuses[-3:]}")

    # ====================================================================
    # production refuses to boot with the dev SECRET_KEY
    # ====================================================================
    from config import ProductionConfig
    original = ProductionConfig.SECRET_KEY
    ProductionConfig.SECRET_KEY = "dev-insecure-change-me"
    raised = False
    try:
        create_app("production")
    except RuntimeError as exc:
        raised = "SECRET_KEY" in str(exc)
    finally:
        ProductionConfig.SECRET_KEY = original
    check("production refuses to boot with the insecure default key", raised)

    # And HSTS IS sent when DEBUG is off.
    app = create_app("production")
    with app.test_client() as c:
        r = c.get("/")
        check("HSTS is sent when DEBUG is off",
              "max-age=" in (r.headers.get("Strict-Transport-Security") or ""))

    passed, total = sum(results), len(results)
    print(f"\n=== Phase 14 security smoke test: {passed}/{total} passed ===")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
