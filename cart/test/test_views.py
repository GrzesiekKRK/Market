from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import tag
from ..views import CartTemplateView
from unittest import mock
from unittest.mock import patch, Mock, MagicMock

from cart.cart import Cart

from products.models import Product
from products.factories import ProductFactory
from users.factories import CustomUserFactory
from inventories.factories import InventoryFactory


class CartTemplateViewTest(TestCase): # TODO fix this test
    def setUp(self) -> None:
        self.product = ProductFactory.create()
        self.user = CustomUserFactory.create()


    def test_get_with_mock_cart(self):
        self.client.force_login(self.user)

        mock_session = MagicMock()

        mock_session.session = {}

        factory = RequestFactory()
        factory.session = mock_session
        cart_instance = Cart(factory)
        cart_instance.cart = {self.product.id:
                                    {
                                     'quantity': 1,
                                     'price': str(self.product.price),
                                     'is_sale': int(self.product.is_sale),
                                     'sale_price': str(self.product.sale_price),
                                     }}

        request = factory.get(reverse('cart'))
        request.session = mock_session
        request.user = self.user
        response = CartTemplateView.as_view()(request)
        response.render()
        # print(vars(response))
        self.assertEqual(response.status_code, 200)
        print(vars(response))
        # self.assertIsInstance(response.context['products'], Cart)
        # self.assertTemplateUsed(response, 'cart/cart.html')


    def test_invalid_get(self):
        self.client.force_login(self.user)
        mock_cart = MagicMock(spec=Cart)
        # mock_cart.get_sub_total_price.return_value = 10
        mock_cart.get_sub_total_price
        mock_cart.__len__.side_effect = Cart.__len__
        mock_cart.cart = {self.product.id:
                                    {
                                     'quantity': 1,
                                     'price': str(self.product.price),
                                     'is_sale': int(self.product.is_sale),
                                     'sale_price': str(self.product.sale_price),
                                     }}
        with mock.patch('cart.views.Cart', side_effect=mock_cart.cart) as mock_cart:
            response = self.client.get(reverse('cart'))


        print(response.context)
