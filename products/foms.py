from django import forms

from .models import ProductImage, Product, Category


class AddProductForm(forms.ModelForm):
    name = forms.CharField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    price = forms.DecimalField()
    miniature_description = forms.CharField(max_length=100)
    description = forms.CharField(max_length=400)
    quantity = forms.DecimalField()
    units_of_measurement = forms.ChoiceField(choices=Product.UNITS_CHOICES)
    is_sale = forms.BooleanField(initial=False, required=False)
    sale_price = forms.DecimalField(initial=0.0)

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'miniature_description', 'description',  'quantity', 'units_of_measurement', 'is_sale', 'sale_price']


class ImageForm(forms.ModelForm):
    miniature = forms.ImageField()
    image = forms.FileField(widget=forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label="")

    class Meta:
        model = ProductImage
        fields = ['miniature', 'image']

    def __init__(self, *args, **kwargs):
        initial_images = kwargs.pop('initial_images', None)
        super().__init__(*args, **kwargs)

        if initial_images:
            print('Initial_Images')
            self.fields['image'].initial = initial_images


class UpdateImageForm(forms.ModelForm):
    miniature = forms.ImageField()
    images = forms.FileField(widget=forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label="")

    class Meta:
        model = ProductImage
        fields = ['miniature', 'image']

