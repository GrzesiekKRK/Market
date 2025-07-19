from django.http import HttpRequest

from .cart import Cart


def items_number(request: HttpRequest) -> dict[str, int]:
    """Context processor that returns the current number of products in the cart.

    Arguments:
        request: The HTTP request object, which contains the session data.

    Returns:
        A dictionary with a key 'number_of_items_in_cart' and its corresponding value
        as the total number of products in the user's cart.
    """
    number_of_items_in_cart = Cart(request).__len__()
    return {"number_of_items_in_cart": number_of_items_in_cart}
