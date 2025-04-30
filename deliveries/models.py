from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from products.consts import PRODUCT_UNITS_KILOGRAMS


class Delivery(models.Model):
    """Delivery methods"""

    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)
    delivery_average_time = models.IntegerField()
    max_length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Length in cm",
        default=1,
        validators=[
            MinValueValidator(0.10, message="Length cannot be less than 0.10 cm"),
            MaxValueValidator(300.00, message="Length cannot be more than 300 cm"),
        ],
    )
    max_width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Width in cm",
        default=1,
        validators=[
            MinValueValidator(0.10, message="Width cannot be less than 0.10 cm"),
            MaxValueValidator(150.00, message="Width cannot be more than 150 cm"),
        ],
    )
    max_height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Height in cm",
        default=1,
        validators=[
            MinValueValidator(0.10, message="Height cannot be less than 0.10 cm"),
            MaxValueValidator(120.00, message="Height cannot be more than 120 cm"),
        ],
    )
    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Weight in kg",
        default=1,
        validators=[
            MinValueValidator(0.10, message="Weight cannot be less than 0.10 kg"),
            MaxValueValidator(50.00, message="Weight cannot be more than 50 kg"),
        ],
    )
    weight_unit = models.PositiveSmallIntegerField(
        default=PRODUCT_UNITS_KILOGRAMS, help_text="Weight unit only in kilograms"
    )

    def __str__(self):
        return (
            f"Delivery by {self.name}  on average in {self.delivery_average_time} days "
        )

    class Meta:
        verbose_name_plural = "Deliveries"
