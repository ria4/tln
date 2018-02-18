from django.conf.urls import url
from django.views.generic import RedirectView
from django.urls import include, path, reverse_lazy

from photologue.views import GalleryArchiveIndexView, PhotoDetailView

from .views import GalleryCustomDetailView


photos_urls = ([
    url(r'^$', RedirectView.as_view(url=reverse_lazy('photologue:pl-gallery',
                                                     kwargs={'slug':'silhouettes'})),
        name='pl-photologue-root'),
    #url(r'^all$', GalleryListView.as_view(), name='gallery-list'),
    url(r'^(?P<slug>[\-\d\w]+)$', GalleryCustomDetailView.as_view(), name='pl-gallery'),
], 'photologue')


urlpatterns = [
    path('', include(photos_urls)),
]
