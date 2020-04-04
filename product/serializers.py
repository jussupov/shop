from rest_framework import serializers
from .models import Product, Photo, Specification
from category.models import Category
from django.conf import settings


class ParentCategorySerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()

    def get_parent(self, obj):
        if obj.parent:
            cat = ParentCategorySerializer(obj.parent)
            return cat.data

    class Meta:
        model = Category
        fields = ("slug", "title", "parent")


# class SpecificationSerialzer(serializers.ModelSerializer):
#     parametr = serializers.SerializerMethodField()
#
#     def get_parametr(self, obj):
#         return obj.category_spec_types.title
#
#     class Meta:
#         model = ProductSpecifications
#         fields = ("value", "parametr")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("image",)


class ListProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.title

    def get_image(self, obj):
        i_qs = Photo.objects.filter(product=obj)
        if i_qs.exists():
            return f"/media/{i_qs.first().image}"
        return settings.NON_IMAGE

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "price",
            "image",
            "category",
            "box_quantity",
            "old_price",
            "likes"
        ]


class DetailProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category = ParentCategorySerializer()
    # specification = SpecificationSerialzer(many=True)
    specification = serializers.SerializerMethodField()

    def get_specification(self, obj):
        return [
            {
                "parameter": d.category_spec_types.title,
                "value": d.value
            } for d in obj.specification.all()
        ]

    def get_images(self, obj):
        i_qs = Photo.objects.filter(product=obj)
        if len(i_qs) == 0:
            return {"image": settings.NON_IMAGE}
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
            "old_price",
            "specification",
            "likes"
        ]

        lookup_field = "slug"

# class ProductSpecificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductSpecifications
#         fields = "__all__"
