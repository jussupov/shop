from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView
from cart.views import CartView
from order.views import OrderView

router = DefaultRouter()

router.register("category", CategoryView, basename="category")
router.register("cart", CartView, basename="cart")
router.register("order", OrderView, basename="order")


urlpatterns = [path("", include(router.urls))]
