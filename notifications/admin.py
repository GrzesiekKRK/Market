from django.contrib import admin

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    ]


admin.site.register(Notification, NotificationAdmin)
