from django.test import TestCase
from django.urls import reverse
from django.test import tag
from products.models import Category, Product
from products.factories import ProductFactory, CategoryFactory


class CategoryModelTest(TestCase):

    def setUp(self) -> None:
        self.factory = CategoryFactory.create()

    def test_model_str_method_output(self):
        category = self.factory
        self.assertEqual(str(category), self.factory.name)
        self.assertEqual(str(category), str(self.factory))
        self.assertIsInstance(category, Category)


class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.factory = ProductFactory.create()

    def test_model_str_method_output(self):
        product = self.factory
        self.assertEqual(str(product), self.factory.name)
        self.assertEqual(str(product), str(self.factory))
        self.assertIsInstance(product, Product)
