import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from faker import Faker
import random
from .consts import USER_ROLES

fake = Faker()


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
    pesel = factory.LazyFunction(
        lambda: "".join(str(random.randint(0, 9)) for _ in range(11))
    )
    bank_account = factory.LazyFunction(
        lambda: "".join(str(random.randint(0, 9)) for _ in range(25))
    )
    created_at = factory.Faker("date_time_this_decade")
    secondary_email = factory.Faker("email")
    address = factory.Faker("address")
    postal_code = factory.LazyFunction(
        lambda: f"{random.randint(10, 99)}-{random.randint(100, 999)}"
    )
    role = factory.LazyFunction(lambda: random.choice(USER_ROLES))
    reviews = 0
