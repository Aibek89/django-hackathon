from django.contrib import admin

from product.models import Product, Category, Review, Image, Rating

admin.site.register(Product)
admin.site.register(Category)

admin.site.register(Review)
admin.site.register(Image)
admin.site.register(Rating)
