from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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

# class StripePaymentService:
#     ...

# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         checkout_session = stripe.checkout.Session.create(
#             line_items=[
#                 {
#                         # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
#                         'price': '{{PRICE_ID}}',
#                         'quantity': 1,
#                 },
#                 ],
#                 mode='payment',
#                 success_url=YOUR_DOMAIN + '/success.html',
#                 cancel_qurl=YOUR_DOMAIN + '/cancel.html',
#             )


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'



