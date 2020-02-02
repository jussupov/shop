from django.contrib import admin
from .models import CategorySpecTypes, Product, ProductImage, ProductSpecValues


admin.site.register(CategorySpecTypes)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductSpecValues)

