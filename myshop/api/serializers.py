from rest_framework import serializers
from products.models import Product, Category, SubCategory, Cart


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'slug', 'image']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'subcategories']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    subcategory = serializers.StringRelatedField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'category', 'subcategory', 'price', 'images']

    def get_images(self, obj):
        images = {
            'small': obj.image_small.url,
            'medium': obj.image_medium.url,
            'large': obj.image_large.url
        }
        return images


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
