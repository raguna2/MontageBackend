# accouts/url.py
from django.urls import path

from .views import mainview

# accountsのURLパターン
urlpatterns = [
    # トップページ
    path('', mainview, name='main'),
]
