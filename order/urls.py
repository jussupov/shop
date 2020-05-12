from .views import OrderView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("order", OrderView, basename="order")


urlpatterns = [
    path("", include(router.urls))
]