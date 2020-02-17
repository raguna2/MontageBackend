# URLconfはこれ
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    # namespace for django 2.1 see: https://mocabrown.com/blog/archives/5346
    path('', include(('apps.accounts.urls', 'accounts'), )),
    path('gql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

if not settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
