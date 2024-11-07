
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from users.factories import CustomUserFactory
from .models import Wishlist
fake = Faker()


class WishlistFactory(DjangoModelFactory):
    class Meta:
        model = Wishlist

    user = factory.SubFactory(CustomUserFactory)

