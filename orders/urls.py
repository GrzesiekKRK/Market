from django.urls import path
from .views import YourOrderListView, OrderDetailView, CreateOrderView, OrderDeleteView

urlpatterns = [
    path('', YourOrderListView.as_view(), name='market-customer-order'),
    path('detail/<int:pk>/', OrderDetailView.as_view(), name='market-customer-order-detail'),
    path('create_order/', CreateOrderView.create_order, name='customer-create-order'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='customer-delete-unpaid-order')
    ]
