from django.contrib import admin

from photologue.admin import GalleryAdmin as GalleryAdminDefault, PhotoAdmin as PhotoAdminDefault
from photologue.models import Gallery, Photo
from .models import GalleryCustom, PhotoCustom


class GalleryCustomInline(admin.StackedInline):
    model = GalleryCustom
    can_delete = False

class GalleryAdmin(GalleryAdminDefault):
    inlines = [GalleryCustomInline, ]

admin.site.unregister(Gallery)
admin.site.register(Gallery, GalleryAdmin)


class PhotoCustomInline(admin.StackedInline):
    model = PhotoCustom
    can_delete = False

class PhotoAdmin(PhotoAdminDefault):
    inlines = [PhotoCustomInline, ]

admin.site.unregister(Photo)
admin.site.register(Photo, PhotoAdmin)
