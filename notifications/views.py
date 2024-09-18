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

        read = notification.is_read
        if not read:
            read = NotificationDetailView.read(notification)
        context['notification'] = notification
        context['title'] = notification.title
        context['body'] = notification.body
        ic(context)
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
