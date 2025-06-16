from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from deliveries.consts import DELIVERY_CHOICES
from inventories.models import Inventory
from products.consts import PRODUCT_UNITS_KILOGRAMS
from products.models import Product, ProductDimension


class Delivery(models.Model):
    id = models.PositiveSmallIntegerField(
        choices=DELIVERY_CHOICES,
        primary_key=True,
    )
    name = models.CharField(choices=DELIVERY_CHOICES, max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=5.0)
    delivery_average_time = models.IntegerField()
    max_length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Length in cm",
        default=300,
        validators=[
            MinValueValidator(0.10, message="Length cannot be less than 0.10 cm"),
            MaxValueValidator(300.00, message="Length cannot be more than 300 cm"),
        ],
    )
    max_width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Width in cm",
        default=150,
        validators=[
            MinValueValidator(0.10, message="Width cannot be less than 0.10 cm"),
            MaxValueValidator(150.00, message="Width cannot be more than 150 cm"),
        ],
    )
    max_height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Height in cm",
        default=120,
        validators=[
            MinValueValidator(0.10, message="Height cannot be less than 0.10 cm"),
            MaxValueValidator(120.00, message="Height cannot be more than 120 cm"),
        ],
    )
    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Weight in kg",
        default=50,
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
            try:
                product = get_object_or_404(Product, id=item["product"].id)
                if product:
                    list_products.append(product)
            except (TypeError, ValueError):
                continue
        return list_products

    @staticmethod
    def filter_dimensions(product) -> None | QuerySet:
        product = get_object_or_404(ProductDimension, product=product)
        delivery_parcel = get_object_or_404(Delivery, id=1)
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

    @staticmethod
    def filter_deliveries_method(items: {Product}) -> {} | {Inventory: Product}:
        if not items:
            return None
        list_products = Delivery.check_items(items)
        deliveries_by_vendor = Delivery.multiply_vendor_products(list_products)

        return deliveries_by_vendor

    @staticmethod
    def multiply_vendor_products(list_products) -> {} | {Inventory: str}:
        his_products = {}
        deliveries_methods_all = Delivery.objects.all()
        vendor_package = 0
        for product in list_products:
            vendor = get_object_or_404(Inventory, products=product)

            if vendor:
                if vendor in his_products:
                    his_products[vendor]["products"] = his_products[vendor][
                        "products"
                    ] + [product]

                    if len(vendor_package) == len(deliveries_methods_all):
                        vendor_package = Delivery.filter_dimensions(product)

                        if len(vendor_package) < len(deliveries_methods_all):
                            his_products[vendor]["deliveries"] = [vendor_package]

                else:
                    vendor_package = Delivery.filter_dimensions(product)
                    his_products[vendor] = {
                        "products": [product],
                        "deliveries": vendor_package,
                        "selected_delivery": Delivery.objects.get(id=1),
                    }

        return his_products

    # TODO Comments/check typing all
    @staticmethod
    def delivery_price_total(delivery_by_vendor, get_selected_delivery) -> int:
        if delivery_by_vendor:
            deliveries_price = 0
            if get_selected_delivery:
                for vendor in delivery_by_vendor:
                    deliveries_price += delivery_by_vendor[vendor][
                        "selected_delivery"
                    ].price

            return deliveries_price
        return 0
