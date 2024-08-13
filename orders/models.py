from django.db import models
from datetime import datetime
from products.models import Product
from users.models import CustomUser


class Order(models.Model):
    product = models.ManyToManyField(Product)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(default=datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product

    def sell(self):
        order_quantity = self.order_quantity
