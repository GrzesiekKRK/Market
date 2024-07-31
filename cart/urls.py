from django.urls import path
from . import views

urlpatterns = [

    path('cart/', views.cart, name='market-cart'),
    path('products/<int:pk>/add-to-cart/', views.add_product_to_cart_view, name='product-add-to-cart'),
    path('products/<int:pk>/remove/', views.remove_item_from_cart, name='remove-product-from-cart'),
    path('cart/clear/', views.clear_cart, name='remove-all-products-from-cart'),
    path('cart/<int:pk>/decrease/', views.decrease_quantity_of_product, name='decrease-numbers-of-item-in-cart'),
    path('cart/<int:pk>/increase/', views.increase_quantity_of_product, name='increase-numbers-of-item-in-cart'),
    ]

