from django.urls import path

from .views import (
    WishlistAddProductView,
    WishlistRemoveProductView,
    WishListTemplateView,
)

urlpatterns = [
    path("", WishListTemplateView.as_view(), name="wishlist"),
    path(
        "<int:pk>/add",
        WishlistAddProductView.as_view(),
        name="add-to-wishlist",
    ),
    path(
        "<int:pk>/remove", WishlistRemoveProductView.as_view(), name="wishlist-remove"
    ),
]
