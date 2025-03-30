import django_filters
from django import forms

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    is_sale = django_filters.BooleanFilter(widget=forms.CheckboxInput())
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["name", "category", "reviews", "is_sale"]
