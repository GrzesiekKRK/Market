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


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=6)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return f"Product {self.product.name} from order {self.order}, in {self.quantity} and price {self.price}"

    def total_price(self):
        return self.quantity * self.price

