from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order
from icecream import ic


class YourOrderListView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order.html'
    login_required = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(customer=self.request.user)
        ic(self.request.user.role)
        context['order'] = orders
        return context



