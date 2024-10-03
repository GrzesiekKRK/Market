from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import View
from .cart import Cart

from products.models import Product
from orders.models import ProductOrder
from icecream import ic
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect


def cart(request: HttpRequest) -> HttpResponse: # TODO Refactor to TemplateView
    """Renders Cart """
    cart = Cart(request)
    
    products = cart
    total_price = cart.get_sub_total_price()
    items_in_cart = cart.__len__() # TODO len(cart)

    return render(request, 'cart/cart.html', {'products': products, 'total_price': total_price, 'items_in_cart': items_in_cart})


def add_product_to_cart_view(request: HttpRequest, pk: int, quantity: int = 1) -> HttpResponseRedirect: # TODO View
    cart = Cart(request)

    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        cart.add(product=product, quantity=quantity)

    messages.success(request, f'Product {product.name} added.')
    return redirect('market-products')


def increase_quantity_of_product(request: HttpRequest, pk: int) -> HttpResponseRedirect: # TODO View
    cart = Cart(request)

    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        cart.add(product=product, quantity=+1)
        messages.success(request, f'Product {product.name} quantity change.')

    return redirect('market-cart')


def decrease_quantity_of_product(request: HttpRequest, pk: int) -> HttpResponseRedirect: # TODO View
    cart = Cart(request)

    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        cart.add(product=product, quantity=-1)
        messages.success(request, f'Product {product.name} quantity change.')

    return redirect('market-cart')


def remove_item_from_cart(request: HttpRequest, pk: int) -> HttpResponseRedirect: # TODO View
    cart = Cart(request)

    if request.method == 'POST':
        product = get_object_or_404(Product, id=pk)
        cart.remove(product=product)
        messages.success(request, f'Product {product.name} remove.')

    return redirect('market-cart')


def clear_cart(request: HttpRequest) -> HttpResponseRedirect: # TODO View post
    cart = Cart(request)

    cart.clear()
    messages.success(request, f'Cart clear.')
    return redirect('market-cart')


def renew_order(request: HttpRequest, pk: int) -> HttpResponseRedirect: # TODO View
    if request.method == 'POST':
        items = ProductOrder.objects.filter(order=pk)
        for item in items:
            product = Product.objects.get(id=item.product.id)
            add_product_to_cart_view(request, pk=product.id, quantity=int(item.quantity))
        return redirect('market-cart')


# class RenewOrderView(View):
#     def post(self, request, pk):
#         items = ProductOrder.objects.filter(order=pk)
#         for item in items:
#             product = Product.objects.get(id=item.product.id)
#             add_product_to_cart_view(request, pk=product.id, quantity=int(item.quantity))
#         return redirect('market-cart')
