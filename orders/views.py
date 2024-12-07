from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from django.views.generic import TemplateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from datetime import datetime
from .models import Order, ProductOrder

from products.models import Product
from users.models import CustomUser
from cart.cart import Cart
from payments.services import stripe_checkout_session
from icecream import ic


class CreateOrderTemplateView(LoginRequiredMixin, TemplateView):
    model = Order
    template_name = 'orders/create_order.html'

    def post(self, request: HttpRequest) -> HttpResponse:

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
            item = Product.objects.get(id=product['product'].id)
            if item.is_sale:
                price = item.sale_price
            else:
                price = item.price
            order_product = ProductOrder(product=item, order=order_before_payment, quantity=product['quantity'], price=price)
            order_product.save()

        order_products = ProductOrder.objects.filter(order=order_before_payment.id)

        if len(products) == order_quantity:
            cart.clear()

        context['customer'] = customer
        context['address'] = address
        context['postal_code'] = postal_code
        context['order_number'] = order_before_payment.id
        context['order_quantity'] = order_quantity
        context['total_price'] = total_price
        context['products'] = order_products
        context['stripe_session_url'] = stripe_checkout_session(order_before_payment)

        return render(request, 'orders/create_order.html', context)


class OrderListTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs) -> dict[str: list[Order]]:
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(customer=self.request.user).order_by('-id')
        context['orders'] = orders
        return context


class OrderDetailTemplateView(LoginRequiredMixin, TemplateView):
    model = Order
    template_name = 'orders/order-detail.html'

    def get_context_data(self, **kwargs) -> dict[str: Any]:
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id=context['pk'])
        products = ProductOrder.objects.filter(order=order)
        customer = CustomUser.objects.get(id=order.customer.id)

        context['customer'] = customer
        context['orders'] = order
        context['products_order'] = products
        context['stripe_session_url'] = stripe_checkout_session(order)
        return context


class OrderDeleteUnpaidView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('customer-order')
