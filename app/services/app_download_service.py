"""App-download QR helper — Phase 15 D-10.

The product-page footer renders a QR code only when the admin has set
the `app_download_url` platform setting (typically a one-link/store URL
that lands on Play Store + App Store). The QR image itself is served by
``api.qrserver.com``, a no-key public generator — switching to a local
qrcode-library implementation is a 1-line edit if the dependency is
ever added.
"""
from urllib.parse import quote

from app.services.settings_service import get_setting

QR_GENERATOR = "https://api.qrserver.com/v1/create-qr-code/"


def app_download_url():
    """The configured app-download URL (None when not set)."""
    raw = (get_setting("app_download_url") or "").strip()
    return raw or None


def qr_image_url(url, size=140):
    """Return an `<img src="…">`-ready QR image URL for `url`."""
    if not url:
        return None
    return f"{QR_GENERATOR}?size={size}x{size}&data={quote(url, safe='')}"
