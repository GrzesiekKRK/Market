from django.test import TestCase
from django.urls import reverse
from django.test import tag
from orders.models import Order, ProductOrder
from orders.factories import OrderFactory, ProductOrderFactory


class CategoryModelTest(TestCase):
    def setUp(self) -> None:
        self.factory = OrderFactory.create()

    def test_model_str_method_output(self):
        order = self.factory
        self.assertEqual(str(order), f"order {order.id} ")
        self.assertEqual(str(order), str(self.factory))
        self.assertIsInstance(order, Order)


class ProductOrderModelTest(TestCase):
    def setUp(self) -> None:
        self.factory = ProductOrderFactory.create()

    def test_model_str_method_output(self):
        product_order = self.factory
        self.assertEqual(
            str(product_order),
            f"Product {product_order.product.name}"
            f" from order {product_order.order},"
            f" in {product_order.quantity} and price {product_order.price}",
        )
        self.assertIsInstance(product_order, ProductOrder)
