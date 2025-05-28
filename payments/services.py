import stripe
from django.conf import settings

from orders.models import Order, ProductOrder
from products.models import ProductImage
from users.models import CustomUser

DOMAIN = "http://127.0.0.1:8000/"


def stripe_checkout_session(order: Order) -> stripe.checkout:
    """
    Creates a Stripe checkout session for processing payments. This session contains
    the items in the order, customer details, and payment configurations, and it is
    used to redirect the user to the Stripe payment page.

        Args:
            order (Order): The order for which the Stripe checkout session is being created.
                           It contains customer details, products, prices, and shipping information.

        Returns:
        stripe.checkout.Session: A Stripe checkout session object that will be used
                                    to initiate the payment process on the Stripe platform.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY

    user = CustomUser.objects.get(id=order.customer.id)
    line_items_list = []
    products = ProductOrder.objects.filter(order=order.id)

    for product in products:
        try:
            product_image = ProductImage.objects.get(
                product=product.product.id, miniature=True
            )

        except ProductImage.DoesNotExist:
            product_image = ProductImage(product=product.product)
            product_image.save()
        miniature = [DOMAIN + product_image.image.url]
        stripe_product = {
            "quantity": int(product.quantity),
            "price_data": {
                "currency": "USD",
                "unit_amount_decimal": str(product.price * 100),
                "product_data": {
                    "name": product.product.name,
                    "description": product.product.description,
                    "images": miniature,
                },
            },
        }
        line_items_list.append(stripe_product)

    session = stripe.checkout.Session.create(
        customer_email=user.email,
        payment_method_types=["card"],
        line_items=line_items_list,
        custom_fields=[
            {
                "key": "address",
                "label": {"custom": "Address", "type": "custom"},
                "type": "text",
                "text": {"default_value": order.address},
            },
            {
                "key": "postal_code",
                "label": {"custom": "Postal Code", "type": "custom"},
                "type": "text",
                "text": {"default_value": order.postal_code},
            },
        ],
        mode="payment",
        success_url=DOMAIN + f"payments/{order.id}/success",
        cancel_url=DOMAIN + f"payments/{order.id}/cancel",
        automatic_tax={
            "enabled": True,
        },
        metadata={"order_id": str(order.id)},
        payment_intent_data={
            "metadata": {
                "order_id": order.id,
            }
        },
    )

    return session
