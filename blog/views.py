import binascii
import hashlib
import pytz

from tzlocal import get_localzone

from django.apps import apps
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from zinnia.models.entry import Entry

from tln.utils import md5_2


def entry_detail_slug(req, slug):
    entry = Entry.objects.filter(slug=slug)[0]
    date = entry.publication_date.astimezone(get_localzone())
    year = date.year
    month = "%.2d" % date.month
    day = "%.2d" % date.day
    return redirect('zinnia:entry_detail', year=year, month=month, day=day, slug=slug, permanent=True)

def unsubscribe(req, year, month, day, slug, h):
    """
    How to unsubscribe an unauthenticated user from a thread (...)
    """
    entry_model = apps.app_configs['zinnia'].get_model('Entry')
    entry = get_object_or_404(entry_model,
                              publication_date__year=int(year),
                              publication_date__month=int(month),
                              publication_date__day=int(day),
                              slug=slug)
    emails = set([comment.email for comment in entry.comments])
    hashes = {}
    for email in emails:
        hashes[bytes(binascii.hexlify(md5_2(email.encode('utf-8'))))] = email

    h = h.encode('utf-8')
    if h not in hashes:
        raise Http404("This is not a valid link for unsubscribing.")

    email_to_remove = hashes[h]
    superusers_emails = User.objects.filter(is_superuser=True).values_list('email')
    superusers_emails = [l[0] for l in list(superusers_emails)]
    if email_to_remove not in superusers_emails: 
        for comment in entry.comments:
            if comment.email == email_to_remove:
                comment.email = ''
                comment.save()

    return render(req, 'comments/unsubscribed.html', locals())


"""
The part below enables showing non-published entries to the admin.
"""

from tagging.models import TaggedItem
from tagging.utils import get_tag
from zinnia.views.archives import EntryArchiveMixin
from zinnia.views.tags import BaseTagDetail


def get_queryset_base_tag_detail_su_sensitive(self):
    self.tag = get_tag(self.kwargs['tag'])
    if self.tag is None:
        raise Http404
    if self.request.user.is_superuser:
        queryset = Entry.objects.all()
    else:
        queryset = Entry.published.all()
    return TaggedItem.objects.get_by_model(queryset, self.tag)

BaseTagDetail.get_queryset = get_queryset_base_tag_detail_su_sensitive


class SUSensitiveMixin(object):
    def get_queryset(self):
        if self.request.user.is_superuser:
            self.queryset = Entry.objects.all
        else:
            self.queryset = Entry.published.all
        return super().get_queryset()

EntryArchiveMixin.__bases__ = (SUSensitiveMixin,) + EntryArchiveMixin.__bases__
