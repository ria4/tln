from django.contrib.auth.decorators import permission_required
from django.views.generic import RedirectView, TemplateView
from django.urls import include, path, re_path, reverse_lazy

from photologue.views import GalleryArchiveIndexView, PhotoDetailView

from .models import GalleryCustom
from .views import GalleryCustomDetailView


photos_urls = ([
    path('<slug:slug>', GalleryCustomDetailView.as_view(), name='pl-gallery'),
    path('photo/<slug:slug>', permission_required('photos.all_rights')(PhotoDetailView.as_view()), name='pl-photo'),
], 'photologue')


extra_context_galleries = {'galleries': GalleryCustom.objects.filter(gallery__is_public=True).order_by('gallery__date_added')}

urlpatterns = [
    path('', TemplateView.as_view(template_name='photologue/galleries.html',
                                  extra_context=extra_context_galleries)),
    path('lightpainting', TemplateView.as_view(template_name='photologue/lightpainting.html')),
    path('about-lightpainting', TemplateView.as_view(template_name='photologue/lightpainting_en.html')),
    path('tirages', permission_required('photos.all_rights')(
        TemplateView.as_view(template_name='photologue/tirages.html'))),
    path('prints', permission_required('photos.all_rights')(
        TemplateView.as_view(template_name='photologue/tirages_en.html'))),
    path('', include(photos_urls)),
]
