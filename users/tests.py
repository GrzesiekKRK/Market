from django.test import TestCase
from django.urls import reverse
from .forms import RegisterUserForm
from django.test import tag


class TestUserSignUpView(TestCase):
    def setUp(self) -> None:
        self.singup_url = reverse("user-register")

    def test_signup_page_loads_correctly(self):
        response = self.client.get(self.singup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/register.html")
        self.assertIsInstance(response.context["form"], RegisterUserForm)

    def test_signup_post_correct_create_user(self):
        response = self.client.post(self.singup_url, data={"username": ...})
