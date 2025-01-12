from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DeleteView
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Notification
from inventories.models import Inventory
from orders.models import Order, ProductOrder
from users.models import CustomUser


class NotificationListTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "notification/notification.html"

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        notification = Notification.objects.filter(user=self.request.user.id).order_by(
            "is_read"
        )

        context = super().get_context_data(**kwargs)
        context["notifications"] = notification
        return context


class NotificationDetailTemplateView(LoginRequiredMixin, TemplateView):
    model = Notification
    template_name = "notification/notification-detail.html"

    def get_object(self, queryset=None) -> Notification:
        notification = get_object_or_404(Notification, pk=self.kwargs["pk"])

        if notification.user != self.request.user:
            raise Http404(
                "Notification not found or you don't have permission to view it."
            )
        return notification

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        context = super().get_context_data(**kwargs)
        notification = self.get_object()

        read = notification.is_read
        if not read:
            read = NotificationDetailTemplateView.read(notification)
        context["notification"] = notification
        context["title"] = notification.title
        context["body"] = notification.body

        return context

    @staticmethod
    def read(notification: Notification) -> Notification:
        notification.is_read = True
        notification.save()
        return notification


class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    template_name = "notification/notification_confirm_delete.html"
    success_url = "/products/"

    def get_object(self, queryset=None) -> Notification:
        notification = get_object_or_404(Notification, pk=self.kwargs["pk"])

        if notification.user != self.request.user:
            raise Http404(
                "Notification not found or you don't have permission to view it."
            )
        return notification

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        context = super().get_context_data(**kwargs)
        context["notification"] = self.get_object()
        return context


class OrderNotification:
    @staticmethod
    def buyer_notification(order: Order) -> Notification:
        buyer = CustomUser.objects.get(id=order.customer.id)
        title = f"Order {order.id} payment accepted"
        body = f"'Hi your payment was accepted. To see your order click: <a href=\"http://127.0.0.1:8000/order/detail/{order.id}\"><i class='fas fa-envelope me-2 text-secondary'></i>Open notification</a>'"
        notification = Notification(user=buyer, title=title, body=body)
        notification.save()
        return notification

    @staticmethod
    def unpacking_products(products_dict: dict) -> str:
        products = products_dict["products"]
        literal = ""
        for product, quantity in products.items():
            literal += " " + product + " " + quantity + "\r\n"

        return literal

    @staticmethod
    def vendor_notification(order: Order) -> Notification:
        title = f"The purchase of your products has been paid for in orders {order.id}"

        products_order = ProductOrder.objects.filter(order=order.id)
        dict_prod = {"products": {}}
        for product_order in products_order:
            inventory = Inventory.objects.get(product=product_order.product.id)
            if inventory:
                dict_prod["vendor"] = (
                    inventory.vendor.first_name + " " + inventory.vendor.last_name
                )
                dict_prod["products"].update(
                    {product_order.product.name: str(product_order.quantity)}
                )
        sold_products = OrderNotification.unpacking_products(dict_prod)
        body = f"Hi {dict_prod['vendor']} \n\n Sold products:{sold_products}"

        notification = Notification(user=inventory.vendor, title=title, body=body)
        notification.save()
        return notification
