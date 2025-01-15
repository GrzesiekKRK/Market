from django.db import models
from users.models import CustomUser
from products.models import Product


class Inventory(models.Model):
    """Represents an inventory of a vendor (a seller's collection of products)."""
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self) -> str:
        return f"{self.vendor.first_name} your inventory"

    class Meta:
        verbose_name_plural = "Inventories"
