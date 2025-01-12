from django.db import models
from users.models import CustomUser
from products.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self) -> str:
        return f" {self.user.first_name} {self.user.last_name} your wishlist"
