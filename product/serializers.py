from rest_framework import serializers
from .models import Product, Photo, Specification, ProductSpecifications
from category.models import Category
from category.serializers import CategorySerializer
from django.db.models import Max, Min


class ParentCategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        if obj.parent:
            cat = ParentCategorySerializer(obj.parent)
            return cat.data

    class Meta:
        model = Category
        fields = ("slug", "title", "parent")


class SpecificationSerialzer(serializers.ModelSerializer):
    parametr = serializers.SerializerMethodField()

    def get_parametr(self, obj):
        return obj.category_spec_types.title

    class Meta:
        model = ProductSpecifications
        fields = ("value", "parametr")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("image",)


class ListProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.title

    def get_images(self, obj):
        i_qs = Photo.objects.filter(product=obj)
        if len(i_qs) == 0:
            return None
        return ProductImageSerializer(i_qs, many=True).data

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "images",
            "category",
            "box_quantity",
            "old_price",
        ]





class DetailProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category = ParentCategorySerializer()
    specification = SpecificationSerialzer(many=True)

    def get_images(self, obj):
        i_qs = Photo.objects.filter(product=obj)
        if len(i_qs) == 0:
            return None
        return ProductImageSerializer(i_qs, many=True).data

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "category",
            "images",
            "description",
            "box_quantity",
            "price",
            "quantity",
            "specification",
            "old_price",
        ]

        lookup_field = "slug"
