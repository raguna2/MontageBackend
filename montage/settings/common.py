import socket
import sys
import environ
from pathlib import Path

from .settings_secret import (DATABASE_NAME, DATABASE_USER,
                              GOOGLE_RECAPTCHA_SECRET_KEY, SECRET_KEY,
                              SOCIAL_AUTH_TWITTER_KEY,
                              SOCIAL_AUTH_TWITTER_SECRET)

# 開発環境のホスト名をhostnameに入力し、
# see: https://mmmmemo.com/20180615_python_django_02/
hostname = '564f62e4dbfb'
if socket.gethostname() == hostname:
    DEBUG = True
else:
    DEBUG = False

AUTH_USER_MODEL = 'accounts.MontageUser'
GRAPHENE = {
    'SCHEMA': 'montage.schema.schema'
}
ALLOWED_HOSTS = ['*']

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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
PROJECT_APPS = [
    'accounts',
    'categories',
    'portraits'
]
EXTERNAL_APPS = [
    'graphene_django',
    'django_filters',
]
INSTALLED_APPS = CONTRIB_APPS + PROJECT_APPS + EXTERNAL_APPS
# アプリケーション情報 -------------------------------------------------
# ミドルウェア
MIDDLEWARE = [
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
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
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
LOGGING = {
    'version': 1,   # これを設定しないと怒られる
    'formatters': {  # 出力フォーマットを文字列形式で指定する
        'all': {    # 出力フォーマットに`all`という名前をつける
            'format': '\t'.join([
                "[%(levelname)s]",
                "asctime:%(asctime)s",
                "module:%(module)s",
                "message:%(message)s",
                "process:%(process)d",
                "thread:%(thread)d",
            ])
        },
    },
    'handlers': {  # ログをどこに出すかの設定
        'file': {  # どこに出すかの設定に名前をつける `file`という名前をつけている
            'level': 'DEBUG',  # DEBUG以上のログを取り扱うという意味
            'class': 'logging.FileHandler',  # ログを出力するためのクラスを指定
            'filename': str(BASE_DIR / 'django.log'),  # どこに出すか
            'formatter': 'all',  # どの出力フォーマットで出すかを名前で指定
        },
        'console': {  # どこに出すかの設定をもう一つ、こちらの設定には`console`という名前
            'level': 'DEBUG',
            # こちらは標準出力に出してくれるクラスを指定
            'class': 'logging.StreamHandler',
            'formatter': 'all'
        },
    },
    'loggers': {  # どんなloggerがあるかを設定する
        'command': {  # commandという名前のloggerを定義
            'handlers': ['file', 'console'],  # 先述のfile, consoleの設定で出力
            'level': 'DEBUG',
        },
    },
}
# LOGGING_SETTINGS-----------------------------------------------------------------
