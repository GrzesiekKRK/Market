from django.conf import settings
from django.db import models


from users.models import CustomUser
from wishlists.models import Wishlist
from products.models import Product

from icecream import ic


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, null=True)
    is_read = models.BooleanField(verbose_name='read', default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    body = models.TextField()

    def __str__(self):
        return f'Notification of user {self.user} {self.body}'

    @staticmethod
    def create_notification(user, wishlist, product):

        if wishlist:
            body = f"Product {product.name} is on sale. Regular price was {product.price} to sale price now is {product.sale_price}"
            note = Notification(user=user, wishlist=wishlist, product=product, title='special offer', body=body)
        else:
            body = f"Product {product.name} was bought. By kupujący , In quantityi ilośc on adress gdzie"
            note = Notification(user=user, product=product, title='sale', body=body)

        return note


