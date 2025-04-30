from django import forms

from .models import Category, Product, ProductDimension, ProductImage


class AddProductForm(forms.ModelForm):
    name = forms.CharField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    price = forms.DecimalField(help_text="Enter price in Dollars")
    miniature_description = forms.CharField(max_length=100, help_text="Limit 100 marks")
    description = forms.CharField(max_length=400, help_text="Limit 400 marks")
    quantity = forms.DecimalField(
        help_text="Enter quantity in which product is available"
    )
    units_of_measurement = forms.ChoiceField(
        choices=Product.UNITS_CHOICES, help_text="Select units of measurement"
    )
    is_sale = forms.BooleanField(
        initial=False, required=False, help_text="Check if product is on sale"
    )
    sale_price = forms.DecimalField(
        initial=0.1, help_text="Enter sale price in Dollars"
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "price",
            "miniature_description",
            "description",
            "quantity",
            "units_of_measurement",
            "is_sale",
            "sale_price",
        ]


class ProductDimensionForm(forms.ModelForm):
    length = forms.DecimalField(decimal_places=2, max_digits=6, initial=1)
    width = forms.DecimalField(decimal_places=2, max_digits=6, initial=1)
    height = forms.DecimalField(decimal_places=2, max_digits=6, initial=1)
    weight = forms.DecimalField(decimal_places=2, max_digits=6, initial=1)
    weight_unit = forms.ChoiceField(
        choices=[choice for choice in Product.UNITS_CHOICES if choice != 1], initial=3
    )

    class Meta:
        model = ProductDimension
        fields = ["length", "width", "height", "weight"]


class ImageForm(forms.ModelForm):
    miniature = forms.ImageField()
    image = forms.FileField(
        widget=forms.TextInput(
            attrs={
                "name": "images",
                "type": "File",
                "class": "form-control",
                "multiple": "True",
            }
        ),
        label="",
    )

    class Meta:
        model = ProductImage
        fields = ["miniature", "image"]

    def __init__(self, *args, **kwargs):
        initial_images = kwargs.pop("initial_images", None)
        super().__init__(*args, **kwargs)

        if initial_images:
            print("Initial_Images")
            self.fields["image"].initial = initial_images


class UpdateImageForm(forms.ModelForm):
    miniature = forms.ImageField()
    images = forms.FileField(
        widget=forms.TextInput(
            attrs={
                "name": "images",
                "type": "File",
                "class": "form-control",
                "multiple": "True",
            }
        ),
        label="",
    )

    class Meta:
        model = ProductImage
        fields = ["miniature", "image"]
