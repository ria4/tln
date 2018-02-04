# django wants to load all apps at once, therefore preventing easy imports from
# one app (zinnia) to another (the present one).
from django.apps import apps
apps_ready_snap = apps.apps_ready
apps.apps_ready = True


from django.conf import settings
from django.contrib.sites.models import Site
from django.utils.translation import activate, get_language
from zinnia.moderator import EntryCommentModerator

class EntryCommentModeratorCustom(EntryCommentModerator):

    def moderate(self, comment, content_object, request):
        if request.user.is_authenticated:
            return False
        return super().moderate(comment, content_object, request)

    def email(self, comment, entry, request):
        """
        This is mostly copy-paste, except for the notification test.
        """
        current_language = get_language()
        try:
            activate(settings.LANGUAGE_CODE)
            site = Site.objects.get_current()
            #if self.auto_moderate_comments or comment.is_public:
            if (self.auto_moderate_comments and
                not comment.is_public and
                not request.user.is_authenticated):
                self.do_email_notification(comment, entry, site)
            if comment.is_public:
                self.do_email_authors(comment, entry, site)
                self.do_email_reply(comment, entry, site)
        finally:
            activate(current_language)


apps.apps_ready = apps_ready_snap
