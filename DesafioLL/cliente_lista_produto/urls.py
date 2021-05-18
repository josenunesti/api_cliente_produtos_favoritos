from django.conf.urls import url
from rest_framework.authtoken import views
from .views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="API Produtos favoritos de clientes",
      default_version='v1',
      description="A API tem como objetivo prover features para um e-commerce para fazer a gestão de produtos favoritos de seus clientes.",
      terms_of_service="#",
      contact=openapi.Contact(email="jose@teste.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny]
)

urlpatterns = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^v1/client$', client),
    url(r'^v1/client/(?P<id_client>[0-9a-f-]+)$', client_detail),
    url(r'^v1/client/product_favorite$', client_favorite),
    url(r'^v1/client/product_favorite/(?P<id_client>[0-9a-f-]+)$', client_favorite),
    url(r'^v1/client/product_favorite/(?P<id_client>[0-9a-f-]+)/$', client_favorite),
    url(r'^v1/user/create$', CreateUser.as_view()),
    url(r'^v1/get_token_auth$', views.obtain_auth_token)
]
