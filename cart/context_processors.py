from .cart import Cart


def items_number(request):
    number_of_items_in_cart = Cart(request).__len__()
    return {'number_of_items_in_cart': number_of_items_in_cart}
