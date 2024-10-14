import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from faker import Faker
import random
from .models import Product, ProductImage

fake = Faker()


class ProductFactory(DjangoModelFactory):
    class meta:
        model = Product

    PRODUCT_CHOICES = [
        ...
    ]

    name = factory.Faker('word')
    # category = factory.SubFactory(CategoryFactory)
    price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True, max_value=9999)
    miniature_description = factory.Faker('word')
    description = factory.Faker('word')
    quantity = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True, max_value=9999) # zmienić na int
    units_of_measurement = models.PositiveSmallIntegerField(choices=UNITS_CHOICES,
                                                            default=product_units.PRODUCT_UNITS_PIECE)
    reviews = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=6, default=0, )


class ProductImageFactory(DjangoModelFactory):
    class meta:
        model = ProductImage

    miniature = False
    image =
    product = factory.SubFactory(ProductFactory)
