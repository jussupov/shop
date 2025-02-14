from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from account.jwt import CustomTokenObtainPairView


schema_view = get_schema_view(
    openapi.Info(
        title="www-shop API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("admin/", admin.site.urls),
    path("api/", include("category.urls")),
    path("api/", include("product.urls")),
    path("api/token", CustomTokenObtainPairView.as_view()),
    path("api/token/refresh", TokenRefreshView.as_view()),
    path("", include("account.urls")),
    path("api/", include("order.urls"))
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
