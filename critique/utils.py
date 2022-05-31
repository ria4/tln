import pytz

from django.conf import settings


def strftime_local(dt):
    """Print a datetime adjusted to the website timezone."""
    return dt.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime('%Y-%m-%d')
