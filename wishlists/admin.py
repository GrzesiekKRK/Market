from django.contrib import admin

from .models import Wishlist


class WishlistAdmin(admin.ModelAdmin):
    list_filter = ["user"]
    ordering = ["-user"]
    list_per_page = 25


admin.site.register(Wishlist, WishlistAdmin)
