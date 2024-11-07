from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, login
from users.forms import RegisterUserForm, LoginForm
from django.test import tag
from users.models import CustomUser
from users.factories import CustomUserFactory
from django.contrib.auth.hashers import make_password


class TestUserSignUpView(TestCase):
    def setUp(self) -> None:
        self.signup_url = reverse('user-register')

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(
                                  username='test_user',
                                  password='1X<ISRUkw+tuK',
                                  first_name='first',
                                  last_name='last',
                                  email='krk12@wp.pl',
                                  pesel='12345678911',
                                  bank_account='1234756890123456789123450',
                                  secondary_email='walmart@wp.pl',
                                  address='New York',
                                  postal_code='32-576',
                                  role=2,
                                  reviews=3.5
                                  )

    def test_signup_page_loads_correctly(self):
        response = self.client.get(self.signup_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], RegisterUserForm)

    def test_signup_post_correct_create_user(self):
        data = {'username': 'test_user2',
                'password1': '1X<ISRUkw+tuK',
                'password2': '1X<ISRUkw+tuK',
                'email': 'krk12@wp.pl',
                'pesel': '12245677911',
                'secondary_email': 'walmart@wp.pl',
                'address': 'Warhaz',
                'postal_code': '32-576',
                'first_name': 'first2',
                'last_name': 'last2',
                'role': 2,
                'reviews': 5.0,
                'bank_account': '1234756890123456789123450',
                }
        response = self.client.post(self.signup_url, data=data)
        self.assertEqual(CustomUser.objects.count(), 2)
        user = CustomUser.objects.last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.username, data['username'])
        self.assertEqual(user.role, data['role'])
        self.assertRedirects(response, '/accounts/login/')


class TestCustomUserLoginView(TestCase):

    def setUp(self) -> None:
        self.sign_in = reverse('user-login')

    @classmethod
    def setUpTestData(cls):
        CustomUserFactory.create(password=make_password('1X<ISRUkw+tuK'))

    def test_login_uses_correct_template(self):
        response = self.client.get(reverse('user-login'))

        self.assertTemplateUsed(response, 'users/login.html')

    def test_sign_in_page_loads_correctly(self):
        response = self.client.post(self.sign_in)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_correct_login(self):
        user = CustomUser.objects.last()
        response = self.client.post(self.sign_in)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], LoginForm)
        # self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        # self.assertRedirects(response, reverse('products'), status_code=200)

    def test_invalid_form(self):
        data = {'username': 'fail_user',
                'password': '1X<ISRUkw+tuK',
                }

        response = self.client.post(self.sign_in, data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)


class TestUserDeleteView(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUserFactory.create()

    def test_delete_user_get(self):

        user = CustomUser.objects.last()
        response = self.client.get(reverse('user-delete', args=[user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/delete.html')
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)
        self.assertEqual(response.context['object'], user)
        self.assertContains(response, 'Are you sure you want to delete')

    def test_delete_user_post(self):
        user = CustomUser.objects.last()
        response = self.client.post(reverse('user-delete', args=[user.id]))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/')
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)
        # self.assertEqual(response, user.id) # Post jak sprawdzić useraname

