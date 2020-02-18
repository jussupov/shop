from rest_framework.viewsets import ModelViewSet
from .serializers import ListProductSerializer, DetailProductSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Product
from category.models import Category
from rest_framework.response import Response
from utilities.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters

from .filters import ProductFilter


@swagger_auto_schema()
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ("title",)
    filterset_class = ProductFilter
    pagination_class = DefaultPagination

    def retrieve(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        serializer_class = DetailProductSerializer(product)
        return Response(serializer_class.data)
