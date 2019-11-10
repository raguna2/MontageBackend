import logging
from os import environ

# Heroku
import django_heroku

import sentry_sdk

logger = logging.getLogger(__name__)

try:
    logger.info('prodを読み込んでいます')
    from .common import *
    logger.info('prodとcommonが読み込まれました')
except ImportError as e:
    logger.error('/settings/common.pyがうまくインポート出来ていません')
    logger.error(e)

# ここは本番用のみに適用される
# herokuの設定,S3の設定,
DEBUG = False
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


###########################
# Sentry
###########################
sentry_sdk.init(
    dsn="https://de580293695e4353893fdd2f499fd65e@sentry.io/1291134",
    integrations=[DjangoIntegration()])
