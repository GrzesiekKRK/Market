from django.urls import path
from .views import OrderListTemplateView, OrderDetailTemplateView, CreateOrderClass, OrderDeleteView

urlpatterns = [
    path('', OrderListTemplateView.as_view(), name='market-customer-order'),
    path('detail/<int:pk>/', OrderDetailTemplateView.as_view(), name='market-customer-order-detail'),
    path('create_order/', CreateOrderClass.create_order, name='customer-create-order'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='customer-delete-unpaid-order')
    ]
