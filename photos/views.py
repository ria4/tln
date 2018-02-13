from django.shortcuts import get_object_or_404

from photologue.views import GalleryDetailView

from .models import GalleryCustom


class GalleryCustomDetailView(GalleryDetailView):
    context_object_name = "gallery_custom"
    template_name = "photologue/gallery_detail.html"

    def get_object(self, queryset=None):
        gallery_id = super().get_object(queryset=queryset).id
        return get_object_or_404(GalleryCustom, gallery_id=gallery_id)
