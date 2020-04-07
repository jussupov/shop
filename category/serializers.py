from rest_framework import serializers
from .models import Category


class BaseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("title", "slug")
        lookup_field = "slug"


class CategorySerializer(BaseCategorySerializer):
    def get_fields(self):
        fields = super(CategorySerializer, self).get_fields()
        fields["child"] = CategorySerializer(many=True)
        return fields
