from django.urls import path
from .views import InventoryListTemplateView

urlpatterns = [
    path('', InventoryListTemplateView.as_view(), name='market-vendor-inventory')
    ]
