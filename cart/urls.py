from django.urls import path
from views import cart, clear_cart, decrease_quantity_of_product, increase_quantity_of_product, renew_order, add_product_to_cart_view, remove_item_from_cart
from . import views

# from views import ..., ..., ..., ..., ...

urlpatterns = [
    # TODO change things in comments below.
    path('cart/', views.cart, name='market-cart'),
    path('cart/clear/', views.clear_cart, name='remove-all-products-from-cart'), # name cart-clear
    path('cart/<int:pk>/decrease/', views.decrease_quantity_of_product, name='decrease-numbers-of-item-in-cart'), # cart-decrease-quantity-in-product
    path('cart/<int:pk>/increase/', views.increase_quantity_of_product, name='increase-numbers-of-item-in-cart'), # cart-increase-quantity-in-product
    path('cart/<int:pk>/renew/', views.renew_order, name='renew-order'), # cart/<int:pk>/renew

    path('products/<int:pk>/add-to-cart/', views.add_product_to_cart_view, name='product-add-to-cart'),
    path('products/<int:pk>/remove/', views.remove_item_from_cart, name='remove-product-from-cart'), #remove-from-cart /  product-remove-from-cart
    ]

