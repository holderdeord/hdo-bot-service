from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Import promises from https://data.holderdeord.no/api/promises
    """

    def handle(self, *args, **options):
        pass
