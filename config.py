import os
from dotenv import load_dotenv

# ==========================================
# LOAD ENV VARIABLES
# ==========================================

load_dotenv()


# ==========================================
# BASE CONFIG
# ==========================================

class Config:
    """
    Base Configuration
    """

    # --------------------------------------
    # Flask
    # --------------------------------------

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "change_this_secret_key"
    )

    DEBUG = False

    TESTING = False

    # --------------------------------------
    # MongoDB Atlas
    # --------------------------------------

    MONGO_URI = os.getenv(
        "MONGO_URI",
        ""
    )

    DATABASE_NAME = os.getenv(
        "DATABASE_NAME",
        "mudhai_db"
    )

    # --------------------------------------
    # Upload Settings
    # --------------------------------------

    BASE_DIR = os.path.abspath(
        os.path.dirname(__file__)
    )

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    MAX_CONTENT_LENGTH = (
        16 * 1024 * 1024
    )  # 16MB

    # --------------------------------------
    # Allowed File Types
    # --------------------------------------

    ALLOWED_EXTENSIONS = {

        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp",

        "pdf",

        "doc",
        "docx",

        "xls",
        "xlsx"

    }

    # --------------------------------------
    # Admin Session
    # --------------------------------------

    ADMIN_SESSION_KEY = "admin"

    PERMANENT_SESSION_LIFETIME = 3600

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SECURE = False

    SESSION_COOKIE_SAMESITE = "Lax"

    # --------------------------------------
    # Admin Credentials
    # --------------------------------------

    ADMIN_USERNAME = os.getenv(
        "ADMIN_USERNAME",
        "admin"
    )

    ADMIN_PASSWORD = os.getenv(
        "ADMIN_PASSWORD",
        "admin123"
    )

    # --------------------------------------
    # Mail Settings
    # --------------------------------------

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = int(
        os.getenv(
            "MAIL_PORT",
            587
        )
    )

    MAIL_USE_TLS = True

    MAIL_USE_SSL = False

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME"
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD"
    )

    DEFAULT_MAIL_SENDER = os.getenv(
        "MAIL_USERNAME"
    )

    # --------------------------------------
    # Cloudinary
    # --------------------------------------

    CLOUDINARY_CLOUD_NAME = os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    )

    CLOUDINARY_API_KEY = os.getenv(
        "CLOUDINARY_API_KEY"
    )

    CLOUDINARY_API_SECRET = os.getenv(
        "CLOUDINARY_API_SECRET"
    )

    # --------------------------------------
    # Pagination
    # --------------------------------------

    PRODUCTS_PER_PAGE = 12

    BLOGS_PER_PAGE = 9

    ENQUIRIES_PER_PAGE = 20

    # --------------------------------------
    # Branding
    # --------------------------------------

    SITE_NAME = (
        "Mudhai Instrument Services"
    )

    COMPANY_EMAIL = os.getenv(
        "COMPANY_EMAIL",
        "info@mudhai.com"
    )

    COMPANY_PHONE = os.getenv(
        "COMPANY_PHONE",
        "+91XXXXXXXXXX"
    )

    # --------------------------------------
    # Security Headers
    # --------------------------------------

    SECURITY_HEADERS = {

        "X-Frame-Options":
        "SAMEORIGIN",

        "X-Content-Type-Options":
        "nosniff",

        "Referrer-Policy":
        "strict-origin"

    }


# ==========================================
# DEVELOPMENT
# ==========================================

class DevelopmentConfig(Config):

    DEBUG = True

    SESSION_COOKIE_SECURE = False


# ==========================================
# PRODUCTION
# ==========================================

class ProductionConfig(Config):

    DEBUG = False

    SESSION_COOKIE_SECURE = True


# ==========================================
# TESTING
# ==========================================

class TestingConfig(Config):

    TESTING = True

    DEBUG = True


# ==========================================
# CONFIG DICTIONARY
# ==========================================

config = {

    "development":
    DevelopmentConfig,

    "production":
    ProductionConfig,

    "testing":
    TestingConfig

}


# ==========================================
# CURRENT CONFIG
# ==========================================

current_config = config.get(

    os.getenv(
        "FLASK_ENV",
        "development"
    ),

    DevelopmentConfig

)