from datetime import datetime

from orders.models import Order, ProductOrder
from products.models import ProductImage
from users.models import CustomUser

import stripe

from icecream import ic

DOMAIN = 'http://127.0.0.1:8000/'


def stripe_checkout_session(order: Order) -> stripe.checkout:
    user = CustomUser.objects.get(id=order.customer.id)
    line_items_list = []
    products = ProductOrder.objects.filter(order=order)

    for product in products:

        product_image = ProductImage.objects.get(product=product.product.id, miniature=True)
        miniature = [DOMAIN + product_image.image.url]
        stripe_product = {
                            'quantity': int(product.quantity),
                            'price_data': {
                                            'currency': 'USD',
                                            'unit_amount_decimal': str(product.price * 100),
                                            'product_data': {
                                                            'name': product.product.name,
                                                            'description': product.product.description,
                                                            'images': miniature
                                                            }
                                            },
                    }
        line_items_list.append(stripe_product)

    session = stripe.checkout.Session.create(
        customer_email=user.email,
        payment_method_types=['card'],
        line_items=line_items_list,
        custom_fields=[
                        {
                            "key": "address", "label": {"custom": 'Address', 'type': 'custom'}, "type": "text",
                            "text": {"default_value": order.address}
                        },
                        {
                            "key": "postal_code", "label": {"custom": 'Postal Code', 'type': 'custom'}, "type": "text",
                            "text": {"default_value": order.postal_code}
                        },
                        ],
        mode='payment',
        success_url=DOMAIN + 'payments/success/' + f'{order.id}',
        cancel_url=DOMAIN + 'payments/cancel/' + f'{order.id}',
        automatic_tax={
                        'enabled': True,
                        },
        metadata={
                    'order_id': str(order.id)
                    },
        payment_intent_data={
                                "metadata": {
                                                'order_id': order.id,
                                            }
        }
        )

    return session
