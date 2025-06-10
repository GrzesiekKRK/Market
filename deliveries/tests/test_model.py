from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from deliveries.factories import DeliveryFactory
from deliveries.models import Delivery
from inventories.factories import InventoryFactory
from products.consts import PRODUCT_UNITS_KILOGRAMS
from products.factories import ProductDimensionFactory, ProductFactory


class DeliveryModelTest(TestCase):
    def setUp(self):
        self.delivery_locker_standard = DeliveryFactory.create(
            id=1,
            name="Standard Parcel lockers",
            price=15.99,
            delivery_average_time=3,
            weight_unit=PRODUCT_UNITS_KILOGRAMS,
            max_length=90,
            max_width=40,
            max_height=20,
            max_weight=25,
        )
        self.delivery_minimal_dimensions_value = DeliveryFactory.create(
            id=3,
            name="Express Parcel lockers",
            price=15.99,
            delivery_average_time=3,
            weight_unit=PRODUCT_UNITS_KILOGRAMS,
            max_length=0.1,
            max_width=0.1,
            max_height=0.1,
            max_weight=0.1,
        )

    def test_delivery_creation(self):
        self.assertEqual(self.delivery_locker_standard.name, "Standard Parcel lockers")
        self.assertEqual(self.delivery_locker_standard.price, Decimal(15.99))
        self.assertEqual(self.delivery_locker_standard.delivery_average_time, 3)
        self.assertEqual(
            self.delivery_locker_standard.weight_unit, PRODUCT_UNITS_KILOGRAMS
        )

    def test_delivery_str_method(self):
        expected = "Delivery by Standard Parcel lockers  on average in 3 days "
        self.assertEqual(str(self.delivery_locker_standard), expected)

    def test_delivery_validators_min_values(self):
        with self.assertRaises(ValidationError):
            delivery = Delivery(
                name="Test Delivery",
                price=Decimal("10.00"),
                delivery_average_time=2,
                max_length=Decimal("0.05"),  # Poniżej minimum
                max_width=Decimal("0.05"),  # Poniżej minimum
                max_height=Decimal("0.05"),  # Poniżej minimum
                max_weight=Decimal("0.05"),  # Poniżej minimum
            )
            delivery.full_clean()

    def test_delivery_validators_max_values(self):
        with self.assertRaises(ValidationError):
            delivery = Delivery(
                name="Test Delivery",
                price=Decimal("10.00"),
                delivery_average_time=2,
                max_length=Decimal("350.00"),  # Powyżej maksimum
                max_width=Decimal("200.00"),  # Powyżej maksimum
                max_height=Decimal("150.00"),  # Powyżej maksimum
                max_weight=Decimal("60.00"),  # Powyżej maksimum
            )
            delivery.full_clean()


