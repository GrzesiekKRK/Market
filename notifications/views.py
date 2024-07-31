from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView

from .models import Notification
from products.models import ProductImage

from icecream import ic


class NotificationListView(LoginRequiredMixin, TemplateView):
    template_name = 'notification/notification.html'

    def get_context_data(self, **kwargs):
        notification = Notification.objects.filter(user=self.request.user.id)

        context = super().get_context_data(**kwargs)
        context['messages'] = notification
        return context


class NotificationDetailView(LoginRequiredMixin, TemplateView):
    model = Notification
    template_name = 'notification/notification-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notification = Notification.objects.get(id=context['pk'])
        product = notification.product
        miniature = ProductImage.objects.get(product=product.id, miniature=True)
        context['notification'] = notification
        context['product'] = product
        context['miniature'] = miniature
        read = notification.is_read
        if not read:
            read = NotificationDetailView.read(notification)
        return context

    @staticmethod
    def read(notification):
        notification.is_read = True
        notification.save()
        return notification


class NotificationDeleteView(DeleteView):
    model = Notification
    template_name = 'notification/notification-delete.html'
    success_url = '/'
