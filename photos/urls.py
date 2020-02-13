from django.conf.urls import url
from django.contrib.auth.decorators import permission_required
from django.views.generic import RedirectView, TemplateView
from django.urls import include, path, reverse_lazy

from photologue.views import GalleryArchiveIndexView, PhotoDetailView

from .models import GalleryCustom
from .views import GalleryCustomDetailView


photos_urls = ([
    url(r'^(?P<slug>[\-\d\w]+)$', GalleryCustomDetailView.as_view(), name='pl-gallery'),
    url(r'^photo/(?P<slug>[\-\d\w]+)/$', permission_required('photos.all_rights')(PhotoDetailView.as_view()), name='pl-photo'),
], 'photologue')


extra_context_galleries = {'galleries': GalleryCustom.objects.filter(gallery__is_public=True)}

urlpatterns = [
    path('', TemplateView.as_view(template_name='photologue/galleries.html',
                                  extra_context=extra_context_galleries)),
    path('lightpainting', TemplateView.as_view(template_name='photologue/lightpainting.html')),
    path('tirages', TemplateView.as_view(template_name='photologue/tirages.html')),
    path('prints', TemplateView.as_view(template_name='photologue/tirages.html')),
    path('', include(photos_urls)),
]
