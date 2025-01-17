from django.db import models
from django.utils import timezone

from products.models import Product
from users.models import CustomUser


class Order(models.Model):
    """Represents an order placed by a customer, containing product and delivery details."""

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=6)
    date = models.DateTimeField(default=timezone.now)
    status = models.BooleanField(default=False)
    total_price = models.DecimalField(
        decimal_places=2,
        max_digits=6,
    )

    def __str__(self):
        return f"order {self.id} "


class ProductOrder(models.Model):
    """Represents a product in an order, with its quantity and price."""

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=6)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return f"Product {self.product.name} from order {self.order}, in {self.quantity} and price {self.price}"

    def total_price(self):
        """Calculates and returns the total price for the specific product in the order."""
        return self.quantity * self.price
