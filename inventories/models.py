from django.db import models

from products.models import Product
from users.models import CustomUser


class Inventory(models.Model):
    """Represents an inventory of a vendor (a seller's collection of products)."""

    vendor = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, help_text="Owner of this inventory"
    )
    products = models.ManyToManyField(
        Product, help_text="Products which are included in this inventory"
    )

    def __str__(self) -> str:
        return f"{self.vendor.first_name} your inventory"

    class Meta:
        verbose_name_plural = "Inventories"
