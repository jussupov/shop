from django.urls import path, include
from .views import verify

urlpatterns = [
    path("verify", verify),
]
