from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .cart import Cart
from products.models import Product


def add_product_to_cart_view(request, pk):
    cart = Cart(request)

    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        cart.add(product=product)

    messages.success(request, f'Product {product.name} added.')
    return redirect('market-shop')


def cart(request):
    cart = Cart(request)
    items = cart
    total_price = cart.get_sub_total_price()
    return render(request, 'cart/cart.html', {'items': items, 'total_price': total_price})



