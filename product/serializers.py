from rest_framework import serializers

from product.models import Product, Category, Image


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.parent:
            representation.pop('parent')
        return representation


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        requests = self.context.get('request')
        image = requests.FILES
        for i in range(10):
            product = Product.objects.create(**validated_data)
        print(image)
        for image in image.getlist('image'):
            Image.objects.create(product=product, image=image)

        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['like'] = instance.likes.filter(like=True).count()
        representation['rating'] = 0
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField()


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        models = Image
        fields = ['image']


class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(required=True)

