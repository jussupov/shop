from django.contrib import admin
from .models import Product, Specification, ProductSpecifications, Photo


admin.site.register(ProductSpecifications)
admin.site.register(Product)
admin.site.register(Specification)
admin.site.register(Photo)

