from os import environ

try:
    from .common import *
except ImportError:
    print('/settings/common.pyがうまくインポート出来ていません')

# ここは本番用のみに適用される
# herokuの設定,S3の設定,
if not DEBUG:
    # ALLOWED_HOSTSにherokuのURLを書く
    ALLOWED_HOSTS = ['https://montage-graphql-api.herokuapp.com/']

    # Heroku
    import django_heroku
    django_heroku.settings(locals())

    # httpを強制的にhttpsでリダイレクトしてくれる(production用)
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # セッションクッキーと CSRF クッキーにセキュリティを適用する
    # see:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    CORS_ORIGIN_ALLOW_ALL = True
    INSTALLED_APPS += [
        'corsheaders'
        # 'cloudinary',
        # 'cloudinary_storage',
    ]

    # メール
    # EMAIL_HOST = 'smtp.gmail.com'
    # EMAIL_PORT = 587
    # EMAIL_HOST_USER = 'lv42s923@gmail.com'
    # EMAIL_HOST_PASSWORD = '7506kutsumi'
    # EMAIL_USE_TLS = True

    # CDNにCloudinaryを仕様
    # CLOUDINARY_STORAGE = {
    # 'CLOUD_NAME': 'kutsumi',
    # 'API_KEY': '967867132254792',
    # 'API_SECRET': 'oVNO1aizJ8zL7NlmqEHvI7y2fgk'
    # }
    # DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

