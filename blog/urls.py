
from django.conf.urls import url
from django.urls import include, path
from . import views


blog_urls = ([
    #path('search/', include('zinnia.urls.search')),
    path('tags/', include('zinnia.urls.tags')),
    path('feeds/', include('zinnia.urls.feeds')),
    path('', include('zinnia.urls.entries')),
    path('', include('zinnia.urls.archives')),
    path('', include('zinnia.urls.shortlink')),
    path('', include('zinnia.urls.quick_entry')),
    path('', include('zinnia.urls.capabilities')),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/unsubscribe/(?P<h>[0-9a-f]{32})$',
        views.unsubscribe, name='unsubscribe'),
], 'zinnia')

urlpatterns = [
    path('', include(blog_urls)),
    path('comments/', include('django_comments_custom.urls')),
]

