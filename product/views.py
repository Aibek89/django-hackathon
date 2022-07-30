from django.shortcuts import render

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from product.models import Category, Product, Like, Rating, Review
from product.permissions import CustomIsAdmin
from product.serializers import CategorySerializer, ProductSerializer, RatingSerializer, ReviewSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LargeResultsSetPagination
    filterset_fields = ['category']
    permission_classes = [CustomIsAdmin]


class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['category']
    ordering_fields = ['name']
    search_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['POST'])
    def rating(self, request, pk, *args, **kwargs):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj, _ = Rating.objects.get_or_create(product_id=pk, owner=request.user)
        obj.rating = request.data['rating']
        obj.save()
        return Response(request.data, status=201)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk, *args, **kwargs):
        try:
            like_object, _ = Like.objects.get_or_create(owner=request.user, product_id=pk)
            like_object.like = not like_object.like
            like_object.save()
            status = 'like'

            if like_object.like:
                return Response('Like')
            return Response('Unlike')
        except:
            return Response('Такого продукта не существует')


class ReviewView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)





