from rest_framework.viewsets import ModelViewSet
from .models import Cart, CartItem
from .serialzers import CartItemSerialzer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# TODO is Authenticated by token
class CartView(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerialzer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            queryset = CartItem.objects.filter(cart=cart)
            serializer_class = CartItemSerialzer(queryset, many=True)
            return Response(serializer_class.data)
        except Exception:
            return Response([])

