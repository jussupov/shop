from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
)
from .managers import UserManager
from django.dispatch.dispatcher import receiver
from django.conf import settings
from utilities.models import TimeModel
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from uuid import uuid4


class User(AbstractBaseUser):
    GENDER_CHOICES = [("М", "Мужской"), ("Ж", "Женский")]
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
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


class OTP(TimeModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uuid = models.CharField(max_length=255, unique=True)


@shared_task()
def send(subject, body, email, html_message):
    send_mail(
        subject, body, "webmaster@localhost", email, html_message=html_message,
    )


@receiver(models.signals.post_save, sender=User)
def send_code(sender, instance, **kwargs):
    if kwargs["created"]:
        uuid = uuid4()
        OTP.objects.create(user=instance, uuid=uuid)
        link = f"{settings.URL_PATH_PROJECT}/verify?key={uuid}"
        html_message = render_to_string('email-form.html', {'link': link})
        plain_message = strip_tags(html_message)
        emails = [instance.email]
        send.delay(
            subject="Регистрация на сайте",
            body=plain_message,
            email=emails,
            html_message=html_message
        )
