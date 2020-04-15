from django.urls import path, include
from .views import verify, UserView

urlpatterns = [path("verify", verify), path("register", UserView.as_view())]
