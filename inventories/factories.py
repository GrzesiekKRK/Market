import factory
from factory.django import DjangoModelFactory
from faker import Faker
from users.factories import CustomUserFactory
from products.factories import ProductFactory
from .models import Inventory

fake = Faker()


class InventoryFactory(DjangoModelFactory):
    class Meta:
        model = Inventory

    vendor = factory.SubFactory(CustomUserFactory)
