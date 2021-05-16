from django.conf.urls import url
from rest_framework.authtoken import views
from .views import *
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^api/client$', client),
    url(r'^api/client/(?P<id_client>[0-9a-f-]+)$', client_detail),
    url(r'^api/client/product_favorite$', client_favorite),
    url(r'^api/client/product_favorite/(?P<id_client>[0-9a-f-]+)$', client_favorite),
    url(r'^api/client/product_favorite/(?P<id_client>[0-9a-f-]+)/$', client_favorite),
    url(r'^api/user/create$', CreateUser.as_view()),
    url(r'^get_token_auth$', views.obtain_auth_token)
]
