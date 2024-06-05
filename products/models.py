from django.db import models


class Department(models.Model):
    """Divide products in to departments """
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Divide departments in to categorise """
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'


class Product(models.Model):
    """Products model """
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/product/')
    reviews = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=6, default=0,)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

