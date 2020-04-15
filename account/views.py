
from django.shortcuts import render, get_object_or_404
from .models import OTP
import shop.settings as settings
from django.utils import timezone
from cart.models import CartItem, Cart
from rest_framework import views, status, response 
from rest_framework_simplejwt.tokens import RefreshToken
from .serialzers import UserCreateSerializer



class UserView(views.APIView):

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        result = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return response.Response(result, status=status.HTTP_201_CREATED)



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


