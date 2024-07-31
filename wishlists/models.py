from django.db import models
from users.models import CustomUser
from products.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return f" {self.user.first_name} {self.user.first_name} your wishlist"

