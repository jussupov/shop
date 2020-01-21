from rest_framework import serializers
from .models import Category


# For the: [ list ]
class BaseCategorySerailzer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("title", "slug")
        lookup_field = "slug"


# For the: [ retrieve ]
class CategorySerailzer(BaseCategorySerailzer):
    def get_fields(self):
        fields = super(CategorySerailzer, self).get_fields()
        fields["child"] = CategorySerailzer(many=True)
        return fields
