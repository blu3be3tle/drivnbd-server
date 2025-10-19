from urllib.parse import urlparse
from pathlib import Path
import cloudinary
import dj_database_url
from decouple import config
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# Core
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = [
    "drivnbd-serverside.vercel.app",
    ".vercel.app",
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.vercel.app",
    "https://drivnbd-serverside.vercel.app",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://drivnbd-client.vercel.app"
]

# Apps
INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "drf_yasg",
    "django_filters",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
    "djoser",
    "cloudinary",
    "cloudinary_storage",
    # Local
    "api",
    "users",
    "store",
    "order",
]

# Debug Toolbar only when DEBUG=True
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

ROOT_URLCONF = "drivnbd.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "drivnbd.wsgi.app"

# Database
DATABASES = {
    "default": dj_database_url.config(
        default=config("DATABASE_URL"),  # pyright: ignore[reportArgumentType]
        conn_max_age=60,
        ssl_require=True,
    )
}

# Passwords
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# I18N
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static & media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Auth / DRF
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Enter your JWT token in the format: `JWT <your_token>`'
        }
    }
}

# Djoser
DJOSER = {
    'EMAIL_FRONTEND_PROTOCOL': config('FRONTEND_PROTOCOL'),
    'EMAIL_FRONTEND_DOMAIN': config('FRONTEND_DOMAIN'),
    'EMAIL_FRONTEND_SITE_NAME': 'DrivnBD',
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    "SERIALIZERS": {
        "user_create": "users.serializers.UserCreateSerializer",
        "current_user": "users.serializers.UserSerializer",
    },
}


# Email (dev)
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')


# Cloudinary
cloudinary.config(
    cloud_name=config("CLOUD_NAME"),
    api_key=config("API_KEY"),
    api_secret=config("API_SECRET"),
    secure=True,
)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
