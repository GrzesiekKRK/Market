from django.urls import path
from .views import VendorInventoryListView

urlpatterns = [
    path('', VendorInventoryListView.as_view(), name='market-vendor-inventory')
    ]
