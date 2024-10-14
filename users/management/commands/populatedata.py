from django.core.management.base import BaseCommand, CommandError
from ...factories import CustomUserFactory
from ...models import CustomUser
from notifications.factories import NotificationFactory

class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        user = CustomUserFactory.create(username='staszek')

        user = CustomUser.objects.get(id=user.id)

        NotificationFactory.create_batch(5, user=user)

