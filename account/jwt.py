
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from cart.models import Cart, CartItem

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        cart, _ = Cart.objects.get_or_create(user=user,
                                             is_active=True)
        count = CartItem.objects.filter(cart=cart).count()

        token["email"] = user.email
        token["birth_day"] = str(user.birth_day)
        token["first_name"] = user.first_name
        token["gender"] = user.gender
        token["count"] = count
        token["last_name"] = user.last_name

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
