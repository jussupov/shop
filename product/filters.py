from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from .models import Product
from category.models import Category


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    max_box_quantity = filters.NumberFilter(
        field_name="box_quantity", lookup_expr="lte"
    )
    min_box_quantity = filters.NumberFilter(
        field_name="box_quantity", lookup_expr="gte"
    )
    category = filters.CharFilter(field_name="category__slug", method="filter_category")

    def filter_category(self, queryset, name, value):
        category = get_object_or_404(Category, slug=value)
        if category.child:
            products = Product.objects.none()
            for cat in category.child.all():
                products |= Product.objects.filter(category__slug=cat.slug)
            return products
        return Product.objects.filter(category__slug=value)

    class Meta:
        model = Product
        fields = ["price", "category", "box_quantity"]
