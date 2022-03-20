import binascii
import hashlib
import pytz

from tzlocal import get_localzone

from django.apps import apps
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from zinnia.models.entry import Entry
from zinnia.views.entries import EntryDetail

from tln import settings
from tln.utils import remove_query_param, update_query_param, md5_2

from .models import EntryCustom


def entry_detail_slug(req, slug):
    entry = get_object_or_404(Entry, slug=slug)
    date = entry.publication_date.astimezone(get_localzone())
    year = date.year
    month = "%.2d" % date.month
    day = "%.2d" % date.day
    return redirect('zinnia:entry_detail', year=year, month=month, day=day, slug=slug)



class EntryDetailCustom(EntryDetail):
    context_object_name = "entry"
    template_name = "zinnia/entry_detail_base.html"

    def get(self, req, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        entry_custom = self.object.custom

        if (entry_custom.entry.login_required and
            (not req.user.is_superuser)):
            if not req.user.is_authenticated:
                return redirect_to_login(req.path)
            elif req.user not in entry_custom.allowed_users.all():
                logout(req)
                next_url = remove_query_param(req.path, "loginfail")
                login_url = update_query_param(settings.LOGIN_URL, "loginfail", 2)
                return redirect_to_login(next_url, login_url=login_url)
        return self.render_to_response(context)


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
        queryset = Entry.published.filter(login_required=False)
    return TaggedItem.objects.get_by_model(queryset, self.tag)

BaseTagDetail.get_queryset = get_queryset_base_tag_detail_su_sensitive


class SUSensitiveMixin(object):
    def get_queryset(self):
        queryset = Entry.published.filter(login_required=False)
        if self.request.user.is_superuser:
            queryset = Entry.objects
        elif self.request.user.is_authenticated:
            user_id = User.objects.get(username=self.request.user.username).id
            queryset |= Entry.objects.filter(custom__allowed_users__exact=user_id)
        self.queryset = queryset.all
        return super().get_queryset()

EntryArchiveMixin.__bases__ = (SUSensitiveMixin,) + EntryArchiveMixin.__bases__
