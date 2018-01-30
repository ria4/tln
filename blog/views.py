
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render


def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))


# Lines below remove useless fields from comments form.
# /!\ This may break when upgrading django! /!\

from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils import timezone
from django.utils.encoding import force_text
import datetime
def override_get_comment_create_data(self, site_id=None):
    # Use the data of the superclass, and remove extra fields
    return dict(
        content_type = ContentType.objects.get_for_model(self.target_object),
        object_pk    = force_text(self.target_object._get_pk_val()),
        user_name    = self.cleaned_data["name"],
        comment      = self.cleaned_data["comment"],
        submit_date  = timezone.now(),
        site_id      = site_id or getattr(settings, "SITE_ID", None),
        is_public    = True,
        is_removed   = False,
    )

from django_comments.forms import CommentForm
CommentForm.get_comment_create_data = override_get_comment_create_data
CommentForm.base_fields.pop('url')
CommentForm.base_fields.pop('email')

