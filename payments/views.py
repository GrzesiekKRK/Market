from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404
import json
import stripe

from orders.models import Order
from notifications.views import OrderNotification
from core.settings import STRIPE_SECRET_KEY, STRIPE_ENDPOINT_SECRET
from django.contrib.auth.mixins import LoginRequiredMixin
from icecream import ic


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/success.html'

    def get_object(self,  queryset=None):

        order = get_object_or_404(Order, pk=self.kwargs['pk'])

        if order.customer != self.request.user:
            raise Http404("Order not found or you don't have permission to view it.")

        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.get_object()
        return context


class CancelledTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/cancel.html'

    def get_object(self,  queryset=None):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])

        if order.customer != self.request.user:
            raise Http404("Order not found or you don't have permission to view it.")

        return order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.get_object()
        return context


@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    stripe.api_key = STRIPE_SECRET_KEY
    endpoint_secret = STRIPE_ENDPOINT_SECRET

    payload = request.body
    order = json.loads(payload.decode())
    order_id = order['data']['object']['metadata']

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'charge.succeeded':
        print("Payment was successful.")
        order_status = Order.objects.get(id=int(order_id['order_id']))
        order_status.status = True
        order_status.save()

        buyer = OrderNotification.buyer_notification(order_status)
        vendor = OrderNotification.vendor_notification(order_status)

    return HttpResponse(status=200)
