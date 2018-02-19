from django.contrib import admin

from photologue.admin import GalleryAdmin as GalleryAdminDefault
from photologue.models import Gallery
from .models import GalleryCustom


class GalleryCustomInline(admin.StackedInline):
    model = GalleryCustom
    can_delete = False

class GalleryAdmin(GalleryAdminDefault):
    inlines = [GalleryCustomInline, ]

admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)
