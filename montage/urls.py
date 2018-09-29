# URLconfはこれ
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from graphene_django.views import GraphQLView
from montage.schema import schema
from montage.settings.common import MEDIA_URL, MEDIA_ROOT
from montage.settings.common import DEBUG


from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path(r'admin/', admin.site.urls),
    # namespace for django 2.1 see: https://mocabrown.com/blog/archives/5346
    path('', include(('accounts.urls', 'accounts'),)),
    path('gql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),

]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
