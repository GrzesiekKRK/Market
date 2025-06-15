from django.conf import settings
from django.db import models

from users.models import CustomUser


class Notification(models.Model):
    """Represents a notification of events like payment acceptance, wishlist product sale,
    and informing the vendor of sales.

    This model is used to store notifications for users, which can be read or unread.
    It helps keep users informed about various events or updates in the system.
    """

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notifications"
    )
    is_read = models.BooleanField(verbose_name="read", default=False)
    title = models.CharField(max_length=100)
    body = models.TextField()

    def __str__(self) -> str:
        return f"Notification of user {self.user} {self.body}"

    @staticmethod
    def create_wishlist_notification(wishlist_owner, product) -> None:
        title = f"Special Offer: {product.name}"
        body = f"<a href =\"{settings.SITE_URL}/products/detail/{product.id}\"><i class='fas fa-envelope me-2 text-secondary'></i>{product.name}</a>"
        user = CustomUser.objects.get(id=wishlist_owner.user.id)
        notification = Notification(user=user, title=title, body=body)
        notification.save()
