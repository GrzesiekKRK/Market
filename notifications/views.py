from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import DeleteView, TemplateView

from inventories.models import Inventory
from orders.models import Order, ProductOrder
from users.models import CustomUser

from .models import Notification


class NotificationListTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "notification/notification.html"

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Retrieves notifications for the logged-in user and passes them to the template.
        The notifications are ordered by their 'is_read' status, so unread notifications
        appear first.

        Args:
            **kwargs: Additional keyword arguments passed to the method.
                      This includes any URL variables or context data.

        Returns:
            dict[str, Any]: A dictionary of context data for rendering the template.
                             Contains the list of notifications under the key 'notifications'.
        """
        notification = Notification.objects.filter(user=self.request.user.id).order_by(
            "is_read"
        )
        paginator = Paginator(notification, 12)
        page_number = self.request.GET.get("page")
        try:
            page_number = int(page_number)
        except (TypeError, ValueError):
            page_number = 1
        page_obj = paginator.get_page(page_number)
        context = super().get_context_data(**kwargs)
        context["notifications"] = page_obj
        return context


class NotificationDetailTemplateView(LoginRequiredMixin, TemplateView):
    model = Notification
    template_name = "notification/notification-detail.html"

    def get_object(self, queryset=None) -> Notification:
        """
        Retrieves the notification based on its primary key (pk).
        Only allows access if the notification belongs to the logged-in user.

        Args:
            queryset (QuerySet, optional): A queryset used to fetch the object (not used here).

        Returns:
            Notification: The notification object associated with the provided pk.

        Raises:
            Http404: If the notification is not found or the logged-in user does not have permission.
        """
        notification = get_object_or_404(Notification, pk=self.kwargs["pk"])

        if notification.user != self.request.user:
            raise Http404(
                "Notification not found or you don't have permission to view it."
            )
        return notification

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Retrieves the context for the notification details page and marks the notification as read.

        Args:
            **kwargs: Additional keyword arguments passed to the method.
                      This includes any URL variables or context data.

        Returns:
            dict[str, Any]: A dictionary of context data, including the notification's title, body,
                             and read status.
        """
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
        """
        Marks the given notification as read and saves it.

        Args:
            notification (Notification): The notification instance to mark as read.

        Returns:
            Notification: The updated notification instance with is_read set to True.
        """
        notification.is_read = True
        notification.save()
        return notification


class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    """Handles the deletion of a notification."""

    model = Notification
    template_name = "notification/notification_confirm_delete.html"
    success_url = "/products/"

    def get_object(self, queryset=None) -> Notification:
        """
        Retrieves the notification to be deleted.
        Ensures the notification belongs to the logged-in user before allowing deletion.

        Args:
            queryset (QuerySet, optional): A queryset used to fetch the object (not used here).

        Returns:
            Notification: The notification instance that will be deleted.

        Raises:
            Http404: If the notification does not exist or the logged-in user does not have permission.
        """
        notification = get_object_or_404(Notification, pk=self.kwargs["pk"])

        if notification.user != self.request.user:
            raise Http404(
                "Notification not found or you don't have permission to view it."
            )
        return notification

    def get_context_data(self, **kwargs) -> dict[str:Any]:
        """
        Passes the notification to the context so the user can confirm its deletion.

        Args:
            **kwargs: Additional keyword arguments passed to the method.
                      This includes any URL variables or context data.

        Returns:
            dict[str, Any]: A dictionary of context data, including the notification to be deleted.
        """
        context = super().get_context_data(**kwargs)
        context["notification"] = self.get_object()
        return context


class OrderNotification:
    """Handles creating notifications related to orders, such as payment acceptance and vendor updates."""

    @staticmethod
    def buyer_notification(order: Order) -> Notification:
        """
        Creates and sends a notification to the buyer when their payment is accepted.

        Args:
            order (Order): The order instance for which the notification is created.

        Returns:
            Notification: The created notification instance sent to the buyer.
        """
        buyer = CustomUser.objects.get(id=order.customer.id)
        title = f"Order {order.id} payment accepted"
        body = f"'Hi your payment was accepted. To see your order click: <a href=\"http://127.0.0.1:8000/order/detail/{order.id}\"><i class='fas fa-envelope me-2 text-secondary'></i>Open notification</a>'"
        notification = Notification(user=buyer, title=title, body=body)
        notification.save()
        return notification

    @staticmethod
    def unpacking_products(products_dict: dict) -> str:
        """
        Converts the product dictionary into a human-readable string format.

        Args:
            products_dict (dict): A dictionary containing product names and their quantities.

        Returns:
            str: A formatted string listing all products and their quantities.
        """
        products = products_dict["products"]
        literal = ""
        for product, quantity in products.items():
            literal += " " + product + " " + quantity + "\r\n"

        return literal

    @staticmethod
    def vendor_notification(order: Order) -> Notification:
        """
        Creates and sends a notification to the vendor when their products are sold.

        Args:
            order (Order): The order instance for which the notification is created.

        Returns:
            Notification: The created notification instance sent to the vendor.
        """
        title = f"The purchase of your products has been paid for in orders {order.id}"

        products_order = ProductOrder.objects.filter(order=order.id)
        dict_prod = {"products": {}}
        for product_order in products_order:
            inventory = Inventory.objects.get(products=product_order.product.id)
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
