from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Clear the entire cache."""

    def handle(self, *args, **options):
        cache.clear()
