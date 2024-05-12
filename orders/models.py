from django.db import models
from datetime import datetime
from products.models import Product
from users.models import CustomUser


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    date = models.DateTimeField(default=datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.product
