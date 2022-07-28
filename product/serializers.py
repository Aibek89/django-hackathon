from rest_framework import serializers

from product.models import Product, Category, Image


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        models = Image
        fields = ['image']

