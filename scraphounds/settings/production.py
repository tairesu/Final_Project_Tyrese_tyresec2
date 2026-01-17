from .base import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'junkyardfinder.blake4it.com']
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = False
CSRF_TRUSTED_ORIGINS = [
    "https://junkyardfinder.blake4it.com",
]

STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'media'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django.security.DisallowedHost": {"handlers": ["console"], "level": "ERROR", "propagate": False},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": True},
    },
}
