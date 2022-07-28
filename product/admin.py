from django.contrib import admin

from product.models import Product, Category, Reviews, Image, Rating

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Reviews)
admin.site.register(Image)
admin.site.register(Rating)
