import os
import sys

import cloudinary
import django_heroku

# 開発環境のホスト名をhostnameに入力し、
# see: https://mmmmemo.com/20180615_python_django_02/
DEBUG = os.environ.get('DJANGO_DEBUG', True)
SECRET_KEY = os.environ['SECRET_KEY']

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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# /montage/apps/ 以下をアプリを追加していくディレクトリにする
# ディレクトリ構成については下記を参照
# see :https://qiita.com/aion/items/ca375efac5b90deed382
sys.path.append(os.path.join(BASE_DIR, "apps"))

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

ROOT_URLCONF = 'montage.urls'
WSGI_APPLICATION = 'montage.wsgi.application'

###########################
# Apps
###########################
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'graphene_django',
    'django_filters',
    'corsheaders',
    'django_cleanup',
    'cloudinary',
    'cloudinary_storage',
    'apps.accounts.apps.AccountsConfig',
    'apps.categories.apps.CategoriesConfig',
    'apps.portraits.apps.PortraitsConfig',
    'apps.relationships.apps.RelationshipsConfig',
    'apps.friendships.apps.FriendshipsConfig',
]
SITE_ID = 1

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
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

###########################
# DATABASE
###########################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_DATABASE'),
        'USER': os.environ.get('DB_USERNAME'),
        'HOST': os.environ.get('DB_HOST', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'password'),
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
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'DEBUG')
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

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
API_IDENTIFIER = os.environ.get('AUTH0_API_IDENTIFIER')
ALGORITHMS = ["RS256"]
MGT_CLIENT_ID = os.environ.get('MGT_CLIENT_ID')
MGT_CLIENT_ID_SECRET = os.environ.get('MGT_CLIENT_ID_SECRET')

if not DEBUG:
    # ALLOWED_HOSTSにherokuのURLを書く
    ALLOWED_HOSTS = [
        'https://montage.bio',
        os.environ.get('DJANGO_DEBUG_HOST', 'http://montage.bio')
    ]

    django_heroku.settings(locals())

    # httpを強制的にhttpsでリダイレクトしてくれる(production用)
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # セッションクッキーと CSRF クッキーにセキュリティを適用する
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = False

    ###########################
    # Sentry
    ###########################
    from sentry_sdk.integrations.django import DjangoIntegration
    import sentry_sdk
    sentry_sdk.init(
        dsn="https://de580293695e4353893fdd2f499fd65e@sentry.io/1291134",
        integrations=[DjangoIntegration()])

    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_BROWSER_XSS_FILTER = True
