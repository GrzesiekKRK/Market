from django.test import TestCase
from notifications.models import Notification
from notifications.factories import NotificationFactory

from users.factories import CustomUserFactory


class NotificationModelTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = NotificationFactory.create_batch(10, user=self.user)

    def test_model_str_method_output(self):
        user_notifications = Notification.objects.filter(user=self.user)
        last_notification = Notification.objects.last()
        self.assertEqual(
            str(last_notification),
            f"Notification of user {last_notification.user} {last_notification.body}",
        )
        self.assertIsInstance(last_notification, Notification)
        self.assertCountEqual(user_notifications, self.factory)
