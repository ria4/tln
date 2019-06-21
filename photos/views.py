from django.contrib.auth import logout
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import get_object_or_404, redirect

from photologue.models import Gallery
from photologue.views import GalleryDetailView, PhotoDetailView

from tln import settings
from tln.utils import remove_query_param, update_query_param

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
                next_url = remove_query_param(req.path, "loginfail")
                login_url = update_query_param(settings.LOGIN_URL, "loginfail", 2)
                return redirect_to_login(next_url, login_url=login_url)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = Gallery.objects.on_site()
        gallery = super().get_object(queryset=queryset)
        gallery_custom = get_object_or_404(GalleryCustom, gallery_id=gallery.id)
        return gallery_custom
