from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductView

router = DefaultRouter()

router.register("product", ProductView, basename="product")

urlpatterns = [path("", include(router.urls))]
