from django.test import TestCase
from django.urls import reverse
from django.test import tag
from wishlists.models import Wishlist
from wishlists.factories import WishlistFactory


class WishlistModelTest(TestCase):

    def setUp(self):
        self.factory = WishlistFactory.create()

    def test_model_str_method_output(self):
        wish = Wishlist.objects.last()
        self.assertEqual(str(self.factory), f" {wish.user.first_name} {wish.user.last_name} your wishlist")
