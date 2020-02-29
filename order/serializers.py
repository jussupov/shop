from rest_framework import serializers
from .models import Order, Address, City


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "cart", "amount", "is_paid")
        read_only_fields = ("amount", "is_paid", "cart")

    def save(self, **kwargs):
        validated_data = dict(list(self.validated_data.items()) + list(kwargs.items()))
        instance, _ = Order.objects.get_or_create(cart=validated_data["cart"])
        instance.amount = validated_data["amount"]
        instance.save()
        return instance


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("title", "id")


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
