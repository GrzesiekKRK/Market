from django.db import models
from users.models import CustomUser
from products.models import Product


class Inventory(models.Model):
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.DecimalField(decimal_places=2, max_digits=6, default=0)

    def __str__(self):
        return f'You have {self.product_quantity} {self.product.name}s in inventory'

    class Meta:
        verbose_name_plural = 'Inventories'
