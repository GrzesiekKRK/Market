from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, TemplateView

from cart.cart import Cart
from payments.services import stripe_checkout_session
from products.models import Product
from users.models import CustomUser

from .models import Order, ProductOrder


class CreateOrderTemplateView(LoginRequiredMixin, TemplateView):
    """Handles the creation of an order by the logged-in customer."""

    model = Order
    template_name = "orders/create_order.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Creates an order based on the current user's cart, saves the order, and creates
        ProductOrder instances for each product in the cart. Then, redirects the user to
        the order confirmation page with the order details.

        Args:
            request (HttpRequest): The HTTP request object containing the user's data,
                                    including the cart and session information.

        Returns:
            HttpResponse: The HTTP response rendering the order creation page with the order details.
        """

        context = {}

        user = request.user
        customer = CustomUser.objects.get(id=user.id)
        address = customer.address
        postal_code = customer.postal_code

        cart = Cart(request)
        products = cart
        order_quantity = len(cart)
        total_price = cart.get_sub_total_price()
        order_before_payment = self.model(
            customer=customer,
            order_quantity=order_quantity,
            address=address,
            postal_code=postal_code,
            total_price=total_price,
        )

        order_before_payment.save()
        for product in products:
            item = Product.objects.get(id=product["product"].id)
            if item.is_sale:
                price = item.sale_price
            else:
                price = item.price
            order_product = ProductOrder(
                product=item,
                order=order_before_payment,
                quantity=product["quantity"],
                price=price,
            )
            order_product.save()

        order_products = ProductOrder.objects.filter(order=order_before_payment.id)

        if len(products) == order_quantity:
            cart.clear()

        context["customer"] = customer
        context["address"] = address
        context["postal_code"] = postal_code
        context["order_number"] = order_before_payment.id
        context["order_quantity"] = order_quantity
        context["total_price"] = total_price
        context["products"] = order_products
        context["stripe_session_url"] = stripe_checkout_session(order_before_payment)

        return render(request, "orders/create_order.html", context)


class OrderListTemplateView(LoginRequiredMixin, TemplateView):
    """Displays the list of orders placed by the logged-in user."""

    template_name = "orders/order.html"
    model = Order

    def get_context_data(self, **kwargs) -> dict[str : list[Order]]:
        """
        Retrieves all orders placed by the logged-in user and passes them to the template
        for display in a list format.

            Args:
                **kwargs: Additional keyword arguments passed to the method, including URL parameters.

            Returns:
                dict[str, list[Order]]: A dictionary containing the list of orders, which will be rendered
                                              in the template under the 'orders' key.
        """
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(customer=self.request.user).order_by("-id")
        paginator = Paginator(orders, 12)
        page_number = self.request.GET.get("page")
        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1
        page_obj = paginator.get_page(page_number)
        context["products"] = page_obj
        return context


class OrderDetailTemplateView(LoginRequiredMixin, TemplateView):
    """Displays the details of a specific order placed by the logged-in user."""

    model = Order
    template_name = "orders/order-detail.html"

    def get_object(self, queryset=None) -> Order:
        """
        Retrieves the specific order by its primary key (pk) and ensures the logged-in user
        is the one who placed the order.

            Args:
                queryset (QuerySet, optional): A queryset to retrieve the object (unused in this case).

            Returns:
                Order: The order instance to be displayed.

            Raises:
                Http404: If the order does not belong to the logged-in user or does not exist.
        """
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        if order.customer != self.request.user:
            raise Http404("Order not found or you don't have permission to view it.")

        return order

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Retrieves and passes the order details to the template, including the products
        associated with the order and the Stripe session URL for payment.

            Args:
                **kwargs: Additional keyword arguments passed to the method.

            Returns:
                dict[str, Any]: A dictionary containing the order details, products, and Stripe session URL.
        """
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        products = ProductOrder.objects.filter(order=order)
        customer = CustomUser.objects.get(id=order.customer.id)

        context["customer"] = customer
        context["orders"] = order
        context["products_order"] = products
        context["stripe_session_url"] = stripe_checkout_session(order)
        return context


class OrderDeleteUnpaidView(LoginRequiredMixin, DeleteView):
    """Handles the deletion of an unpaid order placed by the logged-in user."""

    model = Order
    success_url = reverse_lazy("customer-order")

    def get_object(self, queryset=None) -> Order:
        """
        Retrieves the order to be deleted, ensuring the logged-in user is the one who placed it.

            Args:
                queryset (QuerySet, optional): A queryset used to retrieve the object (not used here).

            Returns:
                Order: The order instance to be deleted.

            Raises:
                Http404: If the order does not belong to the logged-in user or does not exist.
        """
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        if order.customer != self.request.user:
            raise Http404("Order not found or you don't have permission to view it.")

        return order

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Passes the order details to the context for confirmation before deletion.

            Args:
                **kwargs: Additional keyword arguments passed to the method.

            Returns:
                dict[str, Any]: A dictionary containing the order to be deleted.
        """
        context = super().get_context_data(**kwargs)
        context["orders"] = self.get_object()

        return context
