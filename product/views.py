from rest_framework.viewsets import ModelViewSet
from .serializers import ListProductSerializer, DetailProductSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Product, Specification
from rest_framework.response import Response
from utilities.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters
from django.db.models import Max, Min
from .filters import ProductFilter


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@swagger_auto_schema()
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter)
    search_fields = ("title",)
    filterset_class = ProductFilter
    pagination_class = DefaultPagination

    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data
            category = request.GET.get('category')
            if category:
                data.update(
                    Product.objects.filter(category__slug=category).aggregate(
                        maxPrice=Max('price'),
                        minPrice=Min('price'),
                        minBoxQuantity=Max('box_quantity'),
                        maxBoxQuantitiy=Min('box_quantity')
                    )
                )

            else:
                data.update(
                    Product.objects.aggregate(
                        maxPrice=Max('price'),
                        minPrice=Min('price'),
                        minBoxQuantity=Max('box_quantity'),
                        maxBoxQuantitiy=Min('box_quantity')
                    )
                )

            return Response(data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

