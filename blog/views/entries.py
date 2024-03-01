"""Views for Zinnia entries"""
from tzlocal import get_localzone

from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_safe
from django.views.generic.dates import BaseDateDetailView

from blog.models.entry import Entry
from blog.views.mixins.archives import ArchiveMixin
from blog.views.mixins.callable_queryset import CallableQuerysetMixin
from blog.views.mixins.entry_cache import EntryCacheMixin
from blog.views.mixins.entry_preview import EntryPreviewMixin
from blog.views.mixins.entry_protection import EntryProtectionMixin
from blog.views.mixins.templates import EntryArchiveTemplateResponseMixin


@require_safe
def entry_detail_slug(req, slug):
    entry = get_object_or_404(Entry, slug=slug)
    date = entry.publication_date.astimezone(get_localzone())
    year = date.year
    month = "%.2d" % date.month
    day = "%.2d" % date.day
    return redirect('blog:entry_detail', year=year, month=month, day=day, slug=slug)


class EntryDateDetail(ArchiveMixin,
                      EntryArchiveTemplateResponseMixin,
                      CallableQuerysetMixin,
                      BaseDateDetailView):
    """
    Mixin combinating:

    - ArchiveMixin configuration centralizing conf for archive views
    - EntryArchiveTemplateResponseMixin to provide a
      custom templates depending on the date
    - BaseDateDetailView to retrieve the entry with date and slug
    - CallableQueryMixin to defer the execution of the *queryset*
      property when imported
    """
    queryset = Entry.published.on_site


class EntryDetail(EntryCacheMixin,
                  EntryPreviewMixin,
                  EntryProtectionMixin,
                  EntryDateDetail):
    """
    Detailed archive view for an Entry with password
    and login protections and restricted preview.
    """
    template_name = "blog/entry_detail_base.html"
