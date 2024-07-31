from django.contrib.auth.views import TemplateView
from django.shortcuts import render


class DashboardView(TemplateView):
    template_name = "market/dashboard.html"


class ConcatView(TemplateView):
    template_name = "market/contact.html"


def checkout(request):
    return render(request, "market/checkout.html")


def testimonial(request):
    return render(request, "market/testimonial.html")
