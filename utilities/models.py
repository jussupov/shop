from django.db import models
from pytils.translit import slugify


class TimeModel(models.Model):
    class Meta:
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


class BaseModel(TimeModel):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)


class TimeAndActiveModel(TimeModel):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True)

