from rest_framework.viewsets import ModelViewSet
from .models import Cart, CartItem
from product.models import Product
from .serialzers import CartItemSerialzer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status


class CartView(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerialzer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)
        queryset = CartItem.objects.filter(cart=cart)
        serializer_class = CartItemSerialzer(queryset, many=True)
        return Response(serializer_class.data)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
        serializer.save(cart=cart)

    # def create(self, request):
    #     cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)

    #     serialzer = CartItemCreateSerializer()

    #     product = get_object_or_404(Product, id=request.data["product"])

    #     if int(request.data["quantity"]) > product.quantity:
    #         return Response(
    #             {"message": "Количество больше чем товаров"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     data = {
    #         "cart_id": cart.id,
    #         "product_id": request.data["product"],
    #         "quantity": request.data["quantity"],
    #     }

    #     serialzer.save(data)

    #     return Response({"message": "Добавлено"}, status=status.HTTP_201_CREATED)
