from django.test import TestCase
from django.urls import reverse
from django.test import tag
from django.contrib.auth.hashers import make_password
import random
from users.forms import RegisterUserForm, LoginForm, UpdateUserForm

from users.models import CustomUser
from users.factories import CustomUserFactory


class RegisterUserFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUserFactory.create(password=make_password("1X<ISRUkw+tuK"))

    def test_form_is_invalid(self):
        random_user_data = CustomUser.objects.last()

        data = {
            "username": f"{random_user_data.username}2",
            "password1": random_user_data.password,
            "password2": random_user_data.password,
            "email": random_user_data.email,
            "secondary_email": random_user_data.secondary_email,
            "address": random_user_data.address,
            "postal_code": random_user_data.postal_code,
            "pesel": random_user_data.pesel,
            "first_name": random_user_data.first_name,
            "last_name": random_user_data.last_name,
            "role": random_user_data.role,
            "bank_account": random_user_data.bank_account,
        }
        form = RegisterUserForm(data)

        self.assertFalse(form.is_valid())

    def test_form_first_name_is_required(self):
        random_user_data = CustomUser.objects.last()

        data = {
            "username": f"{random_user_data.username}2",
            "email": random_user_data.email,
            "secondary_email": random_user_data.secondary_email,
            "address": random_user_data.address,
            "postal_code": random_user_data.postal_code,
            "pesel": random_user_data.pesel,
            "last_name": random_user_data.last_name,
            "role": random_user_data.role,
            "bank_account": random_user_data.bank_account,
        }

        form = RegisterUserForm(data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, field="first_name", errors="This field is required.")

    def test_form_data_is_valid(self):
        random_user_data = CustomUser.objects.last()

        unique_username = "".join(str(random.randint(0, 9)) for _ in range(11))
        unique_pesel = "".join(str(random.randint(0, 9)) for _ in range(11))

        data = {
            "username": unique_username,
            "password1": random_user_data.password,
            "password2": random_user_data.password,
            "email": random_user_data.email,
            "secondary_email": random_user_data.secondary_email,
            "address": random_user_data.address,
            "postal_code": random_user_data.postal_code,
            "pesel": unique_pesel,
            "first_name": random_user_data.first_name,
            "last_name": random_user_data.last_name,
            "role": random_user_data.role,
            "reviews": 5.0,
            "bank_account": random_user_data.bank_account,
        }

        form = RegisterUserForm(data)

        self.assertTrue(form.is_valid())


class LoginFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUserFactory.create()

    def test_form_is_invalid_no_password(self):
        random_user_data = CustomUser.objects.last()
        data = {
            "username": random_user_data.username,
        }
        form = LoginForm(data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, field="password", errors="This field is required.")

    def test_form_data_is_valid(self):
        random_user_data = CustomUser.objects.last()
        data = {
            "username": random_user_data.username,
            "password": random_user_data.password,
        }
        form = LoginForm(data)
        self.assertTrue(form.is_valid())


class UpdateUserFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUserFactory.create()

    def test_form_is_invalid_no_first_name(self):
        random_user_data = CustomUser.objects.last()
        data = {
            "username": random_user_data.username,
            "email": random_user_data.email,
            "secondary_email": random_user_data.secondary_email,
            "address": random_user_data.address,
            "postal_code": random_user_data.postal_code,
            "last_name": random_user_data.last_name,
            "bank_account": random_user_data.bank_account,
        }

        form = UpdateUserForm(data)

        self.assertFalse(form.is_valid())
        self.assertFormError(form, field="first_name", errors="This field is required.")

    def test_form_data_is_valid(self):
        random_user_data = CustomUser.objects.last()
        unique_username = "".join(str(random.randint(0, 9)) for _ in range(11))

        data = {
            "username": unique_username,
            "email": random_user_data.email,
            "secondary_email": random_user_data.secondary_email,
            "address": random_user_data.address,
            "postal_code": random_user_data.postal_code,
            "first_name": random_user_data.first_name,
            "last_name": random_user_data.last_name,
            "bank_account": random_user_data.bank_account,
        }
        form = UpdateUserForm(data)

        self.assertTrue(form.is_valid())
