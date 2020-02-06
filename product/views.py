from rest_framework.viewsets import ModelViewSet
from .serializers import ListProductSerializer, DetailProductSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Product
from category.models import Category
from rest_framework.response import Response
from utilities.pagination import DefaultPagination

from django.shortcuts import get_object_or_404


@swagger_auto_schema()
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer
    lookup_field = "slug"
    pagination_class = DefaultPagination

    def list(self, request):
        if "category" in request.query_params:
            cat_name = request.query_params.get("category")
            try:
                cat = (
                    Category.objects.get(slug=cat_name)
                    .child.all()
                    .values_list("id", flat=True)
                )
                products = self.paginate_queryset(
                    Product.objects.filter(category__id__in=cat)
                )
            except Exception:
                return Response({"detail": "Not found"})

        else:
            products = self.paginate_queryset(Product.objects.all())
        serializer_class = ListProductSerializer(products, many=True)
        return self.get_paginated_response(serializer_class.data)

    def retrieve(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        serializer_class = DetailProductSerializer(product)
        return Response(serializer_class.data)
