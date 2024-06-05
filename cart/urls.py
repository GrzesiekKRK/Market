from django.urls import path
from . import views

urlpatterns = [

    path('cart/', views.cart, name='market-cart'),
    path('products/<int:pk>/add-to-cart', views.add_product_to_cart_view, name='product-add-to-cart'),
    ]
