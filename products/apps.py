from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_defaults_category(sender, **kwargs):
    from .consts import CATEGORIES
    from .models import Category

    categories_to_create = [Category(name=name) for name in CATEGORIES]
    Category.objects.bulk_create(categories_to_create)


class ProductConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"

    def ready(self):
        post_migrate.connect(create_defaults_category, sender=self)
