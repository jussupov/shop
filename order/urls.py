from .views import create_payment
from django.urls import path, include


urlpatterns = [path("payment", create_payment)]
