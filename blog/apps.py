from django.apps import apps, AppConfig
import django_comments
from django_comments import signals
from .moderator import EntryCommentModeratorCustom


class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        from django_comments.moderation import moderator
        moderator.unregister(apps.app_configs['zinnia'].get_model('Entry'))
        moderator.register(apps.app_configs['zinnia'].get_model('Entry'),
                           EntryCommentModeratorCustom)
        signals.comment_was_flagged.connect(moderator.post_save_moderation, sender=django_comments.get_model())
