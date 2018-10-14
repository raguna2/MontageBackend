# ここは開発環境にのみ適用される
from montage.apps.logging import logger_d, logger_e

try:
    logger_d.info('devを読み込んでいます')
    from .common import *
    logger_d.info('devとcommonが正常に読み込まれました')
except ImportError:
    logger_e.error('/settings/common.pyがうまくインポート出来ていません')

# メール
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

