from django.contrib import admin

from .models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    list_filter = ["user"]
    ordering = ["-user"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    list_per_page = 25


admin.site.register(Wishlist, WishlistAdmin)
