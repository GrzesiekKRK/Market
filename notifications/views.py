from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from .models import Notification

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
        context['notification'] = notification

        return context
