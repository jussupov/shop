from django.db import models
from transliterate import translit
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=255, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        title = translit(self.title, reversed=True)
        self.slug = slugify(title)
        super(BaseModel, self).save(*args, **kwargs)
