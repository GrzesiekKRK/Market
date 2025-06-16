from django.contrib import admin

from .models import Category, Product, ProductDimension, ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    ordering = ["-name"]
    search_fields = ["name", "price", "category__name"]
    list_per_page = 25


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    ordering = ["-name"]
    search_fields = ["name"]
    list_per_page = 25


class ProductDimensionAdmin(admin.ModelAdmin):
    list_filter = ["product"]
    search_fields = ["product__name"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductDimension, ProductDimensionAdmin)
