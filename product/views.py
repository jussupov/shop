from django.db.models import Max, Min
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from utilities.pagination import DefaultPagination

from . import serializers as product_serializer
from .filters import ProductFilter
from .models import Product, Specification, Comment


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

@swagger_auto_schema()
class CommentView(ListCreateAPIView):
    lookup_field = "product__slug"
    serializer_class = product_serializer.CommentSerializer
    queryset = Comment.objects.all()



@swagger_auto_schema()
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = product_serializer.ListProductSerializer
    lookup_field = "slug"
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    search_fields = ("title",)
    filterset_class = ProductFilter
    pagination_class = DefaultPagination

    action_serializers = {
        "retrieve": product_serializer.DetailProductSerializer,
        "list": product_serializer.ListProductSerializer,
        "create": product_serializer.CreateProductSerializer,
    }

    @method_decorator(cache_page(60 * 15))
    def list(self, request, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data
            category = request.GET.get("category")
            if category:
                data.update(
                    Product.objects.filter(category__slug=category).aggregate(
                        maxPrice=Max("price"),
                        minPrice=Min("price"),
                        minBoxQuantity=Max("box_quantity"),
                        maxBoxQuantitiy=Min("box_quantity"),
                    )
                )

            else:
                data.update(
                    Product.objects.aggregate(
                        maxPrice=Max("price"),
                        minPrice=Min("price"),
                        minBoxQuantity=Max("box_quantity"),
                        maxBoxQuantitiy=Min("box_quantity"),
                    )
                )

            return Response(data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def comments(self, request):
        slug = request.GET.get("product")
        if slug:
            queryset = Comment.objects.filter(product__slug=slug).values("id", "body", "user__email", "answer")
            serializer = product_serializer.CommentSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response({"message": "Пустой"})

    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def comment(self, request):
        try:
            slug = request.GET.get("product")
            product = Product.objects.get(slug=slug)
            
            data = {
                "user":request.user,
                "product":product,
                "body":request.data['body']
            }

            Comment.objects.create(**data)
            print("created")

            return Response({"message": "Ok"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "Ошибка"}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=["GET"])
    def specification(self, request):
        slug = request.GET.get("category")
        if slug:
            print(slug)
            queryset = Specification.objects.filter(category__slug=slug)
            serializer = product_serializer.SpecificationSerializer(queryset)
            return Response(serializer.data)
        return Response({"message": "Пустой"})

    def get_serializer_class(self):
        if hasattr(self, "action_serializers"):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(ProductView, self).get_serializer_class()
