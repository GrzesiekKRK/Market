from django.conf import settings
from django.db import models


from users.models import CustomUser
from wishlists.models import Wishlist
from products.models import Product
from orders.models import Order
from icecream import ic


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(verbose_name='read', default=False)
    title = models.CharField(max_length=50)
    body = models.TextField()

    def __str__(self):
        return f'Notification of user {self.user} {self.body}'


