from django.db import models
from . import consts as product_units


class Category(models.Model):
    """Divide products in to categorise """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class Product(models.Model):

    UNITS_CHOICES = (
        (product_units.PRODUCT_UNITS_PIECE, 'Piece'),
        (product_units.PRODUCT_UNITS_GRAMS, 'Grams'),
        (product_units.PRODUCT_UNITS_KILOGRAMS, 'Kilograms'),
        (product_units.PRODUCT_UNITS_LITERS, 'Liters'),
    )

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    miniature_description = models.CharField(max_length=100, default='', blank=True, null=True)
    description = models.CharField(max_length=400, default='', blank=True, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=9, default=1)
    units_of_measurement = models.PositiveSmallIntegerField(choices=UNITS_CHOICES, default=product_units.PRODUCT_UNITS_PIECE)
    reviews = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)
    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=6, default=0,)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    miniature = models.BooleanField(default=False)
    image = models.FileField(upload_to='uploads/product/', default='uploads/product/default.jpg')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')


