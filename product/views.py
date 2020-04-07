from rest_framework.viewsets import ModelViewSet
from .serializers import ListProductSerializer, DetailProductSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Product
from rest_framework.response import Response
from utilities.pagination import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Max, Min
from .filters import ProductFilter

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@swagger_auto_schema()
@method_decorator(cache_page(60 * 15))
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ListProductSerializer
    lookup_field = "slug"
    filter_backends = (
        filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter
    )
    search_fields = ("title",)
    filterset_class = ProductFilter
    pagination_class = DefaultPagination

    action_serializers = {
        'retrieve': DetailProductSerializer,
        'list': ListProductSerializer,
    }

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

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(ProductView, self).get_serializer_class()
