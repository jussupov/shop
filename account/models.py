from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    AbstractUser,
    BaseUserManager,
    PermissionsMixin,
)
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager
from django.dispatch.dispatcher import receiver


class User(AbstractBaseUser):
    GENDER_CHOICES = [("М", "Мужской"), ("Ж", "Женский")]
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    birth_day = models.DateField()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "birth_day",
        "gender",
        "first_name",
        "last_name",
    ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

