# django wants to load all apps at once, therefore preventing easy imports from
# one app (zinnia) to another (the present one).
from django.apps import apps
apps_ready_snap = apps.apps_ready
apps.apps_ready = True


import binascii
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template import loader
from django.utils.translation import activate, get_language, ugettext_lazy as _
from zinnia.moderator import EntryCommentModerator
from zinnia.settings import PROTOCOL
from tln.utils import md5_2

apps.apps_ready = apps_ready_snap

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

    def do_email_reply(self, comment, entry, site):
        """
        Mostly copy-paste, except each hash to the template.
        """
        if not self.email_reply:
            return

        exclude_list = (
            self.mail_comment_notification_recipients
            + [author.email for author in entry.authors.all()]
            + [comment.email]
        )
        recipient_list = (
            set([other_comment.email
                 for other_comment in entry.comments
                 if other_comment.email])
            - set(exclude_list)
        )
        if not recipient_list:
            return

        template = loader.get_template(
            'comments/zinnia/entry/email/reply.txt')

        for recipient in recipient_list:
            h = binascii.hexlify(md5_2(recipient.encode('utf-8')))
            h = h.decode('unicode-escape')
            context = {
                'comment': comment,
                'entry': entry,
                'site': site,
                'protocol': PROTOCOL,
                'email_hash': h
            }
            subject = _('[%(site)s] New comment posted on "%(title)s"') % \
                {'site': site.name, 'title': entry.title}
            message = template.render(context)

            mail = EmailMessage(
                subject, message,
                settings.DEFAULT_FROM_EMAIL,
                to=[recipient])
                #bcc=recipient_list)
            mail.send(fail_silently=not settings.DEBUG)
