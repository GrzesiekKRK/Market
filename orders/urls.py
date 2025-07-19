from django.urls import path

from .views import (
    CreateOrderTemplateView,
    OrderDeleteUnpaidView,
    OrderDetailTemplateView,
    OrderListTemplateView,
)

urlpatterns = [
    path("", OrderListTemplateView.as_view(), name="customer-order"),
    path(
        "<int:pk>/detail/",
        OrderDetailTemplateView.as_view(),
        name="customer-order-detail",
    ),
    path(
        "<int:pk>/delete",
        OrderDeleteUnpaidView.as_view(),
        name="customer-delete-unpaid-order",
    ),
    path(
        "create-order/", CreateOrderTemplateView.as_view(), name="customer-create-order"
    ),
]
