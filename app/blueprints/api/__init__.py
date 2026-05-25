"""REST API v1 — consumed by the customer & seller Flutter apps.

JSON in / JSON out, JWT-secured. The route modules are imported here so they
register their endpoints on the shared `api_v1` blueprint:

  auth     — registration, OTP login, password reset
  catalog  — public categories, products, search, stores
  cart     — cart & checkout (customer)
  account  — profile, addresses, orders (customer)
  seller   — products, order fulfilment, earnings (seller)
  docs     — OpenAPI spec + Swagger UI
"""
from flask import Blueprint

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# noqa: E402,F401 — imported for side effects (route registration)
from . import auth      # noqa: E402,F401
from . import catalog   # noqa: E402,F401
from . import cart      # noqa: E402,F401
from . import account   # noqa: E402,F401
from . import seller        # noqa: E402,F401
from . import chat          # noqa: E402,F401
from . import reviews       # noqa: E402,F401
from . import coupons       # noqa: E402,F401
from . import notifications # noqa: E402,F401
from . import docs          # noqa: E402,F401
