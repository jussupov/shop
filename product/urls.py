from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductView, CommentView

router = DefaultRouter()

router.register("product", ProductView, basename="product")

urlpatterns = [path("", include(router.urls))]
