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

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        for i in range(10):
            product = Product.objects.create(**validated_data)
        print(images)
        for image in images.getlist('images'):
            Image.objects.create(product=product, image=image)


class ReviewsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        models = Image
        fields = ['image']

