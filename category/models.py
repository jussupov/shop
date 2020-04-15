from django.db import models

from utilities.models import BaseModel
from utilities.utils import unique_slug_generator


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
        self.slug = unique_slug_generator(Category, self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.parent is None:
            return self.title
        return f"{self.parent} / {self.title}"
