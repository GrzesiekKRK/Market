from django.test import TestCase
from django.urls import reverse

from products.models import Category
from products.forms import ImageForm, AddProductForm
from products.factories import ProductImageFactory

from users.factories import CustomUserFactory


from products.factories import ProductFactory
from products.models import Product
from inventories.factories import InventoryFactory


class ProductListTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.view = reverse("products")
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create_batch(
            10,
        )
        self.additional_factory_deals = ProductFactory.create_batch(5, is_sale=True)

    def test_get_products_page_loads_correctly(self):
        self.client.force_login(self.user)
        response = self.client.get(
            self.view,
        )

        products = Product.objects.all()
        categories = Category.objects.all()
        deals = Product.objects.filter(is_sale=True)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(response.context["products"], products)
        self.assertCountEqual(response.context["categories"], categories)
        self.assertCountEqual(response.context["deals"], deals)
        self.assertTemplateUsed(response, "products/products.html")

    def test_post_products_page_method_not_allowed(self):
        self.client.force_login(self.user)
        response = self.client.post(self.view)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 405)


class ProductDetailTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create()
        self.additional_factory_image = ProductImageFactory.create(product=self.factory)
        self.additional_product_is_sale = ProductFactory(is_sale=True)
        self.additional_factory_image_is_sale = ProductImageFactory.create(
            product=self.additional_product_is_sale
        )

    def test_products_detail_page_loads_correctly(self):
        self.client.force_login(self.user)
        product = Product.objects.last()

        data = {
            "pk": product.id,
        }
        response = self.client.get(reverse("product-detail", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], product)
        self.assertTemplateUsed(response, "products/product-detail.html")

    def test_products_detail_page_loads_correctly_with_instance_is_sale_true(self):
        self.client.force_login(self.user)

        product = Product.objects.get(is_sale=True)

        data = {
            "pk": product.id,
        }
        response = self.client.get(reverse("product-detail", kwargs=data))

        did_get_correct_image = response.context["image"][0]

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], product)
        self.assertEqual(self.additional_factory_image_is_sale, did_get_correct_image)
        self.assertTemplateUsed(response, "products/product-detail.html")


class CategoryTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create()
        self.factory = ProductFactory.create_batch(
            10,
        )
        self.factory_deals = ProductFactory.create_batch(5, is_sale=True)

    def test_category_page_loads_correctly(self):
        self.client.force_login(self.user)
        category = Category.objects.last()

        data = {"pk": category.id}

        response = self.client.get(reverse("category-products", kwargs=data))
        products = Product.objects.filter(category=category)

        """Category site has a menu with hrefs for others categories"""
        categories_without_tested_category = Category.objects.filter().exclude(
            id=category.id
        )

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(list(response.context["products"]), products)
        self.assertCountEqual(
            list(response.context["categories"]), categories_without_tested_category
        )
        self.assertTemplateUsed(response, "products/category.html")


class CreateProductTest(TestCase):
    def setUp(self) -> None:
        self.view = reverse("vendor-add-product")
        """Vendor only"""
        self.user = CustomUserFactory.create(role=2)
        self.factory = ProductFactory.create()
        self.additional_factory_image = ProductImageFactory.create(
            product=self.factory, miniature=True
        )

    def test_create_product_page_loads_correctly(self):
        self.client.force_login(self.user)
        response = self.client.get(
            self.view,
        )

        image_form = response.context["form"]
        add_product_form = response.context["product_form"]

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(image_form, ImageForm)
        self.assertIsInstance(add_product_form, AddProductForm)
        self.assertTemplateUsed(response, "products/add_product.html")

    def test_create_product_page_form_is_valid_loads_correctly(self):
        self.client.force_login(self.user)
        product = Product.objects.last()

        product_data = {
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "miniature_description": product.miniature_description,
            "description": product.description,
            "quantity": product.quantity,
            "units_of_measurement": product.units_of_measurement,
            "sale_price": product.sale_price,
        }

        response = self.client.post(self.view, data=product_data)
        add_product_form = AddProductForm(product_data)
        image_form = ImageForm(product_data)

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(image_form, ImageForm)

        self.assertIsInstance(add_product_form, AddProductForm)
        self.assertEqual(add_product_form.is_valid(), True)


class ProductUpdateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create(role=2)
        self.inventory = InventoryFactory.create(vendor=self.user)
        self.factory = ProductFactory.create()
        self.additional_factory_image = ProductImageFactory.create(product=self.factory)
        self.additional_product_is_sale = ProductFactory(is_sale=True)
        self.additional_factory_image_is_sale = ProductImageFactory.create(
            product=self.additional_product_is_sale
        )

    def test_get_products_update_page_loads_correctly(self):
        self.client.force_login(self.user)
        product = Product.objects.last()
        self.inventory.product.add(product)
        data = {
            "pk": product.id,
        }

        response = self.client.get(reverse("product-update", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], product)
        self.assertTemplateUsed(response, "products/update.html")

    def test_post_products_update_page_loads_correctly(self):
        self.client.force_login(self.user)
        product = Product.objects.last()
        self.inventory.product.add(product)
        data = {
            "pk": product.id,
        }

        product_form_data = {
            "name": product.name,
            "category": product.category,
            "price": product.price,
            "miniature_description": product.miniature_description,
            "description": product.description,
            "quantity": product.quantity,
            "units_of_measurement": product.units_of_measurement,
            "is_sale": True,
            "sale_price": product.sale_price,
        }

        add_product_form = AddProductForm(product_form_data)
        response = self.client.post(reverse("product-update", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.wsgi_request.method, "POST")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], product)
        self.assertEqual(add_product_form.is_valid(), True)
        self.assertTemplateUsed(response, "products/update.html")

    def test_post_products_update_page_invalid_form(self):
        self.client.force_login(self.user)
        product = Product.objects.last()
        self.inventory.product.add(product)
        data = {
            "pk": product.id,
        }

        product_form_data = {
            "name": product.name,
            "category": product.category,
        }
        add_product_invalid_form = AddProductForm(product_form_data)

        response = self.client.post(reverse("product-update", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], product)
        self.assertEqual(add_product_invalid_form.is_valid(), False)
        self.assertTemplateUsed(response, "products/update.html")


class ProductDeleteViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create(role=2)
        self.factory = ProductFactory.create()
        self.additional_factory_image = ProductImageFactory.create(product=self.factory)
        self.additional_product_is_sale = ProductFactory(is_sale=True)
        self.additional_factory_image_is_sale = ProductImageFactory.create(
            product=self.additional_product_is_sale
        )

    def test_get_products_delete_page_loads_correctly(self):
        self.client.force_login(self.user)
        product = Product.objects.last()

        data = {
            "pk": product.id,
        }
        response = self.client.get(reverse("product-delete", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["product"], product)
        self.assertTemplateUsed(response, "products/delete.html")

    def test_post_products_delete_view_works_correctly(self):
        self.client.force_login(self.user)
        product = Product.objects.last()

        data = {
            "pk": product.id,
        }
        response = self.client.post(reverse("product-delete", kwargs=data))

        self.assertEqual(response.wsgi_request.user.is_authenticated, True)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/products/")
