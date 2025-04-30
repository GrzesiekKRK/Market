from django.urls import path

from .views import InventoryListTemplateView

urlpatterns = [
    path("", InventoryListTemplateView.as_view(), name="vendor-inventory"),
]
