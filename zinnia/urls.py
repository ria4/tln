"""Defaults urls for the Zinnia project"""
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy
from django.views import defaults

from zinnia.views.archives import EntryIndex, EntryYear, EntryMonth, EntryDay
from zinnia.views.entries import EntryDetail, entry_detail_slug
from zinnia.views.feeds import LastEntries
from zinnia.views.shortlink import EntryShortLink
from zinnia.views.tags import TagDetail


app_name = 'zinnia'

index_patterns = [
    re_path(r'^$',
        EntryIndex.as_view(),
        name='entry_archive_index'),
    re_path(r'^page/(?P<page>\d+)/$',
        EntryIndex.as_view(),
        name='entry_archive_index_paginated')
]

year_patterns = [
    re_path(r'^(?P<year>\d{4})/$',
        EntryYear.as_view(),
        name='entry_archive_year'),
    re_path(r'^(?P<year>\d{4})/page/(?P<page>\d+)/$',
        EntryYear.as_view(),
        name='entry_archive_year_paginated'),
]

month_patterns = [
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        EntryMonth.as_view(),
        name='entry_archive_month'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/page/(?P<page>\d+)/$',
        EntryMonth.as_view(),
        name='entry_archive_month_paginated'),
]

day_patterns = [
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        EntryDay.as_view(),
        name='entry_archive_day'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/'
          r'(?P<day>\d{2})/page/(?P<page>\d+)/$',
        EntryDay.as_view(),
        name='entry_archive_day_paginated'),
]

archive_patterns = index_patterns + year_patterns + month_patterns + day_patterns


urlpatterns = [
    # catch reverse attempt to 'comments-url-redirect' view
    # which was retired along with django_comments
    path('feeds/discussions/', defaults.bad_request),

    path('feeds/', LastEntries(), name='entry_feed'),
    path('tags/<str:tag>/', TagDetail.as_view(), name='tag_detail'),
    path('', include(archive_patterns)),
    re_path(
        r'^(?P<token>[\dA-Z]+)/$',
        EntryShortLink.as_view(),
        name='entry_shortlink',
    ),
    path('<slug:slug>/', entry_detail_slug, name='entry_detail_slug'),
    re_path(
        r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        EntryDetail.as_view(),
        name='entry_detail',
    ),
]
