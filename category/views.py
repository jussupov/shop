from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerailzer, BaseCategorySerailzer
from .models import Category
from rest_framework.response import Response
from rest_framework.decorators import action
from utilities.permissions import IsAdminOrReadOnly
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema()
class CategoryView(ModelViewSet):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = BaseCategorySerailzer
    lookup_field = "slug"
    permission_classes = (IsAdminOrReadOnly,)

    def retrieve(self, request, slug=None):
        queryset = Category.objects.filter(parent__slug=slug)
        serializer = CategorySerailzer(queryset, many=True)
        return Response(serializer.data)
