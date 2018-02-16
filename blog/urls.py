from django.conf.urls import url
from django.urls import include, path

from zinnia.urls.archives import index_patterns, year_patterns, month_patterns, day_patterns
from zinnia.views.tags import TagDetail
from zinnia.urls import _
from . import views


archive_patterns = index_patterns + year_patterns + month_patterns + day_patterns

tags_urls = [
    url(r'^(?P<tag>[^/]+(?u))/$', TagDetail.as_view(), name='tag_detail'),
    url(r'^(?P<tag>[^/]+(?u))/page/(?P<page>\d+)/$', TagDetail.as_view(), name='tag_detail_paginated'),
]

blog_urls = ([
    path('feeds/', include('zinnia.urls.feeds')),
    path('tags/', include(tags_urls)),
    path('<slug:slug>/', views.entry_detail_slug, name='entry_detail_slug'),
    path('', include('zinnia.urls.entries')),
    path('', include(archive_patterns)),
    path('', include('zinnia.urls.shortlink')),
    path('', include('zinnia.urls.quick_entry')),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/unsubscribe/(?P<h>[0-9a-f]{32})$',
        views.unsubscribe, name='unsubscribe'),
], 'zinnia')


urlpatterns = [
    path('', include(blog_urls)),
    path('comments/', include('django_comments_custom.urls')),
]
