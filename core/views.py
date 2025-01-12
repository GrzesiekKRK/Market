from django.contrib.auth.views import TemplateView


class DashboardView(TemplateView):
    template_name = "market/dashboard.html"


class ConcatView(TemplateView):
    template_name = "market/contact.html"
