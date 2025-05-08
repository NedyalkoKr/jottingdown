""" Django settings for jottingdown project. """

import os, environ, sentry_sdk
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env('/home/ubuntu/.env_5882c0a5a5572cbfc895q8WWGPcqYc85hNwalLbMDBtIXFRE7dmByEXU85')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ['jottingdown.com', '*.jottingdown.com']


# Application definition
# ------------------------------------------------------------------------------

DJANGO_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.humanize',
  'django.contrib.sites',
  'django.contrib.postgres',
]

THIRD_PARTY_APPS = [
  'django_extensions',
  'debug_toolbar',
  'django_htmx',
  'tinymce',
  'widget_tweaks',
]

LOCAL_APPS = [
  'accounts.apps.AccountsConfig',
  'core.apps.CoreConfig',
  'topics.apps.TopicsConfig',
  'search.apps.SearchConfig',
  'analytics.apps.AnalyticsConfig',
  'comments.apps.CommentsConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# Middleware
# ------------------------------------------------------------------------------


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]


# URL Mapper
# ------------------------------------------------------------------------------

ROOT_URLCONF = 'jottingdown.urls'


# Templates
# ------------------------------------------------------------------------------

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]


# Deployment
# ------------------------------------------------------------------------------

WSGI_APPLICATION = 'jottingdown.wsgi.application'
# ASGI_APPLICATION = 'jottingdown.asgi.application'


# Database
# ------------------------------------------------------------------------------

DATABASES = {
  "default": env.db(),
  "OPTIONS":{
    "sslmode": "verify-full",
    "pool": True,
  },
}


# Password validation
# ------------------------------------------------------------------------------

PASSWORD_MIN_LENGTH = 12
PASSWORD_MAX_LENGTH = 64
PASSWORD_RESET_TIMEOUT = 600
PASSWORD_HASHERS = ["django.contrib.auth.hashers.Argon2PasswordHasher",]
AUTH_PASSWORD_VALIDATORS = [
  {
    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "OPTIONS": {
      "max_similarity": 0.6,
    },
  },
  {
    "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    "OPTIONS": {"min_length": PASSWORD_MIN_LENGTH},
  },
  {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
  {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
  {
    "NAME": "validators.account_validators.PasswordMaximumLengthValidator",
    "OPTIONS": {"max_length": PASSWORD_MAX_LENGTH},
  },
  {"NAME": "validators.account_validators.PasswordSpecialCharacterValidator"},
]


# Internationalization
# ------------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Sessions
# ------------------------------------------------------------------------------

SESSION_COOKIE_AGE = 604800 
INVALIDATE_PREVIOUS_SESSIONS = True


# Static files
# ------------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles"),]


# Media files
# ------------------------------------------------------------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Security
# ------------------------------------------------------------------------------

X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
SESSION_COOKIE_SAMESITE = "Lax"
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin'
USE_X_FORWARDED_HOST = True


# Authentication
# ------------------------------------------------------------------------------ 

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_URL = "user_login"
LOGOUT_URL = "user_logout"
ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_SALT = os.environ["REGISTRATION_SALT"]
REGISTRATION_OPEN = True


# Email
# ------------------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = "support@jottingdown.com"
EMAIL_HOST = 'in-v3.mailjet.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
MANAGERS = ("nedcoder@gmail.com",)


# Logging
# ------------------------------------------------------------------------------

LOGGING = {
  "version": 1,
  "disable_existing_loggers": False,
  # 'filters': {
  # 	'require_debug_false': {
  # 		'()': 'django.utils.log.RequireDebugFalse'
  # 	}
  # },
  "handlers": {
    "file": {
      "level": "INFO",
      "class": "logging.FileHandler",
      "filename": "/home/ubuntu/django.log",
    },
  },
  "loggers": {
    "django": {
      "handlers": ["file"],
      "level": "INFO",
      "propagate": True,
    },
  },
}


# Sites
# ------------------------------------------------------------------------------

SITE_ID = 1


# django-storage
# ------------------------------------------------------------------------------

STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STORAGES = {
  "default": {
      "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
      "OPTIONS": {
        'bucket_name': os.getenv('BUCKET_NAME'),
        'access_key': os.getenv('ACCESS_KEY_ID'),
        'secret_key': os.getenv('SECRET_ACCESS_KEY'),
        'region_name': 'nyc3',
        'endpoint_url': os.getenv('ENDPOINT_URL'),
    },
  },
  "staticfiles": {
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
  },
}


# file-validator
# ------------------------------------------------------------------------------

FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.TemporaryFileUploadHandler']


# django-maintenance-mode
# ------------------------------------------------------------------------------

# if True the maintenance mode will be activated
MAINTENANCE_MODE = True

# the template that will be shown by the maintenance-mode page
MAINTENANCE_MODE_TEMPLATE = "pages/maintenance.html"

# if True admin site will not be affected by the maintenance-mode page
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True

# by default, a file named "maintenance_mode_state.txt" will be created in the settings.py directory
# you can customize the state file path in case the default one is not writable
MAINTENANCE_MODE_STATE_FILE_PATH = "/home/ubuntu/maintenance_mode_state.txt"

# the value in seconds of the Retry-After header during maintenance-mode
MAINTENANCE_MODE_RETRY_AFTER = 3600

# the HTTP status code to send
MAINTENANCE_MODE_STATUS_CODE = 200

# Retrieve user's real IP address using django-ipware:
MAINTENANCE_MODE_GET_CLIENT_IP_ADDRESS = "ipware.ip.get_ip"

# the absolute url where users will be redirected to during maintenance-mode
MAINTENANCE_MODE_REDIRECT_URL = None