from decimal import Decimal

from django.conf import settings
from django.http import HttpRequest

from deliveries.models import Delivery
from products.models import Product


class Cart:
    """Class that manages the shopping cart in the user's session.
    Stores products added to the cart and allows manipulation of its contents.
    """

    def __init__(self, request: HttpRequest) -> None:
        """Initializes the cart in the session context.

        Arguments:
                request: The HTTP request object containing session data.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(
        self, product: Product, quantity: int = 1, override_quantity: bool = False
    ) -> None:
        """Adds a product to the cart or changes its quantity.

        Arguments:
            product: The product object to add.
            quantity: The quantity of the product to add (default is 1).
            override_quantity: Whether to override the existing quantity or increase it.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "is_sale": int(product.is_sale),
                "sale_price": str(product.sale_price),
            }
        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.session.save()

    def remove(self, product: Product) -> None:
        """Removes a product from the cart.

        Arguments:
            product: The product to remove.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
        self.session.save()

    def __iter__(self) -> None:
        """Generates product objects from the cart with associated Product data.

        Returns:
            item: Each cart item (product with price, quantity, and other information).
        """
        product_ids = self.cart.keys()
        products = (
            Product.objects.select_related("dimension")
            .prefetch_related("inventory")
            .filter(id__in=product_ids)
        )
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = product
        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["is_sale"] = item["is_sale"]
            item["sale_price"] = Decimal(item["sale_price"])
            item["total_price"] = Decimal(item["price"]) * item["quantity"]
            item["sale_total_price"] = Decimal(item["sale_price"]) * item["quantity"]
            yield item

    def __len__(self) -> int:
        """Returns the number of products in the cart.

        Returns:
            int: The total number of products in the cart.
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_products_sub_total_price(self) -> int:
        """Calculates the sum of the products' prices in the cart (regular price or sale price).

        Returns:
            int: The total price of products in the cart.
        """
        return sum(
            (
                Decimal(item["sale_price"]) * item["quantity"]
                if item["is_sale"]
                else Decimal(item["price"]) * item["quantity"]
            )
            for item in self.cart.values()
        )

    def get_delivery_price(self) -> Decimal:
        """Adds delivery fee to the cart total price."""
        return self.get_sub_total_price() + Decimal(settings.DELIVERY_FEE)

    # TODO Sprawdzanie delivery dla wielu kupców
    def get_delivery_method(self, request: HttpRequest) -> {}:
        selected_delivery_id = request.session.get("selected_delivery_id")
        vendor_id = request.POST.get("vendor_id")
        if not selected_delivery_id:
            selected_delivery_id = 1
        selected_delivery = {vendor_id: Delivery.objects.get(id=selected_delivery_id)}
        return selected_delivery

    def clear(self) -> None:
        """Removes all products from the cart."""
        for key in list(self.cart.keys()):
            del self.cart[key]
        self.session.save()

    def calculate_shipping_cost(self, delivery_methods: dict) -> float:
        """
        Oblicza całkowity koszt dostawy na podstawie wybranych metod.
        """
        total_shipping = 0.0
        for delivery in delivery_methods.values():
            total_shipping += delivery.price
        return total_shipping

    # def update_delivery_method(self, request: HttpRequest) -> None:
    #     """
    #     Aktualizuje wybraną metodę dostawy dla konkretnego sprzedawcy.
    #     """
    #     if request.method == 'POST':
    #         vendor_id = request.POST.get('vendor_id')
    #         delivery_id = request.POST.get('delivery_method')
    #
    #         if vendor_id and delivery_id:
    #             selected_delivery_methods = request.session.get('selected_delivery_methods', {})
    #
    #             # Aktualizuj wybraną metodę dla tego sprzedawcy
    #             selected_delivery_methods[vendor_id] = delivery_id
    #
    #             # Zapisz zaktualizowany słownik w sesji
    #             request.session['selected_delivery_methods'] = selected_delivery_methods
    #
    #             # Zaktualizuj całkowity koszt dostawy
    #             delivery_methods = self.get_delivery_methods(request)
    #             total_shipping = self.calculate_shipping_cost(delivery_methods)
    #             request.session['total_shipping_price'] = total_shipping
    #
    #             # Zaktualizuj sumę końcową
    #             cart_total = request.session.get('cart_total', 0)
    #             request.session['grand_total'] = cart_total + total_shipping
