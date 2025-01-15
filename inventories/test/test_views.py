from django.test import TestCase
from django.urls import reverse
from inventories.models import Inventory
from inventories.factories import InventoryFactory


from products.factories import ProductFactory
from users.factories import CustomUserFactory


class InventoryListTemplateViewTest(TestCase):
    def setUp(self) -> None:
        self.user = CustomUserFactory.create(role=2)
        self.factory = ProductFactory.create_batch(
            10,
        )
        self.inventory_factory = InventoryFactory.create(vendor=self.user)

    def test_get(self):
        self.client.force_login(self.user)
        inventory = Inventory.objects.last()
        for product in self.factory:
            inventory.products.add(product)

        vendor_products = inventory.products.all()
        response = self.client.get(reverse("vendor-inventory"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(vendor_products), 10)
        self.assertEqual(inventory.vendor.role, 2)  # vendor role
        self.assertTemplateUsed(response, "inventories/inventory.html")

    def test_get_invalid_user_role(self):
        user = CustomUserFactory.create(role=1)
        self.client.force_login(user)

        response = self.client.get(reverse("vendor-inventory"))
        self.assertEqual(response.status_code, 403)
