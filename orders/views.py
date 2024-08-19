from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from datetime import datetime
from .models import Order, ProductOrder

from products.models import Product
from users.models import CustomUser
from cart.cart import Cart
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
        date = datetime.today()

        order_before_payment = CreateOrderView.check_order(request, customer, products, total_price)

        if not order_before_payment:
            order_before_payment = Order(
                                    customer=customer,
                                    order_quantity=order_quantity,
                                    address=address,
                                    postal_code=postal_code,
                                    date=date,
                                    total_price=total_price
                                    )
            order_before_payment.save()
            for product in products:
                item = Product.objects.get(id=product['product'].id)
                order_product = ProductOrder(product=item, order=order_before_payment, quantity=product['product'].quantity, price=product['product'].price)
                order_product.save()

        context['customer'] = customer
        context['address'] = address
        context['postal_code'] = postal_code
        context['order_number'] = order_before_payment.id
        context['order_quantity'] = order_quantity
        context['total_price'] = total_price
        context['products'] = products

        return render(request, 'orders/create_order.html', context)

    @staticmethod
    def check_order(request, customer, products, total_price):
        order = Order.objects.get(customer=customer,  total_price=total_price)

        if not order:
            return False
        return order


class YourOrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'
    login_required = True
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

        context['orders'] = order
        context['products'] = products
        return context

