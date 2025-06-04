import factory
from factory.django import DjangoModelFactory
from faker import Faker

from deliveries.models import Delivery

faker = Faker()


class DeliveryFactory(DjangoModelFactory):
    class Meta:
        model = Delivery

    id = factory.Faker("pyint", min_value=1, max_value=9)
    name = factory.Faker("word")
    price = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=500,
    )
    delivery_average_time = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=1,
        max_value=10,
    )
    max_length = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=300,
    )
    max_width = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=1,
        max_value=150,
    )
    max_height = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=120,
    )
    max_weight = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=50,
    )
