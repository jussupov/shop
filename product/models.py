from django.db import models
from utilities.models import TimeAndActiveModel, BaseModel, TimeModel
from category.models import Category


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.PositiveIntegerField(null=False)
    quantity = models.PositiveIntegerField()
    likes = models.PositiveIntegerField(default=0)
    box_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.category} / {self.title}"


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


class ProductSpecifications(TimeModel):
    category_spec_types = models.ForeignKey(
        Specification, on_delete=models.CASCADE, related_name="spec"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specification"
    )
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product} - {self.category_spec_types}"

