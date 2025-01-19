from unittest import mock
from unittest.mock import MagicMock

from django.test import TestCase
from django.urls import reverse

from orders.factories import OrderFactory, ProductOrderFactory
from orders.models import Order, ProductOrder
from products.factories import ProductFactory
from users.factories import CustomUserFactory

mock_instance = mock.Mock()


class CreateOrderTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.view = reverse("customer-create-order")
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create_batch(
            10,
        )

    def test_order_create_page_loads_correctly(self):
        self.client.force_login(self.user)
        mock_stripe = MagicMock()

        with mock.patch(
            "orders.views.stripe_checkout_session",
            side_effect=mock_stripe.stripe_checkout_session,
        ) as mock_stripe:
            response = self.client.get(reverse("customer-create-order"))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/create_order.html")


class OrderListTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.view = reverse("customer-order")
        self.user = CustomUserFactory.create()
        self.factory = OrderFactory.create_batch(10, customer=self.user)

    def test_get_order_list_page_loads_correctly(self):
        self.client.force_login(self.user)
        orders_list = Order.objects.filter(customer=self.user)
        mock_stripe = MagicMock()

        with mock.patch(
            "orders.views.stripe_checkout_session",
            side_effect=mock_stripe.stripe_checkout_session,
        ) as mock_stripe:
            response = self.client.get(reverse("customer-order"))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(orders_list), len(self.factory))
        self.assertCountEqual(response.context["orders"], self.factory)
        self.assertTemplateUsed(response, "orders/order.html")


class OrderDetailTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.order = OrderFactory.create(customer=self.user)
        self.factory = ProductOrderFactory.create(order=self.order)

    def test_get_order_page_loads_correctly(self):
        self.client.force_login(self.user)
        order = Order.objects.last()
        data = {
            "pk": order.id,
        }

        with mock.patch("orders.views.stripe_checkout_session", return_value={}):
            response = self.client.get(reverse("customer-order-detail", kwargs=data))

        product_order = ProductOrder.objects.all()

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["customer"], self.user)
        self.assertEqual(response.context["orders"], order)
        self.assertEqual(str(response.context["products_order"]), str(product_order))
        self.assertTemplateUsed(response, "orders/order-detail.html")

    def test_post_order_method_not_allowed(self):
        self.client.force_login(self.user)
        order = Order.objects.last()
        data = {
            "pk": order.id,
        }

        with mock.patch("orders.views.stripe_checkout_session", return_value={}):
            response = self.client.post(reverse("customer-order-detail", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 405)


class OrderDeleteUnpaidViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = OrderFactory.create(customer=self.user)

    def test_get_delete_unpaid_order_page_loads_correctly(self):
        self.client.force_login(self.user)
        order = Order.objects.last()
        data = {
            "pk": order.id,
        }
        response = self.client.get(reverse("customer-delete-unpaid-order", kwargs=data))
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], order)

    def test_post_delete_unpaid_order_page_loads_correctly(self):
        self.client.force_login(self.user)
        order = Order.objects.last()
        data = {
            "pk": order.id,
        }
        response = self.client.post(
            reverse("customer-delete-unpaid-order", kwargs=data)
        )

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/order/")
