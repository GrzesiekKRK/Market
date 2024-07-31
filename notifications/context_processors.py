from .models import Notification


def messages_number(request):
    user = request.user

    if user.is_authenticated:
        number_of_messages = Notification.objects.filter(user=request.user)
        context = {'number_of_messages': number_of_messages}
    else:
        context = {}
    return context
