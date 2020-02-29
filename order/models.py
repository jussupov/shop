from django.db import models
from utilities.models import TimeModel
from cart.models import Cart
from phonenumber_field.modelfields import PhoneNumberField


class Order(TimeModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    payment_id = models.PositiveIntegerField(unique=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.cart} -> {self.is_paid}"


class City(TimeModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Address(TimeModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    phone = PhoneNumberField(blank=True)

