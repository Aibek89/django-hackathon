from django.shortcuts import render
# from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from product.models import Product, Category, Review, Like, Rating
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, RatingSerializer


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category', 'owner']
    ordering_fields = ['name', 'id']
    search_fields = ['name', 'description']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        # print(pk)
        try:
            like_object, _ = Like.objects.get_or_create(owner=request.user, product_id=pk)
            like_object.like = not like_object.like
            like_object.save()
            status = 'liked'

            if like_object.like:
                return Response({'status': status})
            status = 'unlike'
            return Response({'status': status})
        except:
            return Response('Такого продукта не существует')

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        serializers = RatingSerializer(data=request)
        serializers.is_valid(raise_exception=True)
        object, _ = Rating.objects.get_or_create(product_id=pk, owner=request.user)
        object.rating = request.data['rating']
        object.save()
        return Response(request.data, status=201)

    def get_permissions(self):
        if self.action in ['list', 'retrive']:
            permissions = []

        elif self.action == 'like' or self.action == 'rating':
            permission = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated]


class ReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer




