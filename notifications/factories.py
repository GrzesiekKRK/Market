import factory
from factory.django import DjangoModelFactory
from faker import Faker

from users.factories import CustomUserFactory

from .models import Notification

fake = Faker()


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(CustomUserFactory)
    is_read = False
    title = factory.LazyFunction(
        lambda: fake.sentence(
            nb_words=3,
        )
    )
    body = factory.Faker("paragraph", nb_sentences=3)
