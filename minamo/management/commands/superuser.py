from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
import os
User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not User.objects.filter(username=os.environ.get('ADMIN_USERNAME')).exists():
            User.objects.create_superuser(
                username=os.environ.get('ADMIN_USERNAME'),
                password=os.environ.get('ADMIN_PASSWORD'),
                email =''
            )