from django.urls import path

from .views import (
    CartAddView,
    CartClearView,
    CartDecreaseProductQuantityView,
    CartDeliveryView,
    CartIncreaseProductQuantityView,
    CartRemoveProductView,
    CartTemplateView,
    RenewOrderView,
)

urlpatterns = [
    path("cart/", CartTemplateView.as_view(), name="cart"),
    path(
        "products/<int:pk>/add-to-cart/",
        CartAddView.as_view(),
        name="product-add-to-cart",
    ),
    path("cart/orders/<int:pk>/renew/", RenewOrderView.as_view(), name="renew-order"),
    path(
        "cart/products/<int:pk>/decrease-product-quantity/",
        CartDecreaseProductQuantityView.as_view(),
        name="cart-decrease-quantity-in-product",
    ),
    path(
        "cart/products/<int:pk>/increase-product-quantity/",
        CartIncreaseProductQuantityView.as_view(),
        name="cart-increase-quantity-in-product",
    ),
    path(
        "cart/products/update-delivery/",
        CartDeliveryView.as_view(),
        name="cart-update-delivery",
    ),
    path("cart/products/clear/", CartClearView.as_view(), name="cart-clear"),
    path(
        "cart/products/<int:pk>/remove/",
        CartRemoveProductView.as_view(),
        name="cart-remove-product",
    ),
]
