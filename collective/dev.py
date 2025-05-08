""" Django settings for collective project. """

import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = '2nac&+rq&^$yq#40lqh1ov4it9@qy$x51v@$ht1pllvth5cr#6'
DEBUG = True
ALLOWED_HOSTS = ['*']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


DJANGO_APPS = [
  # "daphne",
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
# -----------------------------------------------------------------------------

MIDDLEWARE = [
  'debug_toolbar.middleware.DebugToolbarMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django_htmx.middleware.HtmxMiddleware',
  # "django_browser_reload.middleware.BrowserReloadMiddleware",
]


# URL Mapper
# -----------------------------------------------------------------------------

ROOT_URLCONF = 'collective.urls'


# Templates
# ------------------------------------------------------------------------------

TEMPLATES = [{
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

WSGI_APPLICATION = 'collective.wsgi.application'
# ASGI_APPLICATION = 'collective.asgi.application'


# Database
# ------------------------------------------------------------------------------

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'collective',
    'USER': 'dbadmin',
    'PASSWORD': 'biology1010.',
    'HOST': '192.168.1.253',
    'PORT': '5432',
  }
}

# Password managament
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

# Sessions
# ------------------------------------------------------------------------------

SESSION_COOKIE_AGE = 604800 
INVALIDATE_PREVIOUS_SESSIONS = True


# Internationalization
# ------------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files
# ------------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles"),]


# Media files
# ------------------------------------------------------------------------------

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Authentication
# ------------------------------------------------------------------------------ 

AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_URL = "user_login"
LOGOUT_URL = "user_logout"
ACCOUNT_ACTIVATION_DAYS = 1
REGISTRATION_SALT = "q-vpbxvm!wl-jq!u-^09chepod1yu9_y)^&od%pnank761j@%9"
REGISTRATION_OPEN = True


# Email
# ------------------------------------------------------------------------------

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "support@jottingdown.dev"


# Logging
# ------------------------------------------------------------------------------

LOGGING = {
  "version": 1,
  "disable_existing_loggers": False,
  "handlers": {
    "file": {
      "level": "INFO",
      "class": "logging.FileHandler",
      "filename": "debug.log",
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


# django-tinymce
# ------------------------------------------------------------------------------

TINYMCE_SPELLCHECKER = False
FILE_UPLOAD_PERMISSIONS = 0o644
TINYMCE_DEFAULT_CONFIG = {
  'relative_urls': False,
  'remove_script_host': False,
  'convert_urls': True,
}


# django-debug-toolbar
# ------------------------------------------------------------------------------

INTERNAL_IPS = ["192.168.1.253", "localhost", "127.0.0.1"]


# django-recaptcha
# ------------------------------------------------------------------------------

RECAPTCHA_PUBLIC_KEY = '6LfZ4xkrAAAAAEMaoDGHPQrZbnrWdn3dM0QgY2RK'
RECAPTCHA_PRIVATE_KEY = '6LfZ4xkrAAAAAPsJEUn5-oyNoyDaQlVlUzJj7M9S'


# file-validator
# ------------------------------------------------------------------------------

FILE_UPLOAD_HANDLERS = ['django.core.files.uploadhandler.TemporaryFileUploadHandler']