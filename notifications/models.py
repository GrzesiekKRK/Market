
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

    def __str__(self):
        return f"Notification of user {self.user} {self.body}"
