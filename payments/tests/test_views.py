from django.test import TestCase
from django.urls import reverse

from orders.factories import OrderFactory
from users.factories import CustomUserFactory


class SuccessTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.order = OrderFactory.create(customer=self.user)

    def test_success_template_load_correctly(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("successful-payment", kwargs={"pk": self.order.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/success.html")

    def test_success_template_does_not_work(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("successful-payment", kwargs={"pk": self.user.id})
        )

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, "payments/success.html")


class CancelledTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.order = OrderFactory.create(customer=self.user)

    def test_cancelled_template_load_correctly(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("cancelled-payment", kwargs={"pk": self.order.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/cancel.html")

    def test_cancelled_template_does_not_work(self):
        self.user = CustomUserFactory.create()
        self.client.force_login(self.user)

        response = self.client.get(reverse("cancelled-payment", kwargs={"pk": 999}))

        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, "payments/cancel.html")
