from django.db import models
from datetime import datetime
from products.models import Product
from users.models import CustomUser


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=6)
    date = models.DateTimeField(default=datetime.today)
    status = models.BooleanField(default=False)
    total_price = models.DecimalField(decimal_places=2, max_digits=6,)

    def __str__(self):
        return self.product

    def sell(self):
        order_quantity = self.order_quantity


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=6,)

    def total_price(self):
        product = self.product
        if product.is_sale:
            return product.quantity * product.sale_price
        else:
            return product.quantity * product.price
