# URLconfはこれ
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

from montage.settings.common import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    # path('jet/', include(('jet.urls', 'jet'), )),
    path('admin/', admin.site.urls),
    # namespace for django 2.1 see: https://mocabrown.com/blog/archives/5346
    path('', include(('accounts.urls', 'accounts'), )),
    path('social/', include(('social_django.urls', 'social'), )),
    path('gql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
