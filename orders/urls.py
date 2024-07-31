from django.urls import path
from .views import YourOrderListView

urlpatterns = [
    path('', YourOrderListView.as_view(), name='market-customer-order')
    ]
