from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import stripe

from orders.models import Order

from icecream import ic


class HomePageView(TemplateView):
    template_name = 'market/home.html'


stripe.api_key = settings.STRIPE_SECRET_KEY

"""
    <a href="{{ stripe_session_url }}">
                    <img src="{{ settings.HOST_CDN }}{% static 'img/stripe_button.png' %}" width="200" height="70"/>
                </a>
"""
"""
def prepare_stripe_subscription_checkout_session(cost: int, interval: int, order_number: str,
                                                 stripe_customer: 'stripe.Customer') -> 'stripe.checkout.Session':
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'USD',
                'product_data': {
                    'name': f'Sphere-Engine Subscription',
                    'description': f'Subscription for Sphere Engine services',
                },
                'unit_amount': cost * 100,  # cents
                'recurring': {
                    'interval': 'month',
                    'interval_count': interval
                },
            },
            'quantity': 1,
        }],
        mode='subscription',
        success_url=reverse('se_billing_invoices') + f'?order={order_number}',
        cancel_url=reverse('se_account_upgrade2'),
        automatic_tax={
            'enabled': True,
        },
        subscription_data={
            'metadata': {
                'order': str(order_number),
            }
        },
    )
    return session
    """

"""
    params['stripe_session_url'] = get_valid_stripe_session_url(stripe_session)
"""


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancel.html'


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
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
        qu = Order.objects.get(id=int(order_id['order_id']))
        qu.status = True
        qu.save()

    ic(order_id)
    return HttpResponse(status=200)


