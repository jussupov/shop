from .models import CartItem
from product.models import Product
from rest_framework import serializers
from product.serializers import ListProductSerializer
from utilities.exceptions import OverflowException
from django.shortcuts import get_object_or_404


class CartItemSerialzer(serializers.ModelSerializer):

    product = ListProductSerializer(read_only=True)
    products = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "cart", "products")
        read_only_fields = ("id", "cart")

    def save(self, **kwargs):
        validated_data = dict(list(self.validated_data.items()) + list(kwargs.items()))
        if validated_data["quantity"] > validated_data["product"].quantity:
            raise OverflowException()
        instance, _ = CartItem.objects.get_or_create(
            product=validated_data["product"], cart=validated_data["cart"]
        )

        instance.quantity = validated_data["quantity"]
        instance.save()
        return instance

