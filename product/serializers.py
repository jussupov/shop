from rest_framework import serializers
from .models import Product, ProductImage, ProductSpecValues, CategorySpecTypes
from category.models import Category
from category.serializers import CategorySerailzer


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("slug", "title")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("image",)


class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        cat_serializer = ParentCategorySerializer(obj.category)
        return cat_serializer.data

    class Meta:
        model = Product
        fields = [
            "title",
            "slug",
            "images",
            "category",
            "description",
            "box_quantity",
            "price",
        ]
        depth = 1
        lookup_field = "slug"

