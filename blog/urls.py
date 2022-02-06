from django.urls import include, path, re_path
from django.views import defaults

from zinnia.urls.archives import index_patterns, year_patterns, month_patterns, day_patterns
from zinnia.views.tags import TagDetail
from zinnia.urls import _

from .views import EntryDetailCustom, entry_detail_slug


archive_patterns = index_patterns + year_patterns + month_patterns + day_patterns

# blog/<archive_year> --> blog/<shortlink> --> blog/<slug>
blog_urls = ([
    # catch reverse attempt to 'comments-url-redirect' view
    # which was retired along with django_comments
    path('feeds/discussions/', defaults.bad_request),

    path('feeds/', include('zinnia.urls.feeds')),
    path('tags/<str:tag>/', TagDetail.as_view(), name='tag_detail'),
    path('', include(archive_patterns)),
    path('', include('zinnia.urls.shortlink')),
    path('<slug:slug>/', entry_detail_slug, name='entry_detail_slug'),
    re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        EntryDetailCustom.as_view(), name='entry_detail'),
    path('', include('zinnia.urls.entries')),
    path('', include('zinnia.urls.quick_entry')),
], 'zinnia')


urlpatterns = [
    path('', include(blog_urls)),
]
