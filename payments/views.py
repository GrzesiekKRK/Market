from django.conf import settings
from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import stripe

from orders.models import Order, ProductOrder
from users.models import CustomUser
from inventories.models import Inventory
from notifications.models import Notification

from icecream import ic


class HomePageView(TemplateView):
    template_name = 'market/home.html'


stripe.api_key = settings.STRIPE_SECRET_KEY


def buyer_notification(order: Order) -> Notification:
    buyer = CustomUser.objects.get(id=order.customer.id)
    title = f"Order {order.id} payment accepted"
    body = f"'Hi your payment was accepted. To see your order click: <a href=\"http://127.0.0.1:8000/order/detail/{order.id}\"><i class='fas fa-envelope me-2 text-secondary'></i>Open notification</a>'"
    notification = Notification(user=buyer, title=title, body=body)
    notification.save()
    return notification


def vendor_notification(order: Order) -> Notification:
    buyer = CustomUser.objects.get(id=order.customer.id)# do adresu
    label = {'Name': buyer.first_name + ' ' + buyer.last_name, 'address': buyer.address}
    title = f"The purchase of your products has been paid for in orders {order.id}"
    products_order = ProductOrder.objects.filter(order=order.id)
    dict_prod = {}
    for product_order in products_order:
        inventory = Inventory.objects.get(product=product_order.product.id)
        if inventory:
            dict_prod['vendor'] = inventory.vendor.first_name + ' ' + inventory.vendor.last_name
            dict_prod[f'{product_order.product.name}'] = product_order.quantity
            dict_prod['address'] = label
        else:
            pass

    body = f"Lista zakupionych productów {dict_prod}"
    note = Notification(user=inventory.vendor, title=title, body=body)
    note.save()
    return note


class SuccessView(TemplateView):
    template_name = 'payments/success.html'


class CancelledView(TemplateView):
    template_name = 'payments/cancel.html'


@csrf_exempt
def stripe_webhook(request) -> HttpResponse:
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
        order_status = Order.objects.get(id=int(order_id['order_id']))
        order_status.status = True
        order_status.save()

        buyer = buyer_notification(order_status)
        vendor = vendor_notification(order_status)

    return HttpResponse(status=200)
