from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product.views import CategoryView, ProductView, ReviewView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('review', ReviewView)
router.register('', ProductView)

urlpatterns = [
    path('', include(router.urls))
]