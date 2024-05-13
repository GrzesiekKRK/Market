from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')
    quantity = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    reviews = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)

    is_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(decimal_places=2, max_digits=6, default=0,)

    def __str__(self):
        return self.name

