from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import tag
from decimal import Decimal
from unittest.mock import MagicMock
from unittest.mock import Mock
from cart.cart import Cart

from products.models import Product
from products.factories import ProductFactory
from users.factories import CustomUserFactory


class CartTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.product = ProductFactory.create()
        self.additional_product = ProductFactory.create()
        self.request = RequestFactory()
        self.request.user = self.user
        self.request.session = MagicMock()
        self.request.session.get.return_value = None

    def test_cart_len_0(self) -> None:
        cart = Cart(self.request)
        self.assertIsInstance(cart, Cart)
        self.assertEqual(len(cart), 0)

    def test_cart_len_2(self) -> None:
        cart = Cart(self.request)
        cart.cart = {self.product.id:
                                            {
                                                'quantity': 2,
                                                'price': str(self.product.price),
                                                'is_sale': int(self.product.is_sale),
                                                'sale_price': str(self.product.sale_price),
                                            },
                    self.additional_product.id:
                                            {
                                                'quantity': 2,
                                                'price': str(self.additional_product.price),
                                                'is_sale': int(self.additional_product.is_sale),
                                                'sale_price': str(self.additional_product.sale_price),
                                            }
                        }
        self.assertEqual(len(cart), 4)
        self.assertIsInstance(cart, Cart)

    def test_cart_len_2_add(self) -> None:
        cart = Cart(self.request)
        cart.add(self.product, quantity=1)
        cart.add(self.additional_product, quantity=1)

        self.assertEqual(len(cart), 2)

    def test_remove_with_two_products_in_cart(self) -> None:
        cart = Cart(self.request)
        cart.add(self.product, quantity=1)
        cart.add(self.additional_product, quantity=1)
        cart.remove(self.product)

        self.assertEqual(len(cart), 1)
        self.assertNotIn(self.product.id, cart.cart)

    def test_remove_wrong_id(self) -> None:
        cart = Cart(self.request)
        cart.add(self.product, quantity=1)
        cart.remove(self.additional_product)

        self.assertEqual(len(cart), 1)
        self.assertNotIn(self.additional_product.id, cart.cart)

    def test_iter_with_for_loop_on_cart(self) -> None:
        session_request = RequestFactory()
        session_request.session = MagicMock()
        session_request.session.get.return_value = None

        cart = Cart(session_request)
        cart.add(self.product, quantity=1)
        cart.add(self.additional_product, quantity=1)

        products = {self.product.id:
                        {
                            'quantity': 1,
                            'price': str(self.product.price),
                            'is_sale': int(self.product.is_sale),
                            'sale_price': str(self.product.sale_price),
                        },
                    self.additional_product.id:
                        {
                            'quantity': 1,
                            'price': str(self.additional_product.price),
                            'is_sale': int(self.additional_product.is_sale),
                            'sale_price': str(self.additional_product.sale_price),
                        }
                            }
        for product, item in zip(cart.cart.values(), products.values()):

            self.assertEqual(str(item['price']), product['price'])
            self.assertEqual(item['quantity'], product['quantity'])
            self.assertEqual(str(item['sale_price']), product['sale_price'])

    def test_get_sub_total_price(self) -> None:
        cart = Cart(self.request)
        product = ProductFactory.create(is_sale=False)
        product2 = ProductFactory.create(is_sale=False)
        cart.add(product, quantity=4)
        cart.add(product2, quantity=1)

        get_sub = cart.get_sub_total_price()
        value = product.price * 4 + product2.price * 1
        self.assertEqual(get_sub, value)

    def test_get_sub_total_price_with_one_product_on_sale(self) -> None:
        cart = Cart(self.request)
        product = ProductFactory.create(is_sale=False)
        product2 = ProductFactory.create(is_sale=True)
        cart.add(product, quantity=4)
        cart.add(product2, quantity=1)

        get_sub = cart.get_sub_total_price()
        value = product.price * 4 + product2.sale_price * 1

        self.assertEqual(get_sub, value)

    def test_fail_save_clear(self) -> None:
        cart = Cart(self.request)
        product = ProductFactory.create(is_sale=False)
        product2 = ProductFactory.create(is_sale=True)
        cart.add(product, quantity=4)
        cart.add(product2, quantity=1)

        self.assertEqual(len(cart), 5)

    def test_clear_cart(self) -> None:
        cart = Cart(self.request)
        product = ProductFactory.create(is_sale=False)
        product2 = ProductFactory.create(is_sale=True)
        cart.add(product, quantity=4)
        cart.add(product2, quantity=1)

        cart.clear()

        self.assertEqual(len(cart), 0)
        self.assertEqual(cart.cart, {})

