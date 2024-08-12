from django.conf import settings
from decimal import Decimal
from products.models import Product
from icecream import ic


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False) -> None:
        """Change number of  products in cart"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price),
                                     'is_sale': int(product.is_sale),
                                     'sale_price': str(product.sale_price),
                                     }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.session.save()

    def remove(self, product):
        """Remove single product from cart """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
        self.session.save()

    def __iter__(self):
        """Get the product objects and add them to the cart """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['is_sale'] = item['is_sale']
            item['sale_price'] = Decimal(item['sale_price'])
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_sub_total_price(self):
        return sum(Decimal(item['sale_price']) * item['quantity'] if item['is_sale'] else Decimal(item['price']) * item['quantity'] for item
                   in self.cart.values())

    def clear(self):
        """
        Remove all items from the cart.
        """
        for key in list(self.cart.keys()):  # Use list() to create a copy of keys
            del self.cart[key]
        self.session.save()

