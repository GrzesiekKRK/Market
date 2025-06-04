from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import RequestFactory, TestCase

from deliveries.factories import DeliveryFactory
from deliveries.models import Delivery
from inventories.factories import InventoryFactory
from products.consts import PRODUCT_UNITS_KILOGRAMS
from products.factories import ProductDimensionFactory, ProductFactory


class DeliveryModelTest(TestCase):
    def setUp(self):
        self.delivery_standard = DeliveryFactory.create_batch(5)

    def test_delivery_creation(self):
        self.assertEqual(self.delivery_standard.name, "Standard Parcel lockers")
        self.assertEqual(self.delivery_standard.price, Decimal("15.99"))
        self.assertEqual(self.delivery_standard.delivery_average_time, 3)
        self.assertEqual(self.delivery_standard.weight_unit, PRODUCT_UNITS_KILOGRAMS)

    def test_delivery_str_method(self):
        expected = "Delivery by Standard Parcel lockers  on average in 3 days "
        self.assertEqual(str(self.delivery_standard), expected)

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


class DeliveryStaticMethodsTest(TestCase):
    def setUp(self):
        self.delivery_that_non_of_products_can_use = Delivery.objects.create(
            name="Not Available Parcel lockers",
            id=3,
            price=Decimal("17.99"),
            delivery_average_time=3,
            max_length=Decimal("0.1"),
            max_width=Decimal("0.1"),
            max_height=Decimal("0.1"),
            max_weight=Decimal("0.1"),
        )

        self.delivery_parcel = Delivery.objects.create(
            name="Standard Parcel lockers",
            price=Decimal("15.99"),
            delivery_average_time=3,
            max_length=Decimal("30.0"),
            max_width=Decimal("20.0"),
            max_height=Decimal("15.0"),
            max_weight=Decimal("5.0"),
        )

        self.delivery_courier = Delivery.objects.create(
            name="Courier Delivery",
            price=Decimal("25.99"),
            delivery_average_time=2,
            max_length=Decimal("100.0"),
            max_width=Decimal("80.0"),
            max_height=Decimal("60.0"),
            max_weight=Decimal("25.0"),
        )
        """ Vendor products   """

        self.product_1 = ProductFactory.create()

        self.product_2 = ProductFactory.create()

        self.dimensions_1 = ProductDimensionFactory.create(
            product=self.product_1,
            length=50.00,
            width=30.00,
            height=20.00,
            weight=8.0,
        )

        self.dimensions_2 = ProductDimensionFactory.create(
            product=self.product_2, length=20.00, width=19.00, height=14.00, weight=4.0
        )

        """ Vendor  """
        self.vendor = InventoryFactory.create()
        self.vendor.products.add(self.product_1)
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
        items = [{"product": self.product_1}, {"product": self.product_2}]

        result = Delivery.check_items(items)

        self.assertEqual(len(result), 2)
        self.assertIn(self.product_1, result)
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
        result = Delivery.filter_dimensions(self.product_1)
        print(result)
        self.assertIsNotNone(result)
        self.assertEqual(result.count(), Delivery.objects.exclude(id=3).count())

    def test_filter_dimensions_product_too_big_for_locker(self):

        result = Delivery.filter_dimensions(self.product_1)

        self.assertIsNotNone(result)
        excluded_methods = result.filter(name__contains="Parcel lockers")
        self.assertEqual(excluded_methods.count(), 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Courier Delivery")

    def test_filter_deliveries_method_empty_items(self):
        result = Delivery.filter_deliveries_method([])
        self.assertIsNone(result)

    def test_multiply_vendor_products_with_single_product(self):
        product = [self.product_1]

        result = Delivery.multiply_vendor_products(product)
        self.assertIsInstance(result, dict)
        self.assertIn(self.vendor, result)
        self.assertIn("products", result[self.vendor])
        self.assertIn("deliveries", result[self.vendor])
        self.assertIn("selected_delivery", result[self.vendor])

    # TODO
    def test_multiply_vendor_products_method_with_4_products(self):
        products = [
            self.product_1,
            self.product_2,
            self.product_3_vendor_2,
            self.product_4_vendor_2,
        ]

        result = Delivery.multiply_vendor_products(products)
        print(result)
        self.assertIsInstance(result, dict)
        self.assertIn(self.vendor, result)
        self.assertIn("products", result[self.vendor])
        self.assertIn("deliveries", result[self.vendor])
        self.assertIn("selected_delivery", result[self.vendor])

    def test_get_delivery_method_default(self):
        factory = RequestFactory()
        request = factory.get("/")
        request.session = {}

        result = Delivery.get_delivery_method(request)

        self.assertEqual(result.id, 1)

    def test_get_delivery_method_with_invalid_id(self):
        factory = RequestFactory()
        request = factory.get("/")
        request.session = {"selected_delivery_id": 999999}

        result = Delivery.get_delivery_method(request)
        self.assertEqual(result.id, 1)

    def test_delivery_price_total_with_delivery_courier_selected_non_default_option(
        self,
    ):

        delivery_by_vendor = {self.vendor: {"selected_delivery": self.delivery_courier}}

        result = Delivery.delivery_price_total(delivery_by_vendor, None)

        self.assertEqual(result, self.delivery_courier.price)

    def test_delivery_price_total_without_products(self):
        result = Delivery.delivery_price_total({}, None)
        self.assertEqual(result, 0)

    def test_delivery_price_total_with_none_in_place_of_vendors(self):
        result = Delivery.delivery_price_total(None, None)
        self.assertEqual(result, 0)

    def test_selected_deliveries_with_default_option(self):
        delivery_by_vendor = {self.vendor: {"selected_delivery": self.delivery_parcel}}

        result = Delivery.selected_deliveries(delivery_by_vendor, None)
        self.assertIn(self.vendor.id, result)
        self.assertEqual(result[self.vendor.id], self.delivery_parcel)

    def test_selected_deliveries_with_non_default_option(self):
        """Test selected_deliveries z wybraną dostawą"""
        delivery_by_vendor = {self.vendor: {"selected_delivery": self.delivery_parcel}}
        get_selected_delivery = [self.delivery_courier]

        result = Delivery.selected_deliveries(delivery_by_vendor, get_selected_delivery)

        self.assertIn("vendor_id", result)
        self.assertEqual(result["vendor_id"], self.delivery_courier)


class DeliveryIntegrationTest(TestCase):
    def test_full_delivery_filtering_workflow(self):
        """Test pełnego procesu filtrowania dostaw"""
        items = [{"product": self.small_product}, {"product": self.big_product}]

        # Test całego procesu
        result = Delivery.filter_deliveries_method(items)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)

        # Sprawdź czy vendors są w wynikach
        vendor_keys = list(result.keys())
        self.assertTrue(len(vendor_keys) > 0)

        # Sprawdź strukturę danych dla każdego vendora
        for vendor in result:
            self.assertIn("products", result[vendor])
            self.assertIn("deliveries", result[vendor])
            self.assertIn("selected_delivery", result[vendor])

    def test_delivery_method_selection_workflow(self):
        """Test procesu wybierania metody dostawy"""
        factory = RequestFactory()
        request = factory.get("/")
        request.session = {"selected_delivery_id": self.courier_delivery.id}

        # Test pobierania wybranej metody
        selected = Delivery.get_delivery_method(request)
        self.assertEqual(selected, self.courier_delivery)

        # Test kalkulacji ceny
        delivery_by_vendor = {self.vendor_a: {"selected_delivery": selected}}

        total_price = Delivery.delivery_price_total(delivery_by_vendor, None)
        self.assertEqual(total_price, self.courier_delivery.price)
