from django.db import models


class Delivery(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField()
    delivery_average_time = models.IntegerField()

    def __str__(self):
        return f'Delivery by {self.name}  on average in {self.delivery_average_time} days '
