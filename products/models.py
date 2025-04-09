from django.db import models

from products.validators import validate_minimal_price

from . import consts as product_units


class Category(models.Model):
    """
    Represents a product category. Categories are used to group products together
    for easier browsing and searching.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"


class Product(models.Model):
    """
    Represents a product that is available for purchase. Each product belongs to
    a category, and can have a price, description, and reviews. Products can also
    have a sale price if they are on sale.
    """

    UNITS_CHOICES = (
        (product_units.PRODUCT_UNITS_PIECE, "Piece"),
        (product_units.PRODUCT_UNITS_GRAMS, "Grams"),
        (product_units.PRODUCT_UNITS_KILOGRAMS, "Kilograms"),
        (product_units.PRODUCT_UNITS_LITERS, "Liters"),
    )

    name = models.CharField(max_length=100, help_text="Does not need to be unique")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category",
        help_text="Check for similar products",
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=6, default=1, validators=[validate_minimal_price]
    )
    miniature_description = models.CharField(
        max_length=100, default="", blank=True, null=True, help_text="Limit 100 marks"
    )
    description = models.CharField(
        max_length=400, default="", blank=True, null=True, help_text="Limit 400 marks"
    )
    quantity = models.DecimalField(decimal_places=2, max_digits=9, default=1)
    units_of_measurement = models.PositiveSmallIntegerField(
        choices=UNITS_CHOICES, default=product_units.PRODUCT_UNITS_PIECE
    )
    reviews = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(
        decimal_places=2, max_digits=6, default=1, validators=[validate_minimal_price]
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    Represents an image associated with a product. A product can have multiple images,
    including miniature images used for product previews.
    """

    miniature = models.BooleanField(
        default=False, help_text="This image will be display on dashboard"
    )
    image = models.FileField(
        upload_to="uploads/product/", default="uploads/product/default.jpg"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="image")
