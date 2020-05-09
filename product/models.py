from django.db import models

from category.models import Category
from utilities.models import BaseModel, TimeAndActiveModel, TimeModel
from utilities.utils import unique_slug_generator
from account.models import User



class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.TextField()
    price = models.PositiveIntegerField(null=False)
    quantity = models.PositiveIntegerField()
    likes = models.PositiveIntegerField(default=0)
    box_quantity = models.PositiveIntegerField(default=0)
    old_price = models.PositiveIntegerField(null=True, blank=True)
    specification = models.ManyToManyField(to='ValueSpecification')

    def __str__(self):
        return f"{self.category} / {self.title}"

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(Product, self.title)
        super(Product, self).save(*args, **kwargs)


class Photo(TimeModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="product/images")

    def __str__(self):
        return f"{self.product} --> {self.image}"


class Specification(TimeModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category} | {self.title}"


class ValueSpecification(TimeModel):
    category_spec_types = models.ForeignKey(
        Specification, on_delete=models.CASCADE, related_name="spec"
    )
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category_spec_types} - {self.value}"


class Comment(TimeModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comments")
    active = models.BooleanField(default=False)
    body = models.TextField()
    answer = models.TextField(null=True, blank=True, default=None)
    

#
# class ProductSpecifications(TimeModel):
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, related_name="specification"
#     )
#     value = models.ForeignKey(ValueSpecification, on_delete=models.CASCADE, related_name="value")
#
#     def __str__(self):
#         return f"{self.product} - {self.category_spec_types}"
