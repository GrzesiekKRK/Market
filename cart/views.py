from typing import Any

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from .cart import Cart

from products.models import Product
from orders.models import ProductOrder
from django.http import HttpRequest, HttpResponseRedirect


class CartTemplateView(TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        products = cart
        total_price = cart.get_sub_total_price()
        items_in_cart = len(cart)
        context["products"] = products
        context["total_price"] = total_price
        context["items_in_cart"] = items_in_cart

        return context


class CartAddView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]

        product = get_object_or_404(Product, id=pk)
        self.model.add(Cart(request), product=product, quantity=1)

        messages.success(request, f"Product {product.name} added.")
        return redirect("products")


class CartIncreaseProductQuantityView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        product = get_object_or_404(Product, id=kwargs["pk"])
        self.model.add(Cart(request), product=product, quantity=+1)

        messages.success(request, f"Product {product.name} quantity change.")
        return redirect("cart")


class CartDecreaseProductQuantityView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:

        product = get_object_or_404(Product, id=pk)
        self.model.add(Cart(request), product=product, quantity=-1)
        messages.success(request, f"Product {product.name} quantity change.")

        return redirect("cart")


class CartRemoveProductView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        product = get_object_or_404(Product, id=pk)
        self.model.remove(Cart(request), product=product)

        messages.success(request, f"Product {product.name} remove.")
        return redirect("cart")


class CartClearView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        self.model.clear(Cart(request))

        messages.success(request, f"Cart clear.")
        return redirect("cart")


class RenewOrderView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        items = ProductOrder.objects.filter(order=pk)
        for item in items:
            product = Product.objects.get(id=item.product.id)
            self.model.add(Cart(request), product=product, quantity=int(item.quantity))

        return redirect("cart")
