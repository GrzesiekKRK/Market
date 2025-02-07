from functools import wraps
from typing import Callable

from django.contrib.auth.models import PermissionDenied
from django.http import Http404

from inventories.models import Inventory


def product_owner_required() -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        def inner(request, *args, **kwargs) -> Callable:
            customer_user = request.user
            product_id = kwargs["pk"]

            # product_owner = get_object_or_404(Inventory, vendor=customer_user.id, products=product_id)
            try:
                product_owner = Inventory.objects.get(
                    vendor=customer_user.id, products=product_id
                )
            except Inventory.DoesNotExist:
                raise Http404(
                    "Product not found or you don't have permission to view it."
                )

            if not product_owner:
                raise PermissionDenied

            return func(request, *args, **kwargs)

        return inner

    return decorator
