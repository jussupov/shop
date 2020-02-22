from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . import serializers as order_serialzer
from .models import Order
from cart.models import Cart
from django.db.models import Sum, F


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = order_serialzer.OrderSerialzer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user, is_active=True)
        cart_items = cart.items.all()
        amount = cart_items.aggregate(
            sum=Sum(F("product__price") * F("quantity") * F("product__box_quantity"))
        )["sum"]
        serializer.save(cart=cart, amount=amount)

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user, cart__is_active=True)
