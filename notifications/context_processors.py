from typing import Any

from .models import Notification


def messages_number(request) -> dict[str: Any]:
    """Display number of unread Notification"""
    user = request.user

    if user.is_authenticated:
        number_of_messages_wish = Notification.objects.filter(user=request.user, is_read=False)

        context = {'number_of_messages': len(number_of_messages_wish)}
    else:
        context = {}
    return context
