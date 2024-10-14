from django.urls import path
from .views import WishListTemplateView

urlpatterns = [
    path('add_product/<int:pk>/', WishListTemplateView.add_wish, name='add-to-wishlist'),
    path('remove/<int:pk>/', WishListTemplateView.remove_from_wishlist, name='wishlist-remove'),
    path('', WishListTemplateView.as_view(), name='wishlist'),
    ]
