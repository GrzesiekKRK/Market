from django.contrib import admin
from .models import Category, Product, Department


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Department)
