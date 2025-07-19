from django.contrib import admin

from .models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    search_fields = [
        "vendor__username",
        "vendor__first_name",
        "vendor__last_name",
        "vendor__email",
        "products__name",
    ]
    list_filter = ["vendor__is_active", "vendor__date_joined"]
    list_per_page = 25


admin.site.register(Inventory, InventoryAdmin)
