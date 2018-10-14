from logging import DEBUG, StreamHandler, getLogger

handler = StreamHandler()
handler.setLevel(DEBUG)

# デバッグ用ロガー(標準出力に出されて捨てられる)
logger_d = getLogger('django_debug')
logger_d.setLevel(DEBUG)
logger_d.addHandler(handler)

# エラーハンドリング用ロガー(django.logに残る)
logger_e = getLogger('error_handling')
logger_e.setLevel(DEBUG)
logger_e.addHandler(handler)
