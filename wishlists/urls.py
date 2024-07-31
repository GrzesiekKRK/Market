from django.urls import path
from .views import MyWishlistView

urlpatterns = [
    path('add_product/<int:pk>/', MyWishlistView.add_wish, name='market-add_to_wishlist'),
    path('remove/<int:pk>/', MyWishlistView.remove_from_wishlist, name='market-wishlist-remove'),
    path('', MyWishlistView.as_view(), name='market-wishlist'),
    ]
