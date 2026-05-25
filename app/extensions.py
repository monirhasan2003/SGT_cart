"""Flask extension singletons.

Each extension is instantiated once here and bound to the app inside the
application factory (`app/__init__.py`). Importing extensions from this module
(rather than the factory) avoids circular imports between models, blueprints
and the factory.

Real-time uses Flask-SocketIO (Phase 8). It runs in `threading` async mode so
no eventlet/gevent is required; when a Redis URL is configured the factory
passes it as a message queue so multiple workers can share events.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_babel import Babel
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_socketio import SocketIO

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()
jwt = JWTManager()
babel = Babel()
cors = CORS()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()
socketio = SocketIO(async_mode="threading", cors_allowed_origins="*")

# Where to redirect anonymous users hitting a login-required web page.
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"

# The `user_loader` is registered in `app/models/user.py` (it needs the User model).
