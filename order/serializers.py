from rest_framework import serializers
from .models import Order


class OrderSerialzer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("cart", "amount", "is_paid")
        read_only_fields = ("amount", "is_paid", "cart")

    def save(self, **kwargs):
        validated_data = dict(list(self.validated_data.items()) + list(kwargs.items()))
        print(validated_data)
        instance, _ = Order.objects.get_or_create(cart=validated_data["cart"])
        instance.amount = validated_data["amount"]
        instance.save()
        return instance
