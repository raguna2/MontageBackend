# URLconfはこれ
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from settings.common import MEDIA_URL, MEDIA_ROOT, DEBUG

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^', include('accounts.urls', namespace='accounts')),
]

# urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

# if DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#         url(r'^__debug__/', include(debug_toolbar.urls)),
#     ]
