import json
from typing import Any

import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from notifications.views import OrderNotification
from orders.models import Order


class SuccessTemplateView(LoginRequiredMixin, TemplateView):
    """
    Displays a success page after a successful payment has been made. It retrieves the order
    associated with the payment and checks if the customer is the one who placed the order.
    """

    template_name = "payments/success.html"

    def get_object(self, queryset=None) -> Order:
        """
        Retrieves the order associated with the payment, ensuring that the user is authorized
        to view the order.

            Args:
                queryset (QuerySet, optional): The queryset to filter the order.

            Returns:
                Order: The order object if found and the user is authorized to view it.

            Raises:
                Http404: If the order does not exist or the user is not authorized to view it.
        """
        order = get_object_or_404(Order, pk=self.kwargs["pk"])

        if order.customer != self.request.user:
            raise Http404("Order not found or you don't have permission to view it.")

        return order

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Adds the order to the context data for rendering the success template.

            Args:
                kwargs (dict): Additional arguments passed to the method.

            Returns:
                dict[str: Any]: The context data to pass to the template, including the order.
        """
        context = super().get_context_data(**kwargs)
        context["order"] = self.get_object()
        return context


class CancelledTemplateView(LoginRequiredMixin, TemplateView):
    """
    Displays a cancel page after a payment has been canceled. It retrieves the order associated
    with the canceled payment and checks if the customer is the one who placed the order.
    """

    template_name = "payments/cancel.html"

    def get_object(self, queryset=None) -> Order:
        """
        Retrieves the order associated with the canceled payment, ensuring that the user is authorized
        to view the order.

            Args:
                queryset (QuerySet, optional): The queryset to filter the order.

            Returns:
                Order: The order object if found and the user is authorized to view it.

            Raises:
                Http404: If the order does not exist or the user is not authorized to view it.
        """
        order = get_object_or_404(Order, pk=self.kwargs["pk"])

        if order.customer != self.request.user:
            raise Http404("Order not found or you don't have permission to view it.")

        return order

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Adds the order to the context data for rendering the cancel template.

            Args:
                kwargs (dict): Additional arguments passed to the method.

            Returns:
                dict[str: Any]: The context data to pass to the template, including the order.
        """
        context = super().get_context_data(**kwargs)
        context["order"] = self.get_object()
        return context


@csrf_exempt
def stripe_webhook(request: HttpRequest) -> HttpResponse:
    """
    Handles Stripe webhook events, specifically processing successful payment events
    ("charge.succeeded"). Updates the order status and sends notifications to both
    the buyer and the vendor.

    Args:
        request (HttpRequest): The HTTP request object containing the webhook payload
                                from Stripe.

    Returns:
        HttpResponse: A response indicating the success (200) or failure (400) of processing
                       the webhook.
    """
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    payload = request.body
    order = json.loads(payload.decode())
    order_id = order["data"]["object"]["metadata"]

    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)

    if event["type"] == "charge.succeeded":
        print("Payment was successful.")
        order_status = Order.objects.get(id=int(order_id["order_id"]))
        order_status.status = True
        order_status.save()

        OrderNotification.buyer_notification(order_status)
        OrderNotification.vendor_notification(order_status)

    return HttpResponse(status=200)
