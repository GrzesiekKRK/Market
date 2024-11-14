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


class AddToWishListTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = CustomUserFactory.create()

    #TODO co z request i session, request udało sie ale potem żąda session
    def test_add_wish(self):
        ProductFactory.create()
        wishlist = WishlistFactory.create(user=self.user)
        product = Product.objects.last()
        wishlist.save()

        data = {
                'pk': product.id,

        }
        request = self.factory.get(reverse('add-to-wishlist', kwargs=data))
        request.user = self.user
        # request.session['my_key'] = 'my_value'
        view = WishListTemplateView()
        view.setup(request)
        response = view.add_wish(request=request, pk=product.id)
        # response = self.client.post(reverse('add-to-wishlist', kwargs=data))
        print(response)
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'wishlist/wishlist.html')
        # self.assertEqual(str(response.context['wishlist']), f' {user.first_name} {user.last_name} your wishlist')

