from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import tag
from unittest import mock
from unittest.mock import patch, Mock, MagicMock


from users.factories import CustomUserFactory
from products.factories import ProductFactory
from orders.factories import OrderFactory, ProductOrderFactory
from inventories.factories import InventoryFactory
from users.models import CustomUser
from notifications.models import Notification
from payments.views import buyer_notification, vendor_notification


class BuyerNotificationTest(TestCase):

    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create()
        self.order = OrderFactory.create(customer=self.user)
        self.order_products = ProductOrderFactory.create(order=self.order, product=self.factory)

    def test_buyer_notification_works_correctly(self):
        notification = buyer_notification(self.order)

        self.assertIsInstance(notification, Notification)
        self.assertEqual(self.user, notification.user)
        self.assertEqual(notification.title, f"Order {self.order.id} payment accepted")
        self.assertEqual(notification.body, f"'Hi your payment was accepted. To see your order click: <a href=\"http://127.0.0.1:8000/order/detail/{self.order.id}\"><i class='fas fa-envelope me-2 text-secondary'></i>Open notification</a>'")

    @tag('x')
    def test_vendor_notification(self):
            vendor = CustomUserFactory.create(role=2)
            inventory = InventoryFactory.create(vendor=vendor)
            inventory.product.add(self.factory)

            vendor_note = vendor_notification(self.order)
            body = f"Hi {vendor} \n\n Sold products: {self.factory.name} {self.order_products.quantity}\r\n"

            self.assertIsInstance(vendor_note, Notification)
            self.assertEqual(vendor_note.title, f"The purchase of your products has been paid for in orders {self.order.id}")
            self.assertEqual(vendor_note.body, body)

    # def test_order_create_page_loads_correctly(self):
    #     self.client.force_login(self.user)
    #     mock_stripe = MagicMock()
    #
    #     with mock.patch('orders.views.stripe_checkout_session', side_effect=mock_stripe.stripe_checkout_session) as mock_stripe:
    #         response = self.client.get(reverse('customer-create-order'))
    #
    #     self.assertEqual(response.wsgi_request.user.is_authenticated, True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'orders/create_order.html')
