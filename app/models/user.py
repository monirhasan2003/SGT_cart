"""User and Address models — Phase 1 (Auth & Users)."""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, login_manager

ROLE_CUSTOMER = "customer"
ROLE_SELLER = "seller"
ROLE_ADMIN = "admin"
ROLES = (ROLE_CUSTOMER, ROLE_SELLER, ROLE_ADMIN)


class User(UserMixin, db.Model):
    """A platform account — customer, seller or admin."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=ROLE_CUSTOMER)
    locale = db.Column(db.String(5), nullable=False, default="en")
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_email_verified = db.Column(db.Boolean, nullable=False, default=False)
    # Loyalty reward-points balance (Phase 9); history in RewardLedger.
    reward_points = db.Column(db.Integer, nullable=False, default=0)
    # Personal referral / affiliate code (Phase 9); assigned on first use.
    referral_code = db.Column(db.String(12), unique=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login_at = db.Column(db.DateTime)
    # Phase 15 D-7 — drives the "Last seen X min ago" chat presence indicator.
    # Stamped on socket connect/disconnect and whenever the user posts a chat
    # message.
    last_seen_at = db.Column(db.DateTime)

    vendor_profile = db.relationship(
        "VendorProfile", back_populates="user",
        uselist=False, cascade="all, delete-orphan",
    )
    addresses = db.relationship(
        "Address", back_populates="user",
        cascade="all, delete-orphan", order_by="Address.id",
    )

    # --- password ---
    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

    # --- role helpers ---
    @property
    def is_admin(self):
        return self.role == ROLE_ADMIN

    @property
    def is_seller(self):
        return self.role == ROLE_SELLER

    @property
    def is_customer(self):
        return self.role == ROLE_CUSTOMER

    @property
    def requires_otp(self):
        """Customers & sellers verify an emailed OTP on every login; admins don't."""
        return self.role != ROLE_ADMIN

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Address(db.Model):
    """A customer's saved shipping address."""

    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    label = db.Column(db.String(50))               # Home / Office
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_line = db.Column(db.String(255), nullable=False)
    area = db.Column(db.String(120))
    city = db.Column(db.String(120), nullable=False)
    district = db.Column(db.String(120))
    postal_code = db.Column(db.String(20))
    is_default = db.Column(db.Boolean, nullable=False, default=False)
    # Phase 15 D-9 B4 — buyer opts in to avoid delivery during Jumma /
    # Maghrib prayer times. Couriers honour the flag where supported.
    prayer_time_delivery = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address {self.id} of user {self.user_id}>"


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login user loader."""
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None
