import os
import sys
from pathlib import Path

import environ

import cloudinary

from .settings_secret import DATABASE_NAME, DATABASE_USER, SECRET_KEY

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
STATIC_URL = '/static/'
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR / 'media')
STATIC_ROOT = str(BASE_DIR / 'static')

ROOT_URLCONF = 'montage.urls'
WSGI_APPLICATION = 'montage.wsgi.application'

###########################
# Apps
###########################
CONTRIB_APPS = [
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
    'accounts.apps.AccountsConfig',
    'categories.apps.CategoriesConfig',
    'portraits.apps.PortraitsConfig',
    'relationships.apps.RelationshipsConfig',
    'friendships.apps.FriendshipsConfig',
]
EXTERNAL_APPS = [
    'graphene_django',
    'django_filters',
    'corsheaders',
    'django_cleanup', # ファイルアップロード
    'cloudinary',
    'cloudinary_storage',
]
INSTALLED_APPS = CONTRIB_APPS + EXTERNAL_APPS + PROJECT_APPS

###########################
# MiddleWare
###########################
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

###########################
# DATABASE
###########################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DATABASE_NAME,
        'USER': DATABASE_USER,
        'HOST': 'postgres',
        'PORT': 5432,
    }
}

###########################
# Validator
###########################
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

###########################
# Localize
###########################
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True


###########################
# LOGGING
###########################
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(processName)s(%(process)d)][%(name)s][L%(lineno)d][%(levelname)s] %(message)s',  # NOQA
            'datefmt': '%Y-%m-%d %H:%M:%S %z',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

###########################
# Cloudinary
###########################
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
)
