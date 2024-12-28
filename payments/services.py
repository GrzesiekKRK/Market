from datetime import datetime


from orders.models import Order, ProductOrder
from products.models import ProductImage
from users.models import CustomUser
from core.settings import STRIPE_SECRET_KEY

import stripe


DOMAIN = 'http://127.0.0.1:8000/'
stripe.api_key = STRIPE_SECRET_KEY


def stripe_checkout_session(order: Order) -> stripe.checkout:
    user = CustomUser.objects.get(id=order.customer.id)
    line_items_list = []
    products = ProductOrder.objects.filter(order=order.id)

    for product in products:
        try:
            product_image = ProductImage.objects.get(product=product.product.id, miniature=True)

        except ProductImage.DoesNotExist:
            product_image = ProductImage(product=product.product)
            product_image.save()
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
