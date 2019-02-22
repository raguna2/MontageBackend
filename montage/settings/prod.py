from os import environ

# Heroku
import django_heroku

from montage.apps.logging import logger_d, logger_e

try:
    logger_d.info('prodを読み込んでいます')
    from .common import *
    logger_d.info('prodとcommonが読み込まれました')
except ImportError:
    logger_e.error('/settings/common.pyがうまくインポート出来ていません')

# ここは本番用のみに適用される
# herokuの設定,S3の設定,
DEBUG = True
# ALLOWED_HOSTSにherokuのURLを書く
ALLOWED_HOSTS = ['*']

django_heroku.settings(locals())

# httpを強制的にhttpsでリダイレクトしてくれる(production用)
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# セッションクッキーと CSRF クッキーにセキュリティを適用する
# see:
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = False
