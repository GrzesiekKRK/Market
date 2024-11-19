from django.test import TestCase
from django.urls import reverse
from django.test import tag
from notifications.models import Notification
from notifications.factories import NotificationFactory

from users.factories import CustomUserFactory
from orders.models import Order, ProductOrder
from orders.factories import OrderFactory, ProductOrderFactory


class NotificationModelTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = NotificationFactory.create_batch(10, user=self.user)


    def test_model_str_method_output(self):
        user_notifications = Notification.objects.filter(user=self.user)
        last_notification = Notification.objects.last()
        self.assertEqual(str(last_notification), f'Notification of user {last_notification.user} {last_notification.body}')
        self.assertIsInstance(last_notification, Notification)
        self.assertCountEqual(user_notifications, self.factory)


