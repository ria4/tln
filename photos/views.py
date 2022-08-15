from django.contrib.auth import logout
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect

from photologue.models import Gallery
from photologue.views import GalleryDetailView

from tln import settings
from tln.constants import MISSING_PERM_TO_PHOTO_GALLERY
from tln.utils import qs_update_loginfail

from .models import GalleryCustom


class GalleryCustomDetailView(GalleryDetailView):
    context_object_name = "gallery_custom"
    template_name = "photologue/gallery_detail.html"

    def get(self, req, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        gallery_custom = self.object

        if ((not gallery_custom.gallery.is_public) and
            (not req.user.is_superuser)):
            if not req.user.is_authenticated:
                return redirect_to_login(req.path)
            elif req.user not in gallery_custom.allowed_users.all():
                logout(req)
                login_url = (
                    settings.LOGIN_URL
                    + "?"
                    + qs_update_loginfail(req, MISSING_PERM_TO_PHOTO_GALLERY)
                )
                return redirect_to_login(req.path, login_url=login_url)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = Gallery.objects.on_site()
        gallery = super().get_object(queryset=queryset)
        gallery_custom = get_object_or_404(GalleryCustom, gallery_id=gallery.id)
        return gallery_custom
