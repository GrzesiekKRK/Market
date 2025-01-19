from django.contrib import admin

from .models import Order, ProductOrder

admin.site.register(Order)
admin.site.register(ProductOrder)
