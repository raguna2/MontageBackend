# ここは開発環境にのみ適用される

try:
    print('devが読み込まれました')
    from .common import *
except ImportError:
    print('/settings/common.pyがうまくインポート出来ていません')

# メール
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
