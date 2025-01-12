from django.test import TestCase
from inventories.models import Inventory
from inventories.factories import InventoryFactory

from users.factories import CustomUserFactory


class InventoryModelTest(TestCase):

    def setUp(self) -> None:
        self.user = CustomUserFactory.create(role=2)
        self.inventory_factory = InventoryFactory.create(vendor=self.user)

    def test_model_str_method_output(self):
        inventory = Inventory.objects.last()
        first_name = inventory.vendor.first_name

        self.assertEqual(str(inventory), f"{first_name} your inventory")
        self.assertIsInstance(inventory, Inventory)
