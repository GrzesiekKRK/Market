from django.db import models


class Delivery(models.Model):
    """Delivery methods"""
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)
    delivery_average_time = models.IntegerField()

    def __str__(self):
        return f'Delivery by {self.name}  on average in {self.delivery_average_time} days '

    class Meta:
        verbose_name_plural = 'Deliveries'
