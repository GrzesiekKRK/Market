from django.urls import path
from .views import NotificationListView, NotificationDetailView, NotificationDeleteView

urlpatterns = [
                path('notification/', NotificationListView.as_view(), name='market-notification'),
                path('notification/<int:pk>/', NotificationDetailView.as_view(), name='market-notification-detail'),
                path('notification/<int:pk>/delete/', NotificationDeleteView.as_view(), name='market-notification-delete'),
                ]
