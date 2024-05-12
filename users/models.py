from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ADMIN = 1
    VENDOR = 2
    USER = 3
    GUEST = 4

    ROLE_CHOICES = (
                    (ADMIN, 'Admin'),
                    (VENDOR, 'Vendor'),
                    (USER, 'User'),
                    (GUEST, 'Guest')
                    )

    email = models.EmailField(max_length=50, verbose_name='Email')
    pesel = models.CharField(max_length=11, unique=True, null=True, verbose_name='Pesel')
    bank_account = models.CharField(max_length=25, null=True, verbose_name='Bank Account Number')
    created_at = models.DateTimeField(auto_now_add=True)
    secondary_email = models.EmailField(max_length=50, verbose_name='Secondary Email')
    address = models.CharField(max_length=100, null=True, verbose_name='Address')
    status = models.BooleanField()
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    reviews = models.DecimalField(default=5.0)

    def __str__(self):
        return f"User {self.first_name} {self.last_name}"


