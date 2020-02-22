from django.db import models
from utilities.models import BaseModel
from transliterate import translit
from pytils.translit import slugify


class Category(BaseModel):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey(
        to="self", blank=True, null=True, on_delete=models.CASCADE, related_name="child"
    )

    class Meta:
        unique_together = (
            "title",
            "parent",
        )

    def save(self, *args, **kwargs):
        # title = translit(self.title, reversed=True)
        try:
            self.slug = f"{self.parent.slug}-{slugify(self.title)}"
        except Exception:
            self.slug = slugify(self.title)
        super(BaseModel, self).save(*args, **kwargs)

    def __str__(self):
        if self.parent is None:
            return self.title
        return f"{self.parent} / {self.title}"
