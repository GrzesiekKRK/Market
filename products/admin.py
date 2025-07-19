from django.contrib import admin

from .models import Category, Product, ProductDimension, ProductImage


class ProductAdmin(admin.ModelAdmin):
    search_fields = ["name", "price", "category__name"]
    list_per_page = 25


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    ordering = ["-name"]
    search_fields = ["name"]
    list_per_page = 25


class ProductDimensionAdmin(admin.ModelAdmin):
    search_fields = ["product__name"]
    list_per_page = 25


class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ["product__name"]
    list_per_page = 25


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(ProductDimension, ProductDimensionAdmin)
