from django.core.exceptions import ValidationError


def validate_minimal_price(price: float):
    if price > 0:
        return price
    raise ValidationError("Can not set product price to zero")
