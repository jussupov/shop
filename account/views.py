from django.shortcuts import render, get_object_or_404
from .models import OTP
from django.conf import settings
from django.utils import timezone


def verify(request):
    key = request.GET.get("key")
    if key is not None:
        otp = get_object_or_404(OTP, uuid=key)

        diff = timezone.now() - otp.created
        diff = diff.total_seconds()

        if diff > settings.DIFF_SECONDS:
            return render(request, "verify/index.html", {"status": False})

        user = otp.user
        user.is_active = True
        user.save()
        otp.delete()
        return render(request, "verify/index.html", {"status": True})

    return render(request, "verify/404.html")
