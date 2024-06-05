from django.urls import path
from . import views

urlpatterns = [

    path('products/<int:pk>/add-to-cart', views.add_product_to_cart_view, name='product-add-to-cart'),
    ]
