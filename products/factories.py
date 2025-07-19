import random

import factory
from factory.django import DjangoModelFactory
from faker import Faker

from .models import Category, Product, ProductDimension, ProductImage

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
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=9999,
    )
    miniature_description = factory.Faker("sentence", nb_words=5)
    description = factory.Faker("word")
    quantity = factory.Faker("pyint", min_value=1, max_value=10)

    units_of_measurement = factory.LazyFunction(lambda: str(random.randint(1, 3)))
    sale_price = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=9999,
    )


class ProductDimensionFactory(DjangoModelFactory):
    class Meta:
        model = ProductDimension

    product = factory.SubFactory(ProductFactory)
    length = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=300,
    )
    width = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=150,
    )
    height = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=120,
    )
    weight = factory.Faker(
        "pydecimal",
        left_digits=4,
        right_digits=2,
        positive=True,
        min_value=0.1,
        max_value=50,
    )
    # weight_unit_kg = 3 #TODO  stała jednostka w kg


class ProductImageFactory(DjangoModelFactory):
    class Meta:
        model = ProductImage

    miniature = True
    product = factory.SubFactory(ProductFactory)
