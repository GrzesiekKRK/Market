from django.urls import path
from .views import (
    NotificationListTemplateView,
    NotificationDetailTemplateView,
    NotificationDeleteView,
)

urlpatterns = [
    path("", NotificationListTemplateView.as_view(), name="notification"),
    path(
        "notification/<int:pk>/detail",
        NotificationDetailTemplateView.as_view(),
        name="notification-detail",
    ),
    path(
        "notification/<int:pk>/delete",
        NotificationDeleteView.as_view(),
        name="notification-delete",
    ),
]
