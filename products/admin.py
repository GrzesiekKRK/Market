from django.contrib import admin

from .models import Category, Product, ProductDimension, ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_filter = ["name"]
    ordering = ["-name"]
    search_fields = ["name", "price"]
    list_per_page = 25


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductDimension)
