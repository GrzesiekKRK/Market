from django.db import models
from users.models import CustomUser
from products.models import Product


class Inventory(models.Model):
    """
    Connect CustomUser(Vendor) with his product
    Give vendor CRUD abilities for Product
    """

    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self) -> str:
        return f"{self.vendor.first_name} your inventory"

    class Meta:
        verbose_name_plural = "Inventories"
