from django.http import HttpRequest

from .cart import Cart


def items_number(request: HttpRequest) -> dict[str, int]:
    """Context processor, displaying current number of products in the cart"""
    number_of_items_in_cart = Cart(request).__len__()
    return {"number_of_items_in_cart": number_of_items_in_cart}
