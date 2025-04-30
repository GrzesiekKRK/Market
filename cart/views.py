from typing import Any

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View

from deliveries.models import Delivery
from orders.models import ProductOrder
from products.models import Product

from .cart import Cart


class CartTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """Generates the context for the cart page, including the cart contents and total price of cart.

        Arguments:
                kwargs: Additional keyword arguments for context generation.

        Returns:
                A dictionary containing the cart products, total price, and item count.
        """
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)

        products = cart
        filtered_delivery_methods = (
            Delivery.objects.all()
        )  # TODO filtraż delivery metod po wymiarach
        items_total_price = cart.get_products_sub_total_price()
        selected_delivery_method = cart.get_delivery_method(self.request)
        total_price = items_total_price + selected_delivery_method.price

        items_in_cart = len(cart)
        context["products"] = products
        context["total_price"] = total_price
        context["items_in_cart"] = items_in_cart
        context["delivery_methods"] = filtered_delivery_methods
        context["selected_delivery_id"] = selected_delivery_method.id

        return context


class CartAddView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """Handles adding a product to the cart.

        Arguments:
            request: The HTTP request object.
            kwargs: Contains the product ID (`pk`) to be added to the cart.

        Returns:
            A redirect to the products page with a success message.
        """
        pk = kwargs["pk"]

        product = get_object_or_404(Product, id=pk)
        self.model.add(Cart(request), product=product, quantity=1)

        messages.success(request, f"Product {product.name} added.")
        return redirect("products")


class CartIncreaseProductQuantityView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        """Handles increasing the quantity of a product in the cart.

        Arguments:
            request: The HTTP request object.
            kwargs: Contains the product ID (`pk`) whose quantity will be increased.

        Returns:
            A redirect to the cart page with a success message.
        """
        product = get_object_or_404(Product, id=kwargs["pk"])
        self.model.add(Cart(request), product=product, quantity=+1)

        messages.success(request, f"Product {product.name} quantity change.")
        return redirect("cart")


class CartDecreaseProductQuantityView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        """Handles decreasing the quantity of a product in the cart.

        Arguments:
            request: The HTTP request object.
            pk: The product ID (`pk`) whose quantity will be decreased.

        Returns:
            A redirect to the cart page with a success message.
        """

        product = get_object_or_404(Product, id=pk)
        self.model.add(Cart(request), product=product, quantity=-1)
        messages.success(request, f"Product {product.name} quantity change.")

        return redirect("cart")


class CartRemoveProductView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        """Handles removing a product from the cart.

        Arguments:
            request: The HTTP request object.
            pk: The product ID (`pk`) to be removed from the cart.

        Returns:
            A redirect to the cart page with a success message.
        """
        product = get_object_or_404(Product, id=pk)
        self.model.remove(Cart(request), product=product)

        messages.success(request, f"Product {product.name} remove.")
        return redirect("cart")


class CartClearView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest) -> HttpResponseRedirect:
        """Handles clearing the entire cart.

        Arguments:
            request: The HTTP request object.

        Returns:
            A redirect to the cart page with a success message.
        """
        self.model.clear(Cart(request))

        messages.success(request, "Cart clear.")
        return redirect("cart")


class CartDeliveryView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request):
        """
        Update the cart's delivery method and recalculate total price.
        """
        if request.method == "POST":
            delivery_id = request.POST.get("delivery_method")

            request.session["selected_delivery_id"] = delivery_id

        return redirect("cart")


class RenewOrderView(LoginRequiredMixin, View):
    model = Cart

    def post(self, request: HttpRequest, pk: int) -> HttpResponseRedirect:
        """Handles renewing an order by adding its products to the cart.

        Arguments:
            request: The HTTP request object.
            pk: The order ID (`pk`) to renew.

        Returns:
            A redirect to the cart page after adding the products from the order.
        """
        items = ProductOrder.objects.filter(order=pk)
        for item in items:
            product = Product.objects.get(id=item.product.id)
            self.model.add(Cart(request), product=product, quantity=int(item.quantity))

        return redirect("cart")
