from .models import CartItem
from rest_framework import serializers
from product.serializers import ListProductSerializer


class CartItemSerialzer(serializers.ModelSerializer):

    product = ListProductSerializer()

    class Meta:
        model = CartItem
        fields = ("product", "qunatity")
