
import binascii
import hashlib
from django.apps import apps
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from tln.utils import md5_2


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
