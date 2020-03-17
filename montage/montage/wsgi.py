"""
WSGI config for montage project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from dj_static import Cling
from django.core.wsgi import get_wsgi_application

"""
DJANGO_SETTINGS_MODULEは設定ファイルのある場所の環境変数
"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "montage.settings")

application = Cling(get_wsgi_application())
