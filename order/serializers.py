from rest_framework import serializers
from .models import Order


class OrderSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("cart", "amount", "is_paid")
        read_only_fields = ("amount", "is_paid", "cart")
