from django.test import TestCase

from products.factories import ProductFactory, ProductImageFactory
from products.forms import AddProductForm, ImageForm


class AddProductFormTest(TestCase):
    def setUp(self) -> None:
        self.product = ProductFactory.create()

    def test_form_is_invalid_price_as_char(self):
        data = {
            "name": self.product.name,
            "category": self.product.category,
            "price": self.product.name,
            "miniature_description": self.product.miniature_description,
            "description": self.product.description,
            "quantity": self.product.quantity,
            "units_of_measurement": self.product.units_of_measurement,
            "is_sale": self.product.is_sale,
            "sale_price": self.product.sale_price,
        }

        form = AddProductForm(data)

        self.assertEqual(form.is_valid(), False)

    def test_form_invalid_first_name_is_required(self):
        data = {
            "category": self.product.category,
            "price": self.product.description,
            "miniature_description": self.product.miniature_description,
            "description": self.product.description,
            "quantity": self.product.quantity,
            "units_of_measurement": self.product.units_of_measurement,
            "is_sale": self.product.is_sale,
            "sale_price": self.product.sale_price,
        }
        form = AddProductForm(data)

        self.assertEqual(form.is_valid(), False)

    def test_form_data_is_valid(self):
        data = {
            "name": self.product.name,
            "category": self.product.category,
            "price": self.product.price,
            "miniature_description": self.product.miniature_description,
            "description": self.product.description,
            "quantity": self.product.quantity,
            "units_of_measurement": self.product.units_of_measurement,
            "is_sale": self.product.is_sale,
            "sale_price": self.product.sale_price,
        }
        form = AddProductForm(data)

        self.assertEqual(form.is_valid(), True)


class ImageFormTest(TestCase):
    def setUp(self) -> None:
        self.image = ProductImageFactory.create()

    def test_form_is_invalid_no_image(self):

        data = {
            "miniature": self.image.miniature,
            "image": self.image,
        }

        form = ImageForm(data)

        self.assertEqual(form.is_valid(), False)

    def test_form_data_is_valid(self):
        data = {
            "miniature": self.image.miniature,
            "image": self.image,
        }
        form = ImageForm(data)

        self.assertEqual(form.is_valid(), False)


class UpdateImageFormTest(TestCase):
    def setUp(self) -> None:
        self.image = ProductImageFactory.create()

    def test_form_is_invalid(self):
        data = {
            "miniature": self.image.miniature,
            "image": self.image,
        }
        form = ImageForm(data)

        self.assertEqual(form.is_valid(), False)

    # TODO Image form fix by stachu
    # def test_form_data_is_valid(self):
    #     data = {
    #         'miniature': self.image.miniature,
    #         'image': self.image,
    #     }
    #     form = ImageForm(data)
    #
    #     self.assertEqual(form.is_valid(), True)
