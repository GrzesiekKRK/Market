from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = ["role", "id", "pesel", "email"]
    search_fields = ("role",)


admin.site.register(CustomUser, CustomUserAdmin)
