from django.contrib import admin

from .models import Order, ProductOrder


class OrderAdmin(admin.ModelAdmin):
    list_filter = ["status", "date"]
    search_fields = [
        "customer__username",
        "customer__first_name",
        "customer__last_name",
        "customer__email",
        "address",
        "postal_code",
    ]
    list_per_page = 25


class ProductOrderAdmin(admin.ModelAdmin):
    search_fields = ["product__name"]


admin.site.register(Order, OrderAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
