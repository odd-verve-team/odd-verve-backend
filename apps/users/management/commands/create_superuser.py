import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates default superuser in database"

    def handle(self, *args, **options):
        email = "test@test.com"
        try:
            get_user_model().objects.get(email=email)
        except get_user_model().DoesNotExist:
            get_user_model().objects.create_superuser(email=email, password="1234")
            logger.info("Superuser created successfully")
        else:
            logger.info("Superuser already exists")
