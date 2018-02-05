from django.conf.urls import url
from django.urls import include, path
from zinnia.views.tags import TagDetail
from . import views


blog_urls = ([
    #path('search/', include('zinnia.urls.search')),
    path('feeds/', include('zinnia.urls.feeds')),
    url(r'^tags/(?P<tag>[^/]+(?u))/$', TagDetail.as_view(), name='tag_detail'),
    url(r'^tags/(?P<tag>[^/]+(?u))/page/(?P<page>\d+)/$', TagDetail.as_view(), name='tag_detail_paginated'),
    path('', include('zinnia.urls.entries')),
    path('', include('zinnia.urls.archives')),
    path('', include('zinnia.urls.shortlink')),
    #path('', include('zinnia.urls.quick_entry')),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/unsubscribe/(?P<h>[0-9a-f]{32})$',
        views.unsubscribe, name='unsubscribe'),
], 'zinnia')

urlpatterns = [
    path('', include(blog_urls)),
    path('comments/', include('django_comments_custom.urls')),
]
