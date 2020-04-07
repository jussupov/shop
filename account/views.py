from django.shortcuts import render, get_object_or_404
from .models import OTP
import shop.settings as settings
from django.utils import timezone
from djoser import signals, utils
from djoser.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import views
from rest_framework import status
from cart.models import CartItem, Cart


def verify(request):
    key = request.GET.get("key")
    if key is not None:
        otp = get_object_or_404(OTP, uuid=key)

        diff = timezone.now() - otp.created
        diff = diff.total_seconds()

        if diff > 360:
            return render(request, "verify/index.html", {"status": False})

        user = otp.user
        user.is_active = True
        user.save()
        otp.delete()
        return render(request, "verify/index.html", {"status": True})

    return render(request, "verify/404.html")


class TokenCreateView(utils.ActionViewMixin, generics.GenericAPIView):

    serializer_class = settings.SERIALIZERS.token_create

    def _action(self, serializer):
        token = utils.login_user(self.request, serializer.user)
        token_serializer_class = settings.SERIALIZERS.token
        data = token_serializer_class(token).data
        user_data = settings.SERIALIZERS.user(token.user)
        data.update(user_data.data)
        cart, _ = Cart.objects.get_or_create(user=token.user, is_active=True)
        count = CartItem.objects.filter(cart=cart).count()
        data.update({"count": count})
        return Response(data=data, status=status.HTTP_200_OK)


class TokenDestroyView(views.APIView):
    """
    Use this endpoint to logout user (remove user authentication token).
    """

    permission_classes = settings.PERMISSIONS.token_destroy

    def post(self, request):
        utils.logout_user(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
