# URLconfはこれ
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from montage.settings.common import MEDIA_URL, MEDIA_ROOT
from montage.settings.common import DEBUG
from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # djangoのinclude内のnamespaceの仕様が変わったらしい
    # see: https://mocabrown.com/blog/archives/5346
    url(r'^', include(('accounts.urls', 'accounts'),)),
    url(r'^graphql/', GraphQLView.as_view(graphiql=True)),
]

# urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

if DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
