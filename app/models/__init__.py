"""SQLAlchemy models for SGT Cart.

Every model module must be imported here so Flask-Migrate's autogenerate
detects all tables.

    Phase 1  -> user, vendor, otp
    Phase 2  -> catalog
    Phase 3  -> cart, order
    Phase 4  -> payment
    Phase 8  -> chat, notification
    Phase 9  -> marketing
    Phase 11 -> analytics
"""
from .user import User, Address, ROLE_CUSTOMER, ROLE_SELLER, ROLE_ADMIN  # noqa: F401
from .vendor import (  # noqa: F401
    VendorProfile, VENDOR_PENDING, VENDOR_APPROVED, VENDOR_SUSPENDED,
)
from .otp import OtpCode, OTP_PURPOSE_LOGIN, OTP_PURPOSE_RESET  # noqa: F401
from .catalog import (  # noqa: F401
    Category, Brand, Product, ProductVariant, ProductImage, ProductSpec,
    ProductPriceTier,
    PRODUCT_DRAFT, PRODUCT_PENDING, PRODUCT_PUBLISHED, PRODUCT_REJECTED,
)
from .qa import Question, Answer, AnswerVote  # noqa: F401
from .cart import CartItem  # noqa: F401
from .order import (  # noqa: F401
    Order, SubOrder, OrderItem, SubOrderEvent,
    PAYMENT_COD, PAYMENT_SSLCOMMERZ, PAYMENT_PENDING, PAYMENT_PAID, PAYMENT_FAILED,
    SUBORDER_PENDING, SUBORDER_PROCESSING, SUBORDER_SHIPPED,
    SUBORDER_DELIVERED, SUBORDER_CANCELLED, SUBORDER_STATUSES,
)
from .payment import (  # noqa: F401
    Transaction, GATEWAY_COD, GATEWAY_SSLCOMMERZ,
    TXN_INITIATED, TXN_PENDING, TXN_SUCCESS, TXN_FAILED, TXN_CANCELLED,
)
from .wallet import (  # noqa: F401
    VendorWallet, PayoutRequest,
    PAYOUT_REQUESTED, PAYOUT_APPROVED, PAYOUT_REJECTED, PAYOUT_STATUSES,
)
from .setting import Setting, AuditLog  # noqa: F401
from .review import Review, ReviewImage, RATING_MIN, RATING_MAX  # noqa: F401
from .analytics import ProductView, SearchLog  # noqa: F401
from .embedding import ProductEmbedding  # noqa: F401
from .banner import (  # noqa: F401
    HomepageBanner, BANNER_HERO, BANNER_STRIP, BANNER_KINDS,
)
from .marketing import (  # noqa: F401
    Coupon, CouponRedemption, FlashSale, FlashSaleItem, RewardLedger,
    Referral, AffiliateCommission, AbandonedCart,
    COUPON_PLATFORM, COUPON_VENDOR, COUPON_SCOPES,
    DISCOUNT_PERCENT, DISCOUNT_FIXED, DISCOUNT_TYPES,
)
from .chat import (  # noqa: F401
    ChatThread, ChatMessage, CHAT_SUPPORT, CHAT_VENDOR, CHAT_KINDS,
    SUPPORT_PURCHASE, SUPPORT_DELIVERY, SUPPORT_REFUND, SUPPORT_OTHER,
    SUPPORT_TOPICS, SUPPORT_TOPIC_LABELS,
)
from .notification import (  # noqa: F401
    Notification, DeviceToken,
    NOTIF_ORDER, NOTIF_CHAT, NOTIF_PAYOUT, NOTIF_PRODUCT, NOTIF_SYSTEM, NOTIF_KINDS,
    DEVICE_ANDROID, DEVICE_IOS, DEVICE_WEB,
)
from .policy import (  # noqa: F401
    PolicyViolation, SURFACE_CHAT, SURFACE_REVIEW, SURFACE_QA, SURFACES,
    SELLER_VIOLATION_THRESHOLD,
)
from .stock import StockNotification  # noqa: F401
from .district import DistrictEta  # noqa: F401
