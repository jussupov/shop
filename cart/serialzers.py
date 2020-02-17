from .models import CartItem
from rest_framework import serializers
from product.serializers import ListProductSerializer


class CartItemSerialzer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
