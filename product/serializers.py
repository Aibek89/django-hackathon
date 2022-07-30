from rest_framework import serializers

from product.models import Category, Product, Image, Rating, Review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.parent:
            representation.pop('parent')
        return representation


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes'] = instance.like.filter(like=True).count()

        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data

        result = 0
        for rating in instance.rating.all():
            result += int(rating.rating)
        try:
            representation['rating'] = result / instance.rating.all().count()
        except ZeroDivisionError:
            pass
        return representation

    def create(self, validated_data):
        requests = self.context.get('request')
        images = requests.FILES
        product = Product.objects.create(**validated_data)

        for image in images.getlist('images'):
            Image.objects.create(product=product, image=image)

        return product



    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['likes'] = instance.likes.filter(like=True).count()
    #     representation['rating'] = 0
    #
    #     return representation


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.mail')

    class Meta:
        model = Review
        fields = '__all__'


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)
