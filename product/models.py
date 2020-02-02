from django.db import models
from category.models import Category
from utilities.models import TimeAndActiveModel, BaseModel, TimeModel


class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.PositiveIntegerField(null=False)
    quantity = models.PositiveIntegerField()
    likes = models.PositiveIntegerField(default=0)
    box_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.category} / {self.title}"


class ProductImage(TimeModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="product/images")

    def __str__(self):
        return f"{self.product} --> {self.image}"


class CategorySpecTypes(TimeModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category} | {self.title}"


class ProductSpecValues(TimeModel):
    category_spec_types = models.ForeignKey(
        CategorySpecTypes, on_delete=models.CASCADE, related_name="spec"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product} - {self.category_spec_types}"

