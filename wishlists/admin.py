from django.contrib import admin

from .models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    ]
    list_per_page = 25


admin.site.register(Wishlist, WishlistAdmin)
