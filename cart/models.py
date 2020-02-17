from django.db import models
from account.models import User
from product.models import Product
from utilities.models import TimeAndActiveModel, TimeModel


class Cart(TimeAndActiveModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(TimeModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qunatity = models.PositiveIntegerField(default=1)
