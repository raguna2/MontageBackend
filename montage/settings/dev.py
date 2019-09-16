# ここは開発環境にのみ適用される
import logging

logger = logging.getLogger(__name__)

try:
    logger.info('devを読み込んでいます')
    from .common import *
    logger.info('devとcommonが正常に読み込まれました')
except ImportError as e:
    logger.error('/settings/common.pyがうまくインポート出来ていません')
    logger.error(e)

# メール
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

