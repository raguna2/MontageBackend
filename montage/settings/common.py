import os
import sys
from pathlib import Path

import environ

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .settings_secret import (DATABASE_NAME, DATABASE_USER,
                              GOOGLE_RECAPTCHA_SECRET_KEY, SECRET_KEY,
                              SOCIAL_AUTH_TWITTER_KEY,
                              SOCIAL_AUTH_TWITTER_SECRET)

# 開発環境のホスト名をhostnameに入力し、
# see: https://mmmmemo.com/20180615_python_django_02/
DEBUG = True

AUTH_USER_MODEL = 'accounts.MontageUser'
GRAPHENE = {'SCHEMA': 'montage.schema.schema'}
ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'localhost:8000',
    'localhost:8080',
    'localhost:8040',
)
# デプロイで失敗時にメールを飛ばしてくれる
# see: http://hideharaaws.hatenablog.com/entry/2014/12/14/005342
ADMINS = (('Name', 'kutsumi.for.public@gmail.com'))

# ファイルパスの設定  --------------------------------------------------
# BASE_DIRはmanage.pyがあるディレクトリ
BASE_DIR = Path(environ.Path(__file__) - 2).resolve()

# /montage/apps/ 以下をアプリを追加していくディレクトリにする
# ディレクトリ構成については下記を参照
# see :https://qiita.com/aion/items/ca375efac5b90deed382
APPS_DIR = BASE_DIR / 'apps'
sys.path.append(str(APPS_DIR))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(BASE_DIR / 'templates')],
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
# 相対パス
STATIC_URL = '/static/'
MEDIA_URL = "/media/"
# 絶対パス
MEDIA_ROOT = str(BASE_DIR / 'media')
STATIC_ROOT = str(BASE_DIR / 'static')

ROOT_URLCONF = 'montage.urls'
WSGI_APPLICATION = 'montage.wsgi.application'
# ファイルパスの設定  --------------------------------------------------
# アプリケーション情報 -------------------------------------------------
CONTRIB_APPS = [
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
SITE_ID = 1
PROJECT_APPS = [
    'montage.apps.accounts.apps.AccountsConfig',
    'categories.apps.CategoriesConfig',
    'portraits.apps.PortraitsConfig',
]
EXTERNAL_APPS = [
    'graphene_django',
    'django_filters',
    'corsheaders',
    'django_extensions',
    'django_cleanup',
]
INSTALLED_APPS = CONTRIB_APPS + EXTERNAL_APPS + PROJECT_APPS
# アプリケーション情報 -------------------------------------------------
# ミドルウェア
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]
# MIDDLEWARE_CLASS = (
#     'app.CorsMiddleware'
# )
# ミドルウェア
# DATABASE ------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'HOST': 'postgres',
        'PORT': 5432,
    }
}
# DATABASE ------------------------------------------
# バリデータ ----------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
# バリデータ ----------------------------------------
# Localize --------------------------
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# Localize --------------------------
# LOGGING_SETTINGS-----------------------------------------------------------------
# see: https://qiita.com/tnnsst35/items/c7d8705cb412e7869d47
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format':
            f'[*%(levelname)s*] %(asctime)s\t場所:%(pathname)s/%(filename)s\n'
            f'処理が止まった場所:%(funcName)sの%(lineno)d行目\n'
            f'エラーメッセージ:%(message)s'
        },
        'log_filing': {
            'format':
            f'%(levelname)s\t%(asctime)s\t%(pathname)s\t%(filename)s\t'
            f'%(funcName)s\t%(lineno)d\t%(message)s'
        },
        'simple': {
            'format': '%(levelname)s\t%(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            'formatter': 'simple'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logfile': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(BASE_DIR / 'django.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 0,
            'formatter': 'log_filing',
        }
    },
    'loggers': {
        'django_debug': {
            'handlers': ['null', 'console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'error_handling': {
            'handlers': ['console', 'logfile'],
            'level': 'ERROR',
            'propagate': False
        },
    }
}
# LOGGING_SETTINGS-----------------------------------------------------------------
# Sentry --------------------------------------------------------------------------
sentry_sdk.init(
    dsn="https://de580293695e4353893fdd2f499fd65e@sentry.io/1291134",
    integrations=[DjangoIntegration()])
# Sentry --------------------------------------------------------------------------
# Django-jet ----------------------------------------------------------------------
JET_DEFAULT_THEME = 'default'
# サイドバーを見やすくする
JET_SIDE_MENU_COMPACT = True
# Django-jet ----------------------------------------------------------------------

