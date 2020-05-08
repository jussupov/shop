
import os

from django.conf import settings
from rest_framework import serializers

from category.models import Category

from .models import Photo, Product, Specification, Comment


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
            "likes",
        ]


class DetailProductSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    category = ParentCategorySerializer()
    # specification = SpecificationSerialzer(many=True)
    specification = serializers.SerializerMethodField()

    def get_specification(self, obj):
        return [
            {"parameter": d.category_spec_types.title, "value": d.value}
            for d in obj.specification.all()
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
            "likes",
        ]

        lookup_field = "slug"


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ["id", "title", "spec"]

        depth = 1


class CreateProductSerializer(serializers.HyperlinkedModelSerializer):

    images = ProductImageSerializer(source="photos_set", many=True, read_only=True)
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = [
            "title",
            "category",
            "images",
            "description",
            "box_quantity",
            "price",
            "quantity",
            "old_price",
        ]

    def create(self, validated_data):

        images_data = self.context.get("view").request.FILES
        category = Category.objects.get(slug=validated_data.get("category"))
        product = Product.objects.create(
            title=validated_data.get("title"),
            category=category,
            description=validated_data.get("description"),
            price=validated_data.get("price"),
            quantity=validated_data.get("quantity"),
            box_quantity=validated_data.get("box_quantity"),
            old_price=validated_data.get("old_price", None),
        )
        for image_data in images_data.values():

            Photo.objects.create(product=product, image=image_data)
        return product


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

# class ProductSpecificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductSpecifications
#         fields = "__all__"
