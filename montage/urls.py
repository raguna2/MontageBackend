# URLconfはこれ
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from montage.settings import common

urlpatterns = [
    path('admin/', admin.site.urls),
    # namespace for django 2.1 see: https://mocabrown.com/blog/archives/5346
    path('', include(('accounts.urls', 'accounts'), )),
    path('gql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

if not common.DEBUG:
    urlpatterns += static(common.MEDIA_URL, document_root=common.MEDIA_ROOT)
    urlpatterns += static(common.STATIC_URL, document_root=common.STATIC_ROOT)
