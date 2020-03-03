from django.urls import path, include
from .views import verify, TokenCreateView, TokenDestroyView

urlpatterns = [
    path("verify", verify),
    path("api/auth/login", TokenCreateView.as_view()),
    path("api/auth/logout", TokenDestroyView.as_view()),
]
