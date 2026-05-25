"""API v1 — OpenAPI 3.0 specification + Swagger UI.

`GET /api/v1/openapi.json` serves the machine-readable spec; `GET /api/v1/docs`
renders an interactive Swagger UI (loaded from a CDN) for exploring the API.
The spec is hand-maintained alongside the route modules.
"""
from flask import jsonify, Response

from . import api_v1

_SECURITY = [{"bearerAuth": []}]


def _op(tag, summary, secured=False, body=None, params=None):
    """Build a minimal OpenAPI operation object."""
    op = {"tags": [tag], "summary": summary, "responses": {"200": {"description": "OK"}}}
    if secured:
        op["security"] = _SECURITY
        op["responses"]["401"] = {"description": "Missing or invalid token"}
    if body:
        op["requestBody"] = {
            "content": {"application/json": {"schema": {
                "type": "object", "properties": {k: {"type": t} for k, t in body.items()},
            }}}
        }
    if params:
        op["parameters"] = [
            {"name": n, "in": loc, "schema": {"type": "string"}}
            for n, loc in params
        ]
    return op


def build_spec():
    """Assemble the full OpenAPI document."""
    q = [("page", "query"), ("per_page", "query"), ("q", "query"),
         ("category", "query"), ("min", "query"), ("max", "query"), ("sort", "query")]
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "SGT Cart API",
            "version": "1.0.0",
            "description": "REST API for the SGT Cart multi-vendor marketplace, "
                           "consumed by the customer and seller mobile apps. "
                           "Send `Accept-Language: bn` or `en` for localized content.",
        },
        "servers": [{"url": "/api/v1"}],
        "tags": [
            {"name": "Auth", "description": "Registration, OTP login, password reset"},
            {"name": "Catalog", "description": "Public categories, products, stores"},
            {"name": "Cart", "description": "Cart & checkout (customer)"},
            {"name": "Account", "description": "Profile, addresses, orders (customer)"},
            {"name": "Seller", "description": "Products, orders, earnings (seller)"},
            {"name": "Chat", "description": "Support & seller messaging (triaged)"},
            {"name": "Reviews", "description": "Verified-purchase product reviews"},
            {"name": "Coupons", "description": "Discount codes"},
            {"name": "Notifications", "description": "In-app feed & device push tokens"},
        ],
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
            }
        },
        "paths": {
            # --- Auth ---
            "/auth/register": {"post": _op(
                "Auth", "Create a customer or seller account",
                body={"name": "string", "email": "string", "phone": "string",
                      "password": "string", "role": "string",
                      "shop_name": "string", "referral_code": "string"})},
            "/auth/login": {"post": _op(
                "Auth", "Log in — emails a one-time code",
                body={"email": "string", "password": "string"})},
            "/auth/verify-otp": {"post": _op(
                "Auth", "Verify the OTP — returns access & refresh tokens",
                body={"email": "string", "code": "string"})},
            "/auth/resend-otp": {"post": _op(
                "Auth", "Resend the login OTP", body={"email": "string"})},
            "/auth/refresh": {"post": _op(
                "Auth", "Exchange a refresh token for a new access token",
                secured=True)},
            "/auth/forgot-password": {"post": _op(
                "Auth", "Email a password reset code", body={"email": "string"})},
            "/auth/reset-password": {"post": _op(
                "Auth", "Reset the password with the OTP",
                body={"email": "string", "code": "string", "password": "string"})},
            "/auth/me": {"get": _op("Auth", "Current authenticated user", secured=True)},

            # --- Catalog ---
            "/categories": {"get": _op("Catalog", "List active categories")},
            "/products": {"get": _op(
                "Catalog", "List/search published products", params=q)},
            "/products/{slug}": {"get": _op(
                "Catalog", "Product detail with related items",
                params=[("slug", "path")])},
            "/search/suggest": {"get": _op(
                "Catalog", "Search autocomplete suggestions",
                params=[("q", "query")])},
            "/search/image": {"post": _op(
                "Catalog", "Find visually similar products (multipart `image` field)")},
            "/products/{slug}/similar": {"get": _op(
                "Catalog", "Similar products (same category, ranked)",
                params=[("slug", "path")])},
            "/products/{slug}/also-viewed": {"get": _op(
                "Catalog", "Products other customers viewed alongside this one",
                params=[("slug", "path")])},
            "/recommendations": {"get": _op(
                "Account", "Personal product recommendations", secured=True)},
            "/stores": {"get": _op("Catalog", "List approved seller stores")},
            "/stores/{slug}": {"get": _op(
                "Catalog", "Store page with its products",
                params=[("slug", "path")] + q)},

            # --- Cart & checkout ---
            "/cart": {"get": _op("Cart", "Get the current cart", secured=True)},
            "/cart/items": {"post": _op(
                "Cart", "Add an item to the cart", secured=True,
                body={"product_id": "integer", "variant_id": "integer",
                      "quantity": "integer"})},
            "/cart/items/{item_id}": {
                "patch": _op("Cart", "Update a cart line's quantity", secured=True,
                             body={"quantity": "integer"},
                             params=[("item_id", "path")]),
                "delete": _op("Cart", "Remove a cart line", secured=True,
                              params=[("item_id", "path")]),
            },
            "/checkout": {"post": _op(
                "Cart", "Place an order from the cart", secured=True,
                body={"address_id": "integer", "payment_method": "string",
                      "coupon_code": "string", "points_to_redeem": "integer",
                      "affiliate_code": "string"})},

            # --- Coupons ---
            "/coupons": {"get": _op(
                "Coupons", "List active platform coupons", secured=True)},
            "/coupons/validate": {"post": _op(
                "Coupons", "Validate a coupon against the cart", secured=True,
                body={"code": "string"})},

            # --- Flash sales & rewards ---
            "/flash-sales": {"get": _op(
                "Coupons", "Live flash sales with discounted products")},
            "/rewards": {"get": _op(
                "Account", "Reward-points balance and history", secured=True)},
            "/referral": {"get": _op(
                "Account", "Referral code, share stats & affiliate earnings",
                secured=True)},

            # --- Account ---
            "/account/profile": {"patch": _op(
                "Account", "Update name / phone / locale", secured=True,
                body={"name": "string", "phone": "string", "locale": "string"})},
            "/addresses": {
                "get": _op("Account", "List saved addresses", secured=True),
                "post": _op("Account", "Add an address", secured=True,
                            body={"full_name": "string", "phone": "string",
                                  "address_line": "string", "city": "string"}),
            },
            "/addresses/{address_id}": {
                "patch": _op("Account", "Update an address", secured=True,
                             params=[("address_id", "path")]),
                "delete": _op("Account", "Delete an address", secured=True,
                              params=[("address_id", "path")]),
            },
            "/addresses/{address_id}/default": {"post": _op(
                "Account", "Set the default address", secured=True,
                params=[("address_id", "path")])},
            "/orders": {"get": _op("Account", "Order history", secured=True)},
            "/orders/{order_number}": {"get": _op(
                "Account", "Order detail", secured=True,
                params=[("order_number", "path")])},

            # --- Seller ---
            "/seller/profile": {"get": _op(
                "Seller", "Seller profile + wallet summary", secured=True)},
            "/seller/products": {
                "get": _op("Seller", "List the seller's products", secured=True,
                           params=[("status", "query")]),
                "post": _op("Seller", "Create a product (draft)", secured=True,
                            body={"title_en": "string", "category_id": "integer",
                                  "base_price": "number", "stock": "integer"}),
            },
            "/seller/products/{product_id}": {
                "get": _op("Seller", "Seller product detail", secured=True,
                           params=[("product_id", "path")]),
                "patch": _op("Seller", "Update a product", secured=True,
                             params=[("product_id", "path")]),
                "delete": _op("Seller", "Delete a product", secured=True,
                              params=[("product_id", "path")]),
            },
            "/seller/products/{product_id}/submit": {"post": _op(
                "Seller", "Submit a product for admin review", secured=True,
                params=[("product_id", "path")])},
            "/seller/products/{product_id}/variants": {"post": _op(
                "Seller", "Add a variant", secured=True,
                params=[("product_id", "path")],
                body={"size": "string", "color": "string",
                      "price": "number", "stock": "integer"})},
            "/seller/products/{product_id}/variants/{variant_id}": {"delete": _op(
                "Seller", "Delete a variant", secured=True,
                params=[("product_id", "path"), ("variant_id", "path")])},
            "/seller/orders": {"get": _op(
                "Seller", "Seller's sub-orders", secured=True,
                params=[("status", "query")])},
            "/seller/orders/{sub_order_id}": {"get": _op(
                "Seller", "Sub-order detail", secured=True,
                params=[("sub_order_id", "path")])},
            "/seller/orders/{sub_order_id}/status": {"post": _op(
                "Seller", "Update fulfilment status", secured=True,
                params=[("sub_order_id", "path")], body={"status": "string"})},
            "/seller/earnings": {"get": _op(
                "Seller", "Wallet, sales stats & payout history", secured=True)},
            "/seller/payouts": {"post": _op(
                "Seller", "Request a payout", secured=True,
                body={"amount": "number", "method": "string"})},
            "/seller/analytics": {"get": _op(
                "Seller", "Sales metrics, top products, forecast", secured=True,
                params=[("days", "query")])},

            # --- Chat ---
            "/chat/support/topics": {"get": _op(
                "Chat", "Support triage topics", secured=True)},
            "/chat/threads": {"get": _op(
                "Chat", "List the user's chat threads", secured=True)},
            "/chat/threads/support": {"post": _op(
                "Chat", "Open a triaged support thread", secured=True,
                body={"topic": "string", "order_number": "string"})},
            "/chat/threads/vendor": {"post": _op(
                "Chat", "Open a chat with a seller", secured=True,
                body={"vendor_slug": "string", "product_slug": "string"})},
            "/chat/threads/{thread_id}": {"get": _op(
                "Chat", "Thread with its messages", secured=True,
                params=[("thread_id", "path")])},
            "/chat/threads/{thread_id}/messages": {"post": _op(
                "Chat", "Send a message (phone numbers are stripped)",
                secured=True, params=[("thread_id", "path")],
                body={"body": "string"})},
            "/chat/threads/{thread_id}/read": {"post": _op(
                "Chat", "Mark a thread read", secured=True,
                params=[("thread_id", "path")])},

            # --- Reviews ---
            "/products/{slug}/reviews": {
                "get": _op("Reviews", "List a product's reviews",
                           params=[("slug", "path")]),
                "post": _op("Reviews", "Write a review (delivered purchase only)",
                            secured=True, params=[("slug", "path")],
                            body={"rating": "integer", "title": "string",
                                  "comment": "string"}),
            },
            "/reviews/reviewable": {"get": _op(
                "Reviews", "Products awaiting the customer's review", secured=True)},
            "/reviews/mine": {"get": _op(
                "Reviews", "Reviews the customer has written", secured=True)},

            # --- Notifications & devices ---
            "/notifications": {"get": _op(
                "Notifications", "List in-app notifications", secured=True)},
            "/notifications/unread-count": {"get": _op(
                "Notifications", "Unread notification count", secured=True)},
            "/notifications/{notification_id}/read": {"post": _op(
                "Notifications", "Mark one notification read", secured=True,
                params=[("notification_id", "path")])},
            "/notifications/read-all": {"post": _op(
                "Notifications", "Mark all notifications read", secured=True)},
            "/devices": {
                "post": _op("Notifications", "Register an FCM device token",
                            secured=True,
                            body={"token": "string", "platform": "string"}),
                "delete": _op("Notifications", "Unregister a device token",
                              secured=True, body={"token": "string"}),
            },
        },
    }


@api_v1.route("/openapi.json", methods=["GET"])
def openapi_spec():
    return jsonify(build_spec())


_SWAGGER_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SGT Cart API — Docs</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    window.ui = SwaggerUIBundle({
      url: "/api/v1/openapi.json",
      dom_id: "#swagger-ui",
      deepLinking: true,
      persistAuthorization: true
    });
  </script>
</body>
</html>"""


@api_v1.route("/docs", methods=["GET"])
def swagger_ui():
    return Response(_SWAGGER_HTML, mimetype="text/html")
