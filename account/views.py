from django.shortcuts import render, get_object_or_404
from .models import OTP
from django.conf import settings


def verify(request):
    key = request.GET.get("key")
    if key is not None:
        otp = get_object_or_404(OTP, uuid=key)
        user = otp.user
        user.is_active = True
        user.save()
        otp.delete()

    return render(request, "verify/index.html")
