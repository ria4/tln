from http import HTTPStatus
import logging

from django.core.exceptions import PermissionDenied

logger = logging.getLogger('django')


class FilterIpMiddleware:
    """Log & filter out IP addresses."""

    OFFENDING_IPS = []

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if not x_forwarded_for:
            return self.get_response(request)

        ip = x_forwarded_for.split(',')[0]
        if ip in self.OFFENDING_IPS:
            logger.warning(f"[{ip}] 403 {request.method} {request.path}")
            raise PermissionDenied

        response = self.get_response(request)
        if response.status_code == HTTPStatus.NOT_FOUND:
            logger.warning(f"[{ip}] 404 {request.method} {request.path}")
        else:
            logger.info(f"[{ip}] {response.status_code} {request.method} {request.path}")

        return response
