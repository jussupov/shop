from django.db import models
from utilities.models import BaseModel


class Category(BaseModel):
    parent = models.ForeignKey(
        to="self", blank=True, null=True, on_delete=models.CASCADE, related_name="child"
    )

    def __str__(self):
        if self.parent is None:
            return self.title
        return f"{self.parent} / {self.title}"
