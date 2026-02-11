from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import os
User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        admin_username = os.environ.get('ADMIN_USERNAME')
        admin_password = os.environ.get('ADMIN_PASSWORD')
        admin_email = os.environ.get('ADMIN_EMAIL', '')

        if not admin_username or not admin_password:
            self.stdout.write('ADMIN_USERNAME or ADMIN_PASSWORD is not set. Skipping superuser creation.')
            return

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(
                username=admin_username,
                password=admin_password,
                email=admin_email,
            )