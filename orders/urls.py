from django.urls import path
from .views import (
    CreateOrderTemplateView,
    OrderListTemplateView,
    OrderDetailTemplateView,
    OrderDeleteUnpaidView,
)

urlpatterns = [
    path("", OrderListTemplateView.as_view(), name="customer-order"),
    path(
        "detail/<int:pk>/",
        OrderDetailTemplateView.as_view(),
        name="customer-order-detail",
    ),
    path(
        "delete/<int:pk>/",
        OrderDeleteUnpaidView.as_view(),
        name="customer-delete-unpaid-order",
    ),
    path(
        "create_order/", CreateOrderTemplateView.as_view(), name="customer-create-order"
    ),
]
