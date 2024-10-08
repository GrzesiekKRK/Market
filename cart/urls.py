from django.urls import path
from .views import CartTemplateView, CartAddView, CartIncreaseProductQuantityView, CartDecreaseProductQuantityView, CartRemoveProductView, RenewOrderView, CartClearView


urlpatterns = [
    # TODO change things in comments below.
    path('cart/', CartTemplateView.as_view(), name='market-cart'),
    path('cart/clear/', CartClearView.as_view(), name='remove-all-products-from-cart'), # name cart-clear
    path('cart/<int:pk>/decrease/', CartDecreaseProductQuantityView.as_view(), name='decrease-numbers-of-item-in-cart'), # cart-decrease-quantity-in-product
    path('cart/<int:pk>/increase/', CartIncreaseProductQuantityView.as_view(), name='increase-numbers-of-item-in-cart'), # cart-increase-quantity-in-product
    path('cart/<int:pk>/renew/', RenewOrderView.as_view(), name='renew-order'), # cart/<int:pk>/renew

    path('products/<int:pk>/add-to-cart/', CartAddView.as_view(), name='product-add-to-cart'),
    path('products/<int:pk>/remove/', CartRemoveProductView.as_view(), name='remove-product-from-cart'), #remove-from-cart /  product-remove-from-cart
    ]

