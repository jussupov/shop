from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . import serializers as order_serialzer
from .models import Order
from cart.models import Cart
from django.db.models import Sum, F
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from utilities.task import Payment
from rest_framework.response import Response
from rest_framework import status


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
        return serializer.save(cart=cart, amount=amount)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        payment = Payment(
            order.amount, "KZT", "Вы купили товар на сайте", str(order.id)
        )
        r = payment.create_payment()
        order.payment_id = int(r.json()["id"])
        order.save()
        if r.status_code == 201:
            return Response(r.json(), status=200)
        else:
            return Response({"response": False, "error_message": r.json()}, 500)

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user, cart__is_active=True)


@api_view(["POST"])
def payment_status_webhook(request):
    if request.data["status"]["code"] == "success":
        order = Order.objects.filter(id=int(request.data["order"])).first()
        order.is_paid = True
        order.reservation.is_paid = True
        order.reservation.save()
        order.save()
    return Response(request.data, status.HTTP_200_OK)

