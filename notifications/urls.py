from django.urls import path

from .views import (
    NotificationDeleteView,
    NotificationDetailTemplateView,
    NotificationListTemplateView,
)

urlpatterns = [
    path("", NotificationListTemplateView.as_view(), name="notification"),
    path(
        "<int:pk>/detail",
        NotificationDetailTemplateView.as_view(),
        name="notification-detail",
    ),
    path(
        "<int:pk>/delete",
        NotificationDeleteView.as_view(),
        name="notification-delete",
    ),
]
