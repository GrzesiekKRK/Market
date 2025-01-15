from typing import Any
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Inventory
from users.permissions import account_role_required
from users.consts import CUSTOMER_USER_ROLE_VENDOR

from products.models import ProductImage


@method_decorator(account_role_required([CUSTOMER_USER_ROLE_VENDOR]), name="dispatch")
class InventoryListTemplateView(LoginRequiredMixin, TemplateView):
    """Display all existing products added by vendor"""

    template_name = "inventories/inventory.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        """
                Method that generates the context data to be passed to the template.

                **kwargs: Additional arguments passed to the method (e.g., URL variables).

                Returns:
                    dict[str, Any]: A dictionary with data that will be used in the template.
        """
        context = super().get_context_data(**kwargs)
        inventory, created = Inventory.objects.get_or_create(vendor=self.request.user)
        context["inventory"] = inventory
        context["products"] = inventory.products.all()
        context["images"] = ProductImage.objects.filter(product__in=inventory.products.all())

        return context