class DeliveryMethodsWorkflowTest(TestCase):
    def setUp(self):
        self.delivery_locker_standard = DeliveryFactory.create(
            id=1,
            name="Standard Parcel lockers",
            price=15.99,
            delivery_average_time=3,
            weight_unit=PRODUCT_UNITS_KILOGRAMS,
            max_length=90,
            max_width=40,
            max_height=20,
            max_weight=25,
        )

        self.delivery_standard_house = DeliveryFactory.create(
            id=4,
            name="Standard In-house",
            price=40,
            delivery_average_time=6,
            weight_unit=PRODUCT_UNITS_KILOGRAMS,
            max_length=300,
            max_width=150,
            max_height=120,
            max_weight=50,
        )
        self.delivery_standard_remote = DeliveryFactory.create(
            id=7,
            name="Standard Remote",
            price=30,
            delivery_average_time=6,
            weight_unit=PRODUCT_UNITS_KILOGRAMS,
            max_length=300,
            max_width=150,
            max_height=120,
            max_weight=50,
        )

        self.delivery_minimal_dimensions_value = DeliveryFactory.create(
            id=3,
            name="Express Parcel lockers",
            price=15.99,
            delivery_average_time=3,
            weight_unit=PRODUCT_UNITS_KILOGRAMS,
            max_length=0.1,
            max_width=0.1,
            max_height=0.1,
            max_weight=0.1,
        )
        """ Vendor products   """

        self.product_1_no_lockers = ProductFactory.create()

        self.product_2 = ProductFactory.create()

        self.dimensions_1 = ProductDimensionFactory.create(
            product=self.product_1_no_lockers,
            length=100.00,
            width=30.00,
            height=10.00,
            weight=28.0,
        )

        self.dimensions_2 = ProductDimensionFactory.create(
            product=self.product_2, length=20.00, width=19.00, height=14.00, weight=4.0
        )

        """ Vendor  """
        self.vendor = InventoryFactory.create(id=1)
        self.vendor.products.add(self.product_1_no_lockers)
        self.vendor.products.add(self.product_2)

        """Vendor_2 products  """

        self.product_3_vendor_2 = ProductFactory.create()

        self.product_4_vendor_2 = ProductFactory.create()

        self.dimensions_3 = ProductDimensionFactory.create(
            product=self.product_3_vendor_2,
            length=50.00,
            width=30.00,
            height=20.00,
            weight=8.0,
        )

        self.dimensions_4 = ProductDimensionFactory.create(
            product=self.product_4_vendor_2,
            length=20.00,
            width=19.00,
            height=14.00,
            weight=4.0,
        )

        """Vendor_2"""
        self.vendor_2 = InventoryFactory.create(id=2)
        self.vendor.products.add(self.product_3_vendor_2)
        self.vendor.products.add(self.product_4_vendor_2)

    def test_check_items_valid_products(self):
        items = [{"product": self.product_1_no_lockers}, {"product": self.product_2}]

        result = Delivery.check_items(items)

        self.assertEqual(len(result), 2)
        self.assertIn(self.product_1_no_lockers, result)
        self.assertIn(self.product_2, result)

    def test_check_items_empty_list(self):
        items = []
        result = Delivery.check_items(items)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_check_items_nonexistent_product(self):

        items = {"product": 99999999}
        result = Delivery.check_items(items)

        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    def test_filter_dimensions_valid_product_for_all_except_none_can_use(self):
        result = Delivery.filter_dimensions(self.product_1_no_lockers)
        delivery_methods_without_lockers = Delivery.objects.filter(max_weight=50).all()
        self.assertIsNotNone(result)
        self.assertEqual(result.count(), len(delivery_methods_without_lockers))

    def test_filter_dimensions_product_too_big_for_locker(self):

        result = Delivery.filter_dimensions(self.product_1_no_lockers)

        self.assertIsNotNone(result)
        excluded_methods = result.filter(name__contains="Parcel lockers")
        self.assertEqual(excluded_methods.count(), 0)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "Standard In-house")

    def test_filter_deliveries_method_empty_items(self):
        result = Delivery.filter_deliveries_method([])
        self.assertIsNone(result)

    def test_multiply_vendor_products_with_single_product(self):
        product = [self.product_1_no_lockers]

        result = Delivery.multiply_vendor_products(product)

        self.assertIsInstance(result, dict)
        self.assertIn(self.vendor, result)
        self.assertIn("products", result[self.vendor])
        self.assertIn("deliveries", result[self.vendor])
        self.assertIn("selected_delivery", result[self.vendor])

    def test_multiply_vendor_products_method_with_4_products(self):
        products = [
            self.product_1_no_lockers,
            self.product_2,
            self.product_3_vendor_2,
            self.product_4_vendor_2,
        ]

        result = Delivery.multiply_vendor_products(products)

        self.assertIsInstance(result, dict)
        self.assertIn(self.vendor, result)
        self.assertIn("products", result[self.vendor])
        self.assertIn("deliveries", result[self.vendor])
        self.assertIn("selected_delivery", result[self.vendor])

    def test_delivery_price_total_without_products(self):
        result = Delivery.delivery_price_total({}, None)
        self.assertEqual(result, 0)

    def test_delivery_price_total_with_none_in_place_of_vendors(self):
        result = Delivery.delivery_price_total(None, None)
        self.assertEqual(result, 0)

    def test_full_delivery_filtering_workflow(self):

        items = [{"product": self.product_2}, {"product": self.product_1_no_lockers}]

        result = Delivery.filter_deliveries_method(items)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        vendor_keys = list(result.keys())
        self.assertTrue(len(vendor_keys) > 0)

        for vendor in result:
            self.assertIn("products", result[vendor])
            self.assertIn("deliveries", result[vendor])
            self.assertIn("selected_delivery", result[vendor])
