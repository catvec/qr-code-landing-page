"""
Django settings for qrlanding project.
"""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


def get_env(key: str, default: str = "") -> str:
    """Get environment variable with default."""
    return os.environ.get(key, default)


# Security settings from environment
SECRET_KEY = get_env("SECRET_KEY", "django-insecure-dev-only-change-in-production")
DEBUG = get_env("DEBUG", "false") == "true"
ALLOWED_HOSTS = [h.strip() for h in get_env("ALLOWED_HOSTS", "").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in get_env("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# Application definition
INSTALLED_APPS = [
    # Unfold must come before django.contrib.admin
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third party
    "django_object_actions",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # Local apps
    "core",
    "pages",
]

# Required for django-allauth
SITE_ID = 1

# Site URL for building absolute URLs and OAuth redirects
SITE_URL = get_env("SITE_URL", "http://localhost:8000")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

ROOT_URLCONF = "qrlanding.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "qrlanding.wsgi.application"

# Database
DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgres://postgres:postgres@localhost:5432/qrlanding"
)
DATABASES = {"default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Unfold admin theme configuration
UNFOLD = {
    "SITE_TITLE": "QR Landing Pages",
    "SITE_HEADER": "QR Landing Pages",
}

# django-allauth configuration
# Silence warning about signup disabled but login enabled (intentional)
SILENCED_SYSTEM_CHECKS = ["account.W001"]

# Account settings - login only, no signups
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_SIGNUP_ENABLED = False

# Custom adapters to prevent signup
ACCOUNT_ADAPTER = "qrlanding.adapters.NoSignupAccountAdapter"
SOCIALACCOUNT_ADAPTER = "qrlanding.adapters.NoSignupSocialAccountAdapter"

# Social account settings
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET = True

# Google OAuth Provider
# Configure these in Google Cloud Console:
# - Dev redirect URI: http://localhost:8000/accounts/google/login/callback/
# - Prod redirect URI: https://yourdomain.com/accounts/google/login/callback/
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": get_env("GOOGLE_OAUTH_CLIENT_ID", ""),
            "secret": get_env("GOOGLE_OAUTH_SECRET", ""),
            "key": "",
        },
    }
}
