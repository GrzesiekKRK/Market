from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "last_name",
        "email",
        "role",
        "is_active",
        "date_joined",
    ]
    list_filter = ["role", "is_active", "date_joined"]
    ordering = ["-date_joined"]
    search_fields = ["email", "username", "first_name", "last_name"]
    list_per_page = 25


admin.site.register(CustomUser, CustomUserAdmin)
