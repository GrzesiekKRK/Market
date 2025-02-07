import random

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from .models import Category, Product, ProductImage

fake = Faker()

CATEGORIES = ["Beverages", "Fruits", "Vegetables"]


PRODUCTS_BY_CATEGORY = {
    "Beverages": [
        "Watermelon Juice",
        "Kiwi Juice",
        "Banana Juice",
        "Pineapple Juice",
        "Carrot Juice",
    ],
    "Fruits": ["Watermelon", "Kiwi", "Banana", "Pineapple"],
    "Vegetables": ["Broccoli", "Potato", "Carrot"],
}


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.LazyFunction(lambda: random.choice(CATEGORIES))


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = factory.SubFactory(CategoryFactory)
    name = factory.LazyAttribute(
        lambda obj: random.choice(PRODUCTS_BY_CATEGORY[obj.category.name])
    )
    price = factory.Faker(
        "pydecimal", left_digits=4, right_digits=2, positive=True, max_value=9999
    )
    miniature_description = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("word")
    quantity = factory.Faker("pyint", min_value=0, max_value=10)

    units_of_measurement = factory.LazyFunction(lambda: str(random.randint(1, 3)))


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    miniature = True
    product = factory.SubFactory(ProductFactory)
