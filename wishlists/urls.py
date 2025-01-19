from django.urls import path

from .views import (
    WishlistAddProductView,
    WishlistRemoveProductView,
    WishListTemplateView,
)

urlpatterns = [
    path("", WishListTemplateView.as_view(), name="wishlist"),
    path(
        "add_product/<int:pk>/",
        WishlistAddProductView.as_view(),
        name="add-to-wishlist",
    ),
    path(
        "remove/<int:pk>/", WishlistRemoveProductView.as_view(), name="wishlist-remove"
    ),
]
