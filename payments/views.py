from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpRequest, HttpResponseRedirect
import json
import stripe

from orders.models import Order
from notifications.views import vendor_notification, buyer_notification
from core.settings import STRIPE_SECRET_KEY, STRIPE_ENDPOINT_SECRET

from icecream import ic


stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TemplateView):
    template_name = 'payments/success.html'


class CancelledTemplateView(TemplateView):
    template_name = 'payments/cancel.html'


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

        buyer = buyer_notification(order_status)
        vendor = vendor_notification(order_status)

    return HttpResponse(status=200)
