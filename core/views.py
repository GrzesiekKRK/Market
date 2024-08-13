from django.contrib.auth.views import TemplateView
from django.shortcuts import render


class DashboardView(TemplateView):
    template_name = "market/dashboard.html"


class ConcatView(TemplateView):
    template_name = "market/contact.html"


class CheckoutView(TemplateView):
    template_name = "market/checkout.html"


def testimonial(request):
    return render(request, "market/testimonial.html")
