"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY', "django-insecure-wu*-bz_&9)ema4f*-0r_5%zxg!mavny(2d2oiz7y-h0iz2a%6=")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", 'True') == 'True'

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", '127.0.0.1,localhost,100.42.176.190').split(',')

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "simple_history",
    "django_extensions",
    "rest_framework",
    'rest_framework_simplejwt',
    "storages",
    "portfolio",
    "common",
    'widget_tweaks',
    "corsheaders",
    'django_filters',
    'django_celery_results',
    'django_celery_beat',

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'simple_history.middleware.HistoryRequestMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",

]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.getenv("CACHE_REDIS_URL", 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

REDIS_CACHE_TIMEOUT = int(os.getenv("REDIS_CACHE_TIMEOUT", 60 * 60 * 24))

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
INTERNAL_IPS = [
    "127.0.0.1",
]
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SIMPLE_HISTORY_FILEFIELD_TO_CHARFIELD = True

MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", '3ZlW8xTkeINu1VmNI0nl')
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", 'KhzoD8UZS7FWPntLy11JxWuyXeYTPdmiSRbnas4i')
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", 'photos')
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")

AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
AWS_S3_ENDPOINT_URL = MINIO_ENDPOINT
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = True
AWS_S3_FILE_OVERWRITE = False
AWS_S3_REGION_NAME = None
AWS_S3_USE_SSL = False
AWS_S3_VERIFY = False


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
#
# else:
#     MEDIA_URL = '{}/media/'.format(AWS_S3_ENDPOINT_URL)
#
#     STATIC_URL = '/static/'
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#
#     STATICFILES_DIRS = [
#         os.path.join(BASE_DIR, 'static'),
#     ]
#
#     DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
#
#     STORAGES = {
#         "default": {
#             "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#             "OPTIONS": {
#                 "access_key": AWS_ACCESS_KEY_ID,
#                 "secret_key": AWS_SECRET_ACCESS_KEY,
#                 "bucket_name": AWS_STORAGE_BUCKET_NAME,
#                 "endpoint_url": AWS_S3_ENDPOINT_URL,
#                 "use_ssl": AWS_S3_USE_SSL,
#                 "verify": AWS_S3_VERIFY,
#             },
#         },
#         "staticfiles": {
#             "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
#         },
#     }
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", 'True') == 'True'

CORS_ALLOWED_ORIGINS = [
    "http://100.42.176.190:4200",
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://0.0.0.0:4200",
]
CORS_ORIGIN_WHITELIST = ('127.0.0.1', 'localhost', '0.0.0.0', '100.42.176.190')

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'sessionId'
]

CORS_ALLOW_CREDENTIALS = True

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = "django-db"
CELERY_RESULT_EXTENDED = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG' if DEBUG else 'INFO')

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{asctime} {levelname} {name} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'verbose',
#         },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': os.path.join(LOG_DIR, 'application.log'),
#             'when': 'midnight',
#             'backupCount': 30,
#             'formatter': 'verbose',
#         },
#         'django_file': {
#             'level': 'ERROR',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': os.path.join(LOG_DIR, 'django.log'),
#             'when': 'midnight',
#             'backupCount': 30,
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         '': {
#             'handlers': ['console', 'file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django': {
#             'handlers': ['console', 'django_file'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'celery.utils.functional': {
#             'handlers': ['console', 'file'],
#             'level': 'WARNING',
#             'propagate': False,
#         },
# 'PIL.Image': {
#             'handlers': ['console', 'file'],
#             'level': 'WARNING',
#             'propagate': False,
#         },
#     },
# }