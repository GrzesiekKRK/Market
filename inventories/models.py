from django.db import models
from users.models import CustomUser
from products.models import Product


class Inventory(models.Model):
    vendor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return f'You have products in inventory'

    class Meta:
        verbose_name_plural = 'Inventories'
