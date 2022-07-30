from django.contrib import admin

from product.models import Product, Category, Review, Image, Rating


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 4


class ProsuctAdmn(admin.ModelAdmin):
    inlines = [ImageInAdmin]


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Image)
admin.site.register(Rating)
