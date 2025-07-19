from django.contrib import admin

from .models import Delivery


class DeliveryAdmin(admin.ModelAdmin):
    list_filter = ["delivery_average_time"]
    search_fields = ["name", "price"]
    list_per_page = 25


admin.site.register(Delivery, DeliveryAdmin)
