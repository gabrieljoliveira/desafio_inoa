from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.count() == 0:
            email = "user@email.com"
            password = "123"
            user = User.objects.create_superuser(
                email=email, first_name="user", password=password
            )
            user.is_staff = True
            user.save()
        else:
            pass
