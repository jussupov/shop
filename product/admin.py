from django.contrib import admin
from .models import Product, Specification, Photo, ValueSpecification


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Specification)
admin.site.register(Photo)
admin.site.register(ValueSpecification)
