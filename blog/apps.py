"""Apps for Zinnia"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    """
    Config for Zinnia application.
    """
    name = 'blog'
    label = 'blog'
    verbose_name = _('Blog')
