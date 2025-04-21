from django.test import TestCase
from django.urls import reverse

from inventories.factories import InventoryFactory
from notifications.factories import NotificationFactory
from notifications.models import Notification
from notifications.views import OrderNotification
from orders.factories import OrderFactory, ProductOrderFactory
from products.factories import ProductFactory
from users.factories import CustomUserFactory


class NotificationListTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = NotificationFactory.create_batch(10, user=self.user)
        self.client.force_login(self.user)
        self.view = reverse("notification")

    def test_get_notifications_page_loads_correctly(self):
        user_notifications = Notification.objects.filter(user=self.user)
        response = self.client.get(self.view)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["notifications"], user_notifications)
        self.assertTemplateUsed(response, "notification/notification.html")

    def test_post_notifications_page_method_not_allowed(self):
        response = self.client.post(reverse("notification"))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 405)


class NotificationDetailTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = NotificationFactory.create(user=self.user)
        self.client.force_login(self.user)

        self.note = Notification.objects.get(user=self.user)

    def test_get_notification_detail_page_loads_correctly(self):
        data = {"pk": self.note.id}

        response = self.client.get(reverse("notification-detail", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notification"], self.note)
        self.assertEqual(response.context["title"], self.note.title)
        self.assertEqual(response.context["body"], self.note.body)
        self.assertTemplateUsed(response, "notification/notification-detail.html")

    def test_post_notification_detail_page_method_not_allowed(self):
        data = {"pk": self.note.id}
        response = self.client.get(reverse("notification-detail", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)


class NotificationDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = NotificationFactory.create(user=self.user)
        self.client.force_login(self.user)

        self.note = Notification.objects.get(user=self.user)

    def test_post_notification_delete_works_correctly(self):
        data = {"pk": self.note.id}

        response = self.client.post(reverse("notification-delete", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/products/")


class BuyerVendorNotificationCreationTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create()
        self.order = OrderFactory.create(customer=self.user)
        self.order_products = ProductOrderFactory.create(
            order=self.order, product=self.factory
        )

    def test_buyer_notification_works_correctly(self):
        notification = OrderNotification.buyer_notification(self.order)

        self.assertIsInstance(notification, Notification)
        self.assertEqual(self.user, notification.user)
        self.assertEqual(notification.title, f"Order {self.order.id} payment accepted")
        self.assertEqual(
            notification.body,
            f"'Hi your payment was accepted. To see your order click: <a href=\"http://127.0.0.1:8000/order/detail/{self.order.id}\"><i class='fas fa-envelope me-2 text-secondary'></i>Open notification</a>'",
        )

    def test_vendor_notification(self):
        vendor = CustomUserFactory.create(role=2)
        inventory = InventoryFactory.create(vendor=vendor)
        inventory.products.add(self.factory)

        vendor_note = OrderNotification.vendor_notification(self.order)
        body = f"Hi {vendor} \n\n Sold products: {self.factory.name} {self.order_products.quantity}\r\n"

        self.assertIsInstance(vendor_note, Notification)
        self.assertEqual(
            vendor_note.title,
            f"The purchase of your products has been paid for in orders {self.order.id}",
        )
        self.assertEqual(vendor_note.body, body)
