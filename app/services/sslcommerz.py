"""SSLCommerz payment gateway integration — Phase 4.

Flow: init_payment() opens a gateway session and returns the hosted page URL;
the customer pays there; SSLCommerz calls our success/fail/cancel/IPN URLs;
validate_payment() confirms a transaction server-to-server.
"""
import requests
from flask import current_app

SANDBOX_BASE = "https://sandbox.sslcommerz.com"
LIVE_BASE = "https://securepay.sslcommerz.com"


def _base_url():
    sandbox = current_app.config.get("SSLCOMMERZ_SANDBOX", True)
    return SANDBOX_BASE if sandbox else LIVE_BASE


def is_configured():
    """True when sandbox/live store credentials are present."""
    return bool(
        current_app.config.get("SSLCOMMERZ_STORE_ID")
        and current_app.config.get("SSLCOMMERZ_STORE_PASSWORD")
    )


def init_payment(order, customer_email, success_url, fail_url, cancel_url, ipn_url):
    """Open an SSLCommerz session for `order`.

    Returns ``(True, gateway_page_url)`` or ``(False, error_message)``.
    """
    if not is_configured():
        return False, "Payment gateway is not configured."

    payload = {
        "store_id": current_app.config["SSLCOMMERZ_STORE_ID"],
        "store_passwd": current_app.config["SSLCOMMERZ_STORE_PASSWORD"],
        "total_amount": str(order.total_amount),
        "currency": "BDT",
        "tran_id": order.order_number,
        "success_url": success_url,
        "fail_url": fail_url,
        "cancel_url": cancel_url,
        "ipn_url": ipn_url,
        "cus_name": order.ship_name,
        "cus_email": customer_email or "customer@sgtcart.com",
        "cus_phone": order.ship_phone,
        "cus_add1": order.ship_address_line,
        "cus_city": order.ship_city,
        "cus_country": "Bangladesh",
        "shipping_method": "NO",
        "num_of_item": order.item_count,
        "product_name": f"SGT Order {order.order_number}",
        "product_category": "ecommerce",
        "product_profile": "general",
    }
    try:
        resp = requests.post(
            _base_url() + "/gwprocess/v4/api.php", data=payload, timeout=30
        )
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        current_app.logger.error("SSLCommerz init failed: %s", exc)
        return False, "Could not reach the payment gateway."

    if data.get("status") == "SUCCESS" and data.get("GatewayPageURL"):
        return True, data["GatewayPageURL"]
    return False, data.get("failedreason") or "The payment gateway rejected the request."


def validate_payment(val_id):
    """Validate a completed transaction with SSLCommerz.

    Returns the response dict, or None when validation cannot be performed.
    """
    if not is_configured() or not val_id:
        return None
    params = {
        "val_id": val_id,
        "store_id": current_app.config["SSLCOMMERZ_STORE_ID"],
        "store_passwd": current_app.config["SSLCOMMERZ_STORE_PASSWORD"],
        "format": "json",
    }
    try:
        resp = requests.get(
            _base_url() + "/validator/api/validationserverAPI.php",
            params=params, timeout=30,
        )
        return resp.json()
    except Exception as exc:  # noqa: BLE001
        current_app.logger.error("SSLCommerz validation failed: %s", exc)
        return None
