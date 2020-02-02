from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import Product


@swagger_auto_schema()
class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
