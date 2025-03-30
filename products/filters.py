import django_filters
from django import forms

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    is_sale = django_filters.BooleanFilter(widget=forms.CheckboxInput())
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")

    ordering = django_filters.OrderingFilter(
        label="Sort by",
        choices=(
            ("price", "Price (Low to High)"),
            ("-price", "Price (High to Low)"),
            ("name", "Name (A to Z)"),
            ("-name", "Name (Z to A)"),
            ("average_rating", "Rating (Low to High)"),
            ("-average_rating", "Rating (High to Low)"),
        ),
        fields={
            "price": "price",
            "name": "name",
            "created_at": "created_at",
            "average_rating": "average_rating",
        },
        field_labels={
            "price": "Price",
            "name": "Name",
            "created_at": "Date",
            "average_rating": "Rating",
        },
    )

    class Meta:
        model = Product
        fields = ["name", "category", "is_sale"]
