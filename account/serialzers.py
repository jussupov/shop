from .models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "gender", "birth_day", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        email = validated_data["email"]
        first_name = validated_data["first_name"]
        last_name = validated_data["last_name"]
        gender = validated_data["gender"]
        birth_day = validated_data["birth_day"]
        password = validated_data["password"]
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "Email addresses must be unique."}
            )
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            birth_day=birth_day,
        )
        user.set_password(password)
        user.save()
        return user
