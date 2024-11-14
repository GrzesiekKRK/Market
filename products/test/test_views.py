from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import tag
from products.models import Category, Product, ProductImage
from products.forms import ImageForm, AddProductForm, UpdateImageForm
from products.views import ProductUpdateView, ProductDeleteView
from products.factories import ProductFactory, CategoryFactory, ProductImageFactory

from users.factories import CustomUserFactory
from users.models import CustomUser

from products.factories import ProductFactory
from products.models import Product


class ProductListTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.view = reverse('products')
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create_batch(10,)
        self.additional_factory_deals = ProductFactory.create_batch(5, is_sale=True)

    def test_products_page_loads_correctly(self):
        self.client.force_login(self.user)
        response = self.client.get(self.view,)

        products = Product.objects.all()
        categories = Category.objects.all()
        deals = Product.objects.filter(is_sale=True)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(list(response.context['products']), products)
        self.assertCountEqual(list(response.context['categories']), categories)
        self.assertCountEqual(list(response.context['deals']), deals)
        self.assertTemplateUsed(response, 'products/products.html')


class ProductDetailTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create()
        self.additional_factory_image = ProductImageFactory.create(product=self.factory)
        self.additional_product_is_sale = ProductFactory(is_sale=True)
        self.additional_factory_image_is_sale = ProductImageFactory.create(product=self.additional_product_is_sale)

    def test_products_detail_page_loads_correctly(self):
        self.client.force_login(self.user)
        product = Product.objects.last()

        data = {
                'pk': product.id,
        }
        response = self.client.get(reverse('product-detail', kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertTemplateUsed(response, 'products/product-detail.html')

    def test_products_detail_page_loads_correctly_with_instance_is_sale_true(self):
        self.client.force_login(self.user)

        # create_product_is_sale = ProductFactory.create(is_sale=True)
        product = Product.objects.get(is_sale=True)

        # create_product_image = ProductImageFactory.create(product=product)
        product_image = ProductImage.objects.get(id=product.id)

        data = {
                'pk': product.id,
                }
        response = self.client.get(reverse('product-detail', kwargs=data))

        did_get_correct_image = response.context['image'][0]

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)
        self.assertEqual(did_get_correct_image, product_image)
        self.assertTemplateUsed(response, 'products/product-detail.html')


class CategoryTemplateViewTest(TestCase):
    def setUp(self) -> None:
        # self.view = reverse('category-products')# jak to użyć poprawnie
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create_batch(10,)
        self.factory_deals = ProductFactory.create_batch(5, is_sale=True)

    def test_category_page_loads_correctly(self):
        self.client.force_login(self.user)
        category = Category.objects.last()

        data = {
                'pk': category.id
        }

        response = self.client.get(reverse('category-products', kwargs=data))
        products = Product.objects.filter(category=category)

        """Category site has a menu with hrefs for others categories"""
        categories_without_tested_category = Category.objects.filter().exclude(id=category.id)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(list(response.context['products']), products)
        self.assertCountEqual(list(response.context['categories']), categories_without_tested_category)
        self.assertTemplateUsed(response, 'products/category.html')


class CreateProductTest(TestCase):
    def setUp(self) -> None:
        self.view = reverse('vendor-add-product')
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create_batch(10,)
        self.additional_factory_deals = ProductFactory.create_batch(5, is_sale=True)


    def test_create_product_page_loads_correctly(self):
        self.client.force_login(self.user)
        response = self.client.get(self.view,)

        image_form = response.context['form']
        add_product_form = response.context['product_form']

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(image_form, ImageForm)
        self.assertIsInstance(add_product_form, AddProductForm)
        self.assertTemplateUsed(response, 'products/add_product.html')

    #TODO co z request
    def test_create_product_page_form_is_valid_loads_correctly(self):
        self.client.force_login(self.user)
        response = self.client.post(self.view, )
        print(response)

        image_form = response.context['form']
        add_product_form = response.context['product_form']

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(image_form, ImageForm)
        self.assertIsInstance(add_product_form, AddProductForm)
        # self.assertTemplateUsed(response, 'products/product-detail.html')
