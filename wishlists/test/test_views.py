from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import tag
from wishlists.models import Wishlist
from wishlists.views import WishListTemplateView
from wishlists.factories import WishlistFactory

from users.factories import CustomUserFactory
from users.models import CustomUser

from products.factories import ProductFactory
from products.models import Product


class WishlistListViewTest(TestCase):
    def setUp(self) -> None:
        self.view = reverse('wishlist')
        self.user = CustomUserFactory.create()

    def test_wishlist_page_loads_correctly(self):
        self.client.force_login(self.user)
        wishlist = WishlistFactory.create(user=self.user)

        products = ProductFactory.create_batch(5)
        wishlist.product.add(*products)
        wishlist.save()

        response = self.client.get(self.view, id=wishlist.id)

        self.assertCountEqual(products, list(response.context['products']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist.html')


class WishlistAddProductViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = ProductFactory.create()
        self.user = CustomUserFactory.create()
        self.additional_factory_wishlist = WishlistFactory.create(user=self.user)

    def test_post_with_created_wishlist(self):
        self.client.force_login(self.user)
        product = Product.objects.last()
        data = {
                'pk': product.id,
        }

        response = self.client.post(reverse('add-to-wishlist', kwargs=data))
        print(response.context)
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist.html')
        self.assertEqual(str(response.context['products']), f'<QuerySet [<Product: {product.name}>]>')

    def test_post_with_wishlist_creation(self):
        user = CustomUserFactory.create()
        self.client.force_login(user)

        product = Product.objects.last()
        data = {
            'pk': product.id,
        }

        response = self.client.post(reverse('add-to-wishlist', kwargs=data))
        wish = Wishlist.objects.get(user=user)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist.html')
        self.assertEqual(str(response.context['products']), f'<QuerySet [<Product: {product.name}>]>')
        self.assertEqual(str(wish), f' {user.first_name} {user.last_name} your wishlist')


#TODO wyjatek czy jest ok?
class WishlistRemoveProductViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = ProductFactory.create()
        self.user = CustomUserFactory.create()
        self.additional_factory_wishlist = WishlistFactory.create(user=self.user)

    def test_post_with_created_wishlist(self):
        self.client.force_login(self.user)
        product = Product.objects.last()
        data = {
                'pk': product.id,
        }
        wish = Wishlist.objects.get(user=self.user)
        print(wish)
        response = self.client.post(reverse('wishlist-remove', kwargs=data))
        print(response.context)
        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist.html')
        self.assertEqual(str(response.context['products']), f'<QuerySet []>')

    def test_post_with_none_existing_product(self):
        Product.objects.all().delete()
        self.client.force_login(self.user)
        data = {
            'pk': 5,
        }

        response = self.client.post(reverse('wishlist-remove', kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 404)


