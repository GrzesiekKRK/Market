from django.urls import path
from .views import WishListTemplateView

urlpatterns = [
    path('add_product/<int:pk>/', WishListTemplateView.add_wish, name='market-add_to_wishlist'),
    path('remove/<int:pk>/', WishListTemplateView.remove_from_wishlist, name='market-wishlist-remove'),
    path('', WishListTemplateView.as_view(), name='market-wishlist'),
    ]
