from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from inventories.models import Inventory
from products.consts import PRODUCT_UNITS_KILOGRAMS
from products.models import Product, ProductDimension


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

    @staticmethod
    def check_items(items: {Product}) -> list[Product]:
        list_products = []

        for item in items:
            product = get_object_or_404(Product, id=item["product"].id)
            if product:
                list_products.append(product)
        return list_products

    @staticmethod
    def filter_dimensions(product) -> None | QuerySet:
        product = get_object_or_404(ProductDimension, product=product)
        delivery_parcel = get_object_or_404(
            Delivery, name__contains="Standard Parcel lockers"
        )
        if delivery_parcel:
            product_length, product_width = product.length, product.width
            product_height, product_weight = product.height, product.weight
            if (
                product_length <= delivery_parcel.max_length
                and product_width <= delivery_parcel.max_width
                and product_height <= delivery_parcel.max_height
                and product_weight <= delivery_parcel.max_weight
            ):
                filtered_methods = Delivery.objects.all()
            else:
                filtered_methods = Delivery.objects.all().exclude(
                    name__contains="Parcel lockers"
                )
            return filtered_methods
        return None

    # TODO testy deliveries
    @staticmethod
    def filter_deliveries_method(items: {Product}) -> {}:
        if not items:
            return None
        list_products = Delivery.check_items(items)
        deliveries_by_vendor = Delivery.multiply_vendor_products(list_products)
        return deliveries_by_vendor

        # TODO zapisalem w deliveries views
        # TODO Cart z podziałem na sprzedających oraz ich mozliwościami wysylki w template
        # TODO logica podziału sprzedajćy oraz produkty
        # TODO Cena jednej paczki poprostu od każdego

    @staticmethod
    def multiply_vendor_products(list_products):
        his_products = {}
        deliveries_methods_all = Delivery.objects.all()
        vendor_package = 0
        for product in list_products:
            vendor = get_object_or_404(Inventory, products=product)
            if vendor:
                if vendor in his_products:
                    his_products[vendor] = his_products[vendor] + [product]

                    if len(vendor_package) == len(deliveries_methods_all):
                        vendor_package = Delivery.filter_dimensions(product)

                        if len(vendor_package) < len(deliveries_methods_all):
                            his_products[vendor.id] = [vendor_package]

                    his_products[vendor] = [product]
                    vendor_package = Delivery.filter_dimensions(product)
                    his_products[vendor.id] = [vendor_package]

                else:
                    his_products[vendor] = [product]
                    vendor_package = Delivery.filter_dimensions(product)
                    his_products[vendor.id] = [vendor_package]
        return his_products
