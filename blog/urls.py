
#from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from . import views

urlpatterns = [
    path('', include('zinnia.urls')),
    path('comments/', include('django_comments_custom.urls')),
    #path('admin/', admin.site.urls),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-\w]+)/unsubscribe/(?P<h>[0-9a-f]{32})$',
        views.unsubscribe, name='unsubscribe'),
]

