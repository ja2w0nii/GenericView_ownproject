import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# .env
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "192.168.50.85"]

# Application definition

INSTALLED_APPS = [
    # Channels
    "channels",
    "chat",
    # django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # cors
    "corsheaders",
    # local apps
    "users",
    "posts",
    # allauth apps
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Keycloak
    "allauth.socialaccount.providers.keycloak",
]

MIDDLEWARE = [
    # cors
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 로그인 여부 확인
    "users.middleware.JsonWebTokenMiddleWare",
]

CORS_ORIGIN_WHITELIST = ["http://127.0.0.1:8000", "http://192.168.50.85"]

ROOT_URLCONF = "genericview.urls"

INTERNAL_IPS = [
    "127.0.0.1",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "genericview.wsgi.application"
ASGI_APPLICATION = "genericview.routing.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "generic",
    #     "USER": "root",
    #     "PASSWORD": "dkapflzksh0829!",
    #     "HOST": "localhost",
    #     "PORT": "3306",
    # }
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# user model
AUTH_USER_MODEL = "users.User"


# allauth
SITE_ID = 1

LOGIN_REDIRECT_URL = "/"
# LOGOUT_REDIRECT_URL = "/users/signin"

# SESSION_COOKIE_AGE = 7200

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)


# keycloak
SOCIALACCOUNT_PROVIDERS = {
    "keycloak": {
        "KEYCLOAK_URL": "http://127.0.0.1:8080",
        "KEYCLOAK_REALM": "genericrealm",
        "KEYCLOAK_CLIENT_ID": "genericclient",
        "KEYCLOAK_CLIENT_SECRET": "n5d5aUFAu2pX5yORXmRwKuPkq9m4iKrn",
    },
}


# channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
