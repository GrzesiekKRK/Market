from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from products.models import ProductImage
from users.consts import CUSTOMER_USER_ROLE_VENDOR
from users.permissions import account_role_required

from .models import Inventory


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
        products = (
            inventory.products.select_related("category")
            .prefetch_related("image")
            .all()
        )

        context["inventory"] = inventory
        context["products"] = self._get_paginated_queryset(products)
        context["images"] = ProductImage.objects.filter(
            product__in=inventory.products.all()
        )

        return context

    def _get_paginated_queryset(self, products: QuerySet):
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get("page")

        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1

        page_obj = paginator.get_page(page_number)

        return page_obj
