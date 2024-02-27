from zoneinfo import ZoneInfo

from django.conf import settings


def strftime_local(dt):
    """Print a datetime adjusted to the website timezone."""
    return dt.astimezone(ZoneInfo(settings.TIME_ZONE)).strftime('%Y-%m-%d')
