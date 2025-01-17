from django.contrib.auth.models import AbstractUser
from django.db import models

from . import consts as users_role


class CustomUser(AbstractUser):
    """
    Custom user model extending the base AbstractUser to include additional fields
    specific to the application. This includes role management, user-specific
    information, and secondary contact details.
    """

    ROLE_CHOICES = (
        (users_role.CUSTOMER_USER_ROLE_MODERATOR, "Moderator"),
        (users_role.CUSTOMER_USER_ROLE_VENDOR, "Vendor"),
        (users_role.CUSTOMER_USER_ROLE, "User"),
    )

    email = models.EmailField(max_length=50, verbose_name="Email")
    pesel = models.CharField(
        max_length=11, unique=True, null=True, verbose_name="Pesel"
    )
    bank_account = models.CharField(
        max_length=25, null=True, verbose_name="Bank Account Number"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    secondary_email = models.EmailField(max_length=50, verbose_name="Secondary Email")
    address = models.CharField(max_length=100, null=True, verbose_name="Address")
    postal_code = models.CharField(
        max_length=6, verbose_name="Postal Code", default="32-856"
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    reviews = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
