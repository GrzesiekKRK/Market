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

        cart = Cart(request)
        products = cart
        order_quantity = cart.__len__()
        total_price = cart.get_sub_total_price()
        date = datetime.today()
        order_before_payment = Order(
                                customer=customer,
                                order_quantity=order_quantity,
                                address=address,
                                date=date,
                                total_price=total_price
                                )
        order_before_payment.save()
        for product in products:
            item = Product.objects.get(id=product['product'].id)
            order_product = ProductOrder(product=item, order=order_before_payment, quantity=item.quantity, price=item.price)
            order_product.save()

        context['customer'] = order_before_payment.customer
        context['order_number'] = order_before_payment.id
        context['order_quantity'] = order_before_payment.order_quantity
        context['address'] = order_before_payment.address
        context['total_price'] = order_before_payment.total_price
        
        context['products'] = ProductOrder.objects.filter(order=order_before_payment)
        for item in order_before_payment.product.all():
            ic(item.quantity)

        return render(request, 'orders/create_order.html', context)


class YourOrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'
    login_required = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(customer=self.request.user)
        context['order'] = orders
        return context


class OrderDetailView(LoginRequiredMixin, TemplateView):
    model = Order
    template_name = 'order/order-detail.html'


