from django.conf.urls import url
from django.urls import include, path

from zinnia.views.archives import EntryIndex
from zinnia.views.archives import EntryMonth
from zinnia.views.archives import EntryYear
from zinnia.views.tags import TagDetail
from zinnia.urls import _
from . import views


index_patterns = [
    url(r'^$',
        EntryIndex.as_view(),
        name='entry_archive_index'),
    url(_(r'^page/(?P<page>\d+)/$'),
        EntryIndex.as_view(),
        name='entry_archive_index_paginated')
]

year_patterns = [
    url(r'^(?P<year>\d{4})/$',
        EntryYear.as_view(),
        name='entry_archive_year'),
    url(_(r'^(?P<year>\d{4})/page/(?P<page>\d+)/$'),
        EntryYear.as_view(),
        name='entry_archive_year_paginated'),
]

month_patterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        EntryMonth.as_view(),
        name='entry_archive_month'),
    url(_(r'^(?P<year>\d{4})/(?P<month>\d{2})/page/(?P<page>\d+)/$'),
        EntryMonth.as_view(),
        name='entry_archive_month_paginated'),
]

archives_urls = index_patterns + year_patterns + month_patterns

tags_urls = [
    url(r'^(?P<tag>[^/]+(?u))/$', TagDetail.as_view(), name='tag_detail'),
    url(r'^(?P<tag>[^/]+(?u))/page/(?P<page>\d+)/$', TagDetail.as_view(), name='tag_detail_paginated'),
]

blog_urls = ([
    #path('search/', include('zinnia.urls.search')),
    path('feeds/', include('zinnia.urls.feeds')),
    path('tags/', include(tags_urls)),
    path('', include('zinnia.urls.entries')),
    path('', include(archives_urls)),
    path('', include('zinnia.urls.shortlink')),
    path('', include('zinnia.urls.quick_entry')),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/unsubscribe/(?P<h>[0-9a-f]{32})$',
        views.unsubscribe, name='unsubscribe'),
], 'zinnia')


urlpatterns = [
    path('', include(blog_urls)),
    path('comments/', include('django_comments_custom.urls')),
]
