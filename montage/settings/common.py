import os
import sys

from .settings_secret import (SECRET_KEY, DATABASE_NAME, DATABASE_USER,
                              SOCIAL_AUTH_TWITTER_KEY,
                              SOCIAL_AUTH_TWITTER_SECRET,
                              GOOGLE_RECAPTCHA_SECRET_KEY)

DEBUG = True

# ファイルパスの設定  --------------------------------------------------
# BASE_DIRはmanage.pyがあるディレクトリ
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# /montage/apps/ 以下をアプリを追加していくディレクトリにする
sys.path.append(os.path.join(BASE_DIR, "apps"))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
ROOT_URLCONF = 'montage.urls'
WSGI_APPLICATION = 'montage.wsgi.application'
# ファイルパスの設定  --------------------------------------------------

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# ミドルウェア
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# DEBUG_TOOLBAR_SETTINGS
DEBUG_TOOLBAR_PATCH_SETTINGS = False
if DEBUG:
    INTERNAL_IPS = ('172.17.0.1', 'localhost',)
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
else:
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# DEBUG_TOOLBAR_SETTINGS --------------------------------------

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
            'filename': os.path.join(BASE_DIR, 'django.log'),  # どこに出すか
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
