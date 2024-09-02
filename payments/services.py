from django.urls import reverse

from orders.models import Order, ProductOrder
from users.models import CustomUser

import stripe

from icecream import ic

DOMAIN = 'http://127.0.0.1:8000/'
"""


    session = stripe.checkout.Session.create(
            customer=stripe_customer.id,
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(credit_cost * 100),  # cents
                    'product_data': {
                        'name': 'Credits',
                        'description': 'Sphere-Engine credits',
                    },
                },
                'quantity': int(credits_amount)
            }],
            automatic_tax={
                'enabled': True,
            },
            mode='payment',
            success_url=reverse('se_billing_invoices') + f'?order={order_number}',
            cancel_url=reverse('se_account_upgrade2'),
            payment_intent_data={
                'metadata': {
                    'order': str(order_number),
                    'payment_type': 'one-time'
                },
            },
            metadata={
                'order': str(order_number),
                'payment_type': 'one-time'
            },
            invoice_creation={
                'enabled': True,
            },
        )
"""


def stripe_checkout_session(order):
    order = Order.objects.get(id=order.id)
    user = CustomUser.objects.get(id=order.customer.id)
    product = ProductOrder.objects.filter(order=order)
    session = stripe.checkout.Session.create(
        customer_email=user.email,
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'USD',
                'unit_amount': int(100 * 100), # product_order.price
                "product_data":
                    {
                        "name": product.name
                    },
                },
            'quantity': 1,
            },
        ],
        custom_fields=[
                        {
                            "key": "address", "label": {"custom": 'Address', 'type': 'custom'}, "type": "text",
                            "text": {"default_value": order.address}
                        },
                        {
                            "key": "postal_code", "label": {"custom": 'Postal Code', 'type': 'custom'}, "type": "text",
                            "text": {"default_value": order.postal_code}
                        }
                        ],
        mode='payment',
        success_url=DOMAIN + 'payments/success/' + f'{order.id}',
        cancel_url=DOMAIN + 'payments/cancel/' + f'{order.id}',
        automatic_tax={
                        'enabled': True,
                        },
        )
    ic(session)
    return session
