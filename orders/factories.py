from datetime import timezone

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from products.factories import ProductFactory
from users.factories import CustomUserFactory

from .models import Order, ProductOrder

fake = Faker()


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    customer = factory.SubFactory(CustomUserFactory)
    address = factory.LazyAttribute(lambda obj: obj.customer.address)
    postal_code = factory.LazyAttribute(lambda obj: obj.customer.postal_code)
    date = factory.Faker("date_time_this_decade", tzinfo=timezone.utc)
    total_price = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True, max_value=9999
    )


class ProductOrderFactory(DjangoModelFactory):
    class Meta:
        model = ProductOrder

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    quantity = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True, max_value=9999
    )
    price = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True, max_value=9999
    )
