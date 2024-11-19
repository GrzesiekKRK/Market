from django.test import TestCase
from django.urls import reverse
from django.test import tag
from orders.models import Order, ProductOrder
from orders.factories import OrderFactory, ProductOrderFactory

from users.models import CustomUser
from users.factories import CustomUserFactory

from products.models import Product
from products.factories import ProductFactory


class CreateOrderTemplateViewTest(TestCase):

    def setUp(self) -> None:
        self.view = reverse('customer-create-order')
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create_batch(10, )

    #TODO CART jest w view co i jak
    def test_order_create_page_loads_correctly(self):
        self.client.force_login(self.user)
        response = self.client.post(self.view, )

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/create_order.html')


class OrderListTemplateViewTest(TestCase):

    def setUp(self) -> None:
        self.view = reverse('customer-order')
        self.user = CustomUserFactory.create()
        self.factory = OrderFactory.create_batch(10, customer=self.user)

    def test_get_order_list_page_loads_correctly(self):
        self.client.force_login(self.user)
        response = self.client.get(self.view, )

        last_order = Order.objects.last()
        customer = last_order.customer

        order_by = Order.objects.filter(customer=self.user).order_by('-id')

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['orders'], self.factory)
        self.assertEqual(customer, self.user)
        self.assertTemplateUsed(response, 'orders/order.html')


class OrderDetailTemplateViewTest(TestCase):

    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = OrderFactory.create(customer=self.user)


    #TODO Stripe line items
    def test_order_get_page_loads_correctly(self):
        self.client.force_login(self.user)
        order = Order.objects.last()
        data = {
                'pk': order.id,
        }
        print(data)
        response = self.client.get(reverse('customer-order-detail', kwargs=data))

        print(response)
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['customer'], self.user)
        self.assertCountEqual(response.context['orders'], order)
        self.assertCountEqual(response.context['products_order'], self.user)
        self.assertTemplateUsed(response, 'orders/order-detail.html')


#TODO django.urls.exceptions.NoReverseMatch: Reverse for 'market-products' not found? success_url = '/order'
class OrderDeleteUnpaidViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = OrderFactory.create(customer=self.user)

    @tag('x')
    def test_delete_unpaid_order_get_page_loads_correctly(self):
        self.client.force_login(self.user)
        order = Order.objects.last()
        data = {
                'pk': order.id,
        }
        print(data)
        response = self.client.get(reverse('customer-delete-unpaid-order', kwargs=data))
        print(response)
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['customer'], self.user)
        self.assertCountEqual(response.context['orders'], order)
        self.assertCountEqual(response.context['products_order'], self.user)

