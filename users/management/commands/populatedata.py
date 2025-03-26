from django.core.management.base import BaseCommand

from inventories.factories import InventoryFactory
from notifications.factories import NotificationFactory
from orders.factories import OrderFactory
from products.factories import ProductFactory, ProductImageFactory
from products.models import Product
from wishlists.factories import WishlistFactory

from ...factories import CustomUserFactory
from ...models import CustomUser


class Command(BaseCommand):
    """Creat Users, 5 x Notifications per user, and Inventory if user is vendor"""

    def handle(self, *args, **options) -> None:
        users = self.users_factories()
        self.notification_factories(users)
        self.inventory_product_factories(users)
        self.order_factories(users)

    @staticmethod
    def users_factories() -> CustomUser:
        users = CustomUserFactory.create_batch(
            20,
        )
        return users

    @staticmethod
    def notification_factories(users: CustomUser):
        for user in users:
            NotificationFactory.create_batch(5, user=user)

    @staticmethod
    def inventory_product_factories(users: CustomUser):
        for user in users:
            if user.role == 2:  # role 1 - moderator,  2 - vendor, 3 - user
                inventory = InventoryFactory(vendor=user)
                products = ProductFactory.create_batch(5)
                for product in products:
                    ProductImageFactory.create(product=product)
                    inventory.products.add(product)
                    sale = Product.objects.filter(is_sale=True).first()
                    if not sale:
                        sale_product = ProductFactory.create(is_sale=True)
                        ProductImageFactory.create(product=sale_product)
                        inventory.products.add(sale_product)
                Command.wishlist_factories(products)

    @staticmethod
    def wishlist_factories(products: Product):
        wishs = WishlistFactory.create_batch(5)

        for wish in wishs:
            for product in products:
                wish.products.add(product)

    @staticmethod
    def order_factories(users: CustomUser):
        for user in users:
            OrderFactory.create_batch(2, customer=user, address=user.address)
