from django.db import models
from utilities.models import TimeModel
from cart.models import Cart


class Order(TimeModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    payment_id = models.PositiveIntegerField(unique=True, null=True)

    def __str__(self):
        return f"{self.amount} {self.cart} -> {self.is_paid}"

