from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from .models import Inventory
from users.permissions import account_role_required

from products.models import ProductImage


from icecream import ic

VENDOR = 2


@method_decorator(account_role_required([VENDOR]), name='dispatch')
class VendorInventoryListView(TemplateView):
    """Display all existing products created by vendor"""
    template_name = 'inventories/inventory.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        inventory = Inventory.objects.get_or_create(vendor=self.request.user)
        context['inventory'] = inventory[0]
        context['products'] = inventory[0].product.all()
        context['images'] = ProductImage.objects.filter(product=1)

        return context


