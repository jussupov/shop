from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView
from cart.views import CartView

router = DefaultRouter()

router.register("category", CategoryView, basename="category")
router.register("cart", CartView, basename="cart")

urlpatterns = [path("", include(router.urls))]
