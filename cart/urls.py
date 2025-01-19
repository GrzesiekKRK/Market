from django.urls import path

from .views import (
    CartAddView,
    CartClearView,
    CartDecreaseProductQuantityView,
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
    path("cart/<int:pk>/renew/", RenewOrderView.as_view(), name="renew-order"),
    path(
        "cart/<int:pk>/decrease/",
        CartDecreaseProductQuantityView.as_view(),
        name="cart-decrease-quantity-in-product",
    ),
    path(
        "cart/<int:pk>/incartcrease/",
        CartIncreaseProductQuantityView.as_view(),
        name="cart-increase-quantity-in-product",
    ),
    path("cart/clear/", CartClearView.as_view(), name="cart-clear"),
    path(
        "products/<int:pk>/remove/",
        CartRemoveProductView.as_view(),
        name="cart-remove-product",
    ),
]
