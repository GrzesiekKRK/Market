from django.core.validators import MaxValueValidator, MinValueValidator
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


class ProductDimension(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="dimension"
    )
    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Length in cm",
        validators=[
            MinValueValidator(0.10, message="Length cannot be less than 0.10 cm"),
            MaxValueValidator(300.00, message="Length cannot be more than 300 cm"),
        ],
    )
    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Width in cm",
        validators=[
            MinValueValidator(0.10, message="Width cannot be less than 0.10 cm"),
            MaxValueValidator(150.00, message="Width cannot be more than 150 cm"),
        ],
    )
    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Height in cm",
        validators=[
            MinValueValidator(0.10, message="Height cannot be less than 0.10 cm"),
            MaxValueValidator(120.00, message="Height cannot be more than 120 cm"),
        ],
    )
    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Weight in kg",
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0.10, message="Weight cannot be less than 0.10 kg"),
            MaxValueValidator(50.00, message="Weight cannot be more than 50 kg"),
        ],
    )
    weight_unit = models.PositiveSmallIntegerField(
        choices=Product.UNITS_CHOICES,
        default=product_units.PRODUCT_UNITS_KILOGRAMS,
        help_text="Weight unit",
    )

    def __str__(self):
        return f"Wymiary produktu: {self.product.name}"

    # TODO Forma, liczenie przez mnożenie, waga

    ...


# 10x15x5 -> wymiar pudełka


"""
Długość (L) = dłuższy z wymiarów w ustawieniu do otwarcia opakowania. Szerokość (B) = krótszy z wymiarów w ustawieniu do otwarcia opakowania.
Wysokość (H) = wymiar pomiędzy podstawa a góra opakowania.


30x20x10

paczką średnia jest do 70x40x15

90x40x15
2
2
2

90x40x20 4


   30 30 30
20 1 1 1  -> 40
20 2 2  20 -> 8

1 1
1 1
1 1

1200mm:300mm = 4 sztuki
800mm:200mm = 4 sztuki
liczba kartonów na jednej warstwie 4*4 = 16 sztuk
waga pojedynczej warstwy=16 sztuk*5 kg (waga kartonu)= 80 kg
1200mm (maksymalna wysokość)- 144mm(wysokość pustej palety) = 1056mm:100mm (wysokość kartonu) =10 warstw
Liczba kartonów na jednej palecie euro:16 sztuk (jedna warstwa)*10 warstw= 160 sztuk kartonów.
10 warstw* 80kg (waga pojedynczej warstwy)=800kg (waga 10 warstw kartonów, nie licząc wagi pustej palety)
waga brutto pojedynczej palety: 800kg+25kg=825kg

Kupujący wybuera metode dostawy, vendor podaje gabaryty produktu z wagą,
paczkomat lub kurire dom lub punkt odn=bioru,
od jakieś kwoty dostawa za friko, a jak nie to zakazfdy produkt 20pln

30x20x10

90x30x20

90 / 30 = 3
30 / 20 = 1
20 / 10 = 2

6

2
2
2

30x20x15

90 / 30 = 3
30 / 20 = 1
30 / 15 = 1

3 * 1 * 1



90x55x40

90 / 30 = 3
55 / 20 = 2
40 / 10 = 4

3x2x4 = 24

4 4 4
4 4 4

4 4
4 4
4 4

"""
