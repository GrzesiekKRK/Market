from django.db import models

from products.models import Product
from users.models import CustomUser


class Wishlist(models.Model):
    """
    Represents a user's wishlist, where they can save products they are interested in.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} your wishlist"
