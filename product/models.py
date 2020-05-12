from django.db import models

from category.models import Category
from utilities.models import BaseModel, TimeAndActiveModel, TimeModel
from utilities.utils import unique_slug_generator
from account.models import User
from django.core.mail import send_mail
from celery import shared_task
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.dispatch.dispatcher import receiver




class Product(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.TextField()
    price = models.PositiveIntegerField(null=False)
    quantity = models.PositiveIntegerField()
    likes = models.PositiveIntegerField(default=0)
    box_quantity = models.PositiveIntegerField(default=0)
    old_price = models.PositiveIntegerField(null=True, blank=True)
    specification = models.ManyToManyField(to='ValueSpecification')

    def __str__(self):
        return f"{self.category} / {self.title}"

    def save(self, *args, **kwargs):
        self.slug = unique_slug_generator(Product, self.title)
        super(Product, self).save(*args, **kwargs)


class Photo(TimeModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="product/images")

    def __str__(self):
        return f"{self.product} --> {self.image}"


class Specification(TimeModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category} | {self.title}"


class ValueSpecification(TimeModel):
    category_spec_types = models.ForeignKey(
        Specification, on_delete=models.CASCADE, related_name="spec"
    )
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category_spec_types} - {self.value}"


class Comment(TimeModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "comments")
    active = models.BooleanField(default=False)
    body = models.TextField()
    answer = models.TextField(null=True, blank=True, default=None)


@shared_task()
def send(subject, body, email, html_message):
    send_mail(
        subject, body, "webmaster@localhost", email, html_message=html_message,
    )

@receiver(models.signals.post_save, sender=Comment)
def answer(sender, instance, **kwargs):
    if not kwargs['created']:
        if instance.answer and len(instance.answer) != 0:
            emails = [instance.user.email]
            html_message = render_to_string("answer-comment.html", {"text":instance.answer})
            plain_message = strip_tags(html_message)
            send.delay(subject="Optovichok ответ на вопрос", body=plain_message, email=emails, html_message=html_message)
        
    
