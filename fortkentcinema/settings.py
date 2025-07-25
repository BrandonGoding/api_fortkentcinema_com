"""
Django settings for fortkentcinema project.

Generated by 'django-admin startproject' using Django 5.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path

from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ENABLE_CDN = config("ENABLE_CDN", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "blog.apps.BlogConfig",
    "cinema.apps.CinemaConfig",
    "core.apps.CoreConfig",
    "rest_framework",
    "corsheaders",
]

if ENABLE_CDN:
    INSTALLED_APPS += [
        "storages",
    ]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "fortkentcinema.urls"

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

WSGI_APPLICATION = "fortkentcinema.wsgi.application"

if config("USE_POSTGRES", default=False, cast=bool):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_DB"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": "localhost",
            "PORT": "",
        }
    }
else:
    # Use SQLite by default if not using Postgres
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_TZ = True

if ENABLE_CDN:
    # === S3 & CloudFront ===
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = "cdn.fortkentcinema.com"
    AWS_S3_REGION_NAME = "us-east-1"  # or your bucket’s region
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_QUERYSTRING_AUTH = False  # no ?X-Amz-Signature on public files
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=31536000, public",  # 1 year (change if needed)
    }

    # CloudFront domain you created
    CLOUDFRONT_DOMAIN = "cdn.fortkentcinema.com"

    # ---------- STATIC ----------
    STATICFILES_STORAGE = "fortkentcinema.storage_backends.StaticStorage"
    STATIC_URL = f"https://{CLOUDFRONT_DOMAIN}/static/"

    # ---------- MEDIA ----------
    DEFAULT_FILE_STORAGE = "fortkentcinema.storage_backends.MediaStorage"
    MEDIA_URL = f"https://{CLOUDFRONT_DOMAIN}/media/"

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "bucket_name": AWS_STORAGE_BUCKET_NAME,
                "region_name": AWS_S3_REGION_NAME,
                "access_key": AWS_ACCESS_KEY_ID,
                "secret_key": AWS_SECRET_ACCESS_KEY,
                "custom_domain": CLOUDFRONT_DOMAIN,
            },
        },
        "staticfiles": {
            "BACKEND": "fortkentcinema.storage_backends.StaticStorage",
        },
    }
else:
    STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static_collected"  # local tmp dir for collectstatic


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
OMDB_API_KEY = config("OMDB_API_KEY", default=None)
CORS_ALLOWED_ORIGINS = [
    "https://www.fortkentcinema.com",
    "https://fortkentcinema.com",
    "http://localhost:3000",
    "http://192.168.2.112:3000",
]

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 6,
}
