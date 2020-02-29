from rest_framework.viewsets import ModelViewSet
from .models import Cart, CartItem
from product.models import Product
from .serialzers import CartItemSerialzer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
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

    @action(detail=False, methods=["post"])
    def bulk(self, request):
        for item in request.data:
            serialzer = CartItemSerialzer(data=item)
            serialzer.is_valid(raise_exception=True)
            cart, _ = Cart.objects.get_or_create(user=self.request.user, is_active=True)
            serialzer.save(cart=cart)
        return Response({"status": "Добавлено"}, status=status.HTTP_200_OK)

