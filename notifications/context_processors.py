from .models import Notification


def messages_number(request):
    user = request.user

    if user.is_authenticated:
        number_of_messages = Notification.objects.filter(user=request.user, is_read=False)
        context = {'number_of_messages': len(number_of_messages)}
    else:
        context = {}
    return context
