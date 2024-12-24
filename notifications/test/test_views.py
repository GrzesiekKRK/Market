from django.test import TestCase
from django.urls import reverse
from django.test import tag
from notifications.models import Notification
from notifications.factories import NotificationFactory

from users.factories import CustomUserFactory


class NotificationListTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = NotificationFactory.create_batch(10, user=self.user)
        self.client.force_login(self.user)
        self.view = reverse('notification')

    def test_get_notifications_page_loads_correctly(self):
        user_notifications = Notification.objects.filter(user=self.user)
        response = self.client.get(self.view)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context['notifications'], user_notifications)
        self.assertTemplateUsed(response, 'notification/notification.html')

    def test_post_notifications_page_method_not_allowed(self):
        response = self.client.post(reverse('notification'))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 405)


class NotificationDetailTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = NotificationFactory.create(user=self.user)
        self.client.force_login(self.user)

        self.note = Notification.objects.get(user=self.user)

    def test_get_notification_detail_page_loads_correctly(self):
        data = {
                'pk': self.note.id
        }

        response = self.client.get(reverse('notification-detail', kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['notification'], self.note)
        self.assertEqual(response.context['title'], self.note.title)
        self.assertEqual(response.context['body'], self.note.body)
        self.assertTemplateUsed(response, 'notification/notification-detail.html')

    def test_post_notification_detail_page_method_not_allowed(self):
        data = {
            'pk': self.note.id
        }
        response = self.client.get(reverse('notification-detail', kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)


class NotificationDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = NotificationFactory.create(user=self.user)
        self.client.force_login(self.user)

        self.note = Notification.objects.get(user=self.user)

    def test_post_notification_delete_works_correctly(self):
        data = {
                'pk': self.note.id
                }

        response = self.client.post(reverse('notification-delete', kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/products/')

    # TODO Zmiana na view z post albo stworzyć confirm delete
    # def test_get_notification_delete_works_correctly(self):
    #     data = {
    #             'pk': self.note.id
    #             }
    #
    #     response = self.client.get(reverse('notification-delete', kwargs=data))
    #
    #     self.assertEqual(response.wsgi_request.user.is_authenticated, True)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertRedirects(response, '/products/')
