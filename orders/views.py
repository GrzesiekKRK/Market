from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from datetime import datetime
from .models import Order, ProductOrder

from products.models import Product
from users.models import CustomUser
from cart.cart import Cart
from payments.services import stripe_checkout_session
from icecream import ic


class CreateOrderView(LoginRequiredMixin):
    @staticmethod
    def create_order(request):
        context = {}

        user = request.user
        customer = CustomUser.objects.get(id=user.id)
        address = customer.address
        postal_code = customer.postal_code

        cart = Cart(request)
        products = cart
        order_quantity = cart.__len__()
        total_price = cart.get_sub_total_price()
        # date = datetime.today()

        order_before_payment = Order.objects.get_or_create(
                                                            customer=customer,
                                                            order_quantity=order_quantity,
                                                            address=address,
                                                            postal_code=postal_code,
                                                            # date=date,
                                                            total_price=total_price,
                                                            )

        order_before_payment[0].save()
        for product in products:
            item = Product.objects.get(id=product['product'].id)
            order_product = ProductOrder(product=item, order=order_before_payment[0], quantity=product['quantity'], price=product['price'])
            order_product.save()

        order_products = ProductOrder.objects.filter(order=order_before_payment[0])
        if len(products) == len(order_products):
            cart.clear()

        context['customer'] = customer
        context['address'] = address
        context['postal_code'] = postal_code
        context['order_number'] = order_before_payment[0].id
        context['order_quantity'] = order_quantity
        context['total_price'] = total_price
        context['products'] = order_products
        context['stripe_session_url'] = stripe_checkout_session(order_before_payment[0])
        return render(request, 'orders/create_order.html', context)


class YourOrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(customer=self.request.user)
        context['orders'] = orders
        return context


class OrderDetailView(LoginRequiredMixin, TemplateView):
    model = Order
    template_name = 'orders/order-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.get(id=context['pk'])
        products = ProductOrder.objects.filter(order=order)
        customer = CustomUser.objects.get(id=order.customer.id)

        context['customer'] = customer
        context['orders'] = order
        context['products_order'] = products
        context['stripe_session_url'] = stripe_checkout_session(order)
        return context


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    success_url = '/order'
