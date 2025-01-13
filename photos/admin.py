from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.forms.models import BaseInlineFormSet
from django.utils.translation import ngettext

from photologue.admin import (
    GalleryAdmin as GalleryAdminDefault,
    PhotoAdmin as PhotoAdminDefault,
    PhotoSizeAdmin,
)
from photologue.models import (
    Gallery,
    Photo,
    PhotoEffect,
    PhotoSize,
    PhotoSizeCache,
    Watermark,
)

from .models import (
    GalleryCustom,
    GalleryProxy,
    PhotoCustom,
    PhotoProxy,
    PhotoSizeProxy,
)


class GalleryCustomFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.forms[0].fields["allowed_users"].queryset = User.objects.filter(is_superuser=False)
        #
        # Instead of excluding all non-superusers,
        # we could also include all superusers by default.
        #
        #initial = []
        #allowed_users = list(User.objects.filter(is_superuser=True) \
        #                                 .values_list("pk", flat=True))
        #initial.append({"allowed_users": allowed_users})
        #self.initial = initial
        #self.extra += len(initial)

class GalleryCustomInline(admin.StackedInline):
    model = GalleryCustom
    can_delete = False
    filter_horizontal = ("allowed_users",)
    formset = GalleryCustomFormSet

class GalleryAdmin(GalleryAdminDefault):
    inlines = [GalleryCustomInline, ]


class PhotoCustomInline(admin.StackedInline):
    model = PhotoCustom
    can_delete = False

class PhotoAdmin(PhotoAdminDefault):
    inlines = [PhotoCustomInline, ]
    actions = ["create_native"]

    @admin.action(
        description="Copier les photos sélectionnées dans le cache en taille native",
    )
    def create_native(self, request, queryset):
        photosize = PhotoSizeCache().sizes.get("native")
        size_exists_n = 0
        size_created_n = 0
        for photo in queryset:
            if not photo.size_exists(photosize):
                photo.create_size(photosize)
                size_created_n += 1
            else:
                size_exists_n += 1

        if size_created_n > 0:
            msg = ngettext(
                "%d image a été ajoutée au cache avec succès.",
                "%d images ont été ajoutées au cache avec succès.",
                size_created_n,
            ) % size_created_n
            if size_exists_n > 0:
                msg += ngettext(
                    " %d image était déjà présente dans le cache.",
                    " %d images étaient déjà présentes dans le cache.",
                    size_exists_n,
                ) % size_exists_n
        else:
            msg = ngettext(
                "L'image était déjà présente dans le cache.",
                "Les images étaient déjà présentes dans le cache.",
                size_exists_n,
            )
        self.message_user(request, msg, messages.SUCCESS)


# unregister all photologue models
admin.site.unregister(Gallery)
admin.site.unregister(Photo)
admin.site.unregister(PhotoEffect)
admin.site.unregister(PhotoSize)
admin.site.unregister(Watermark)

# re-register the models we care about through our proxies
admin.site.register(GalleryProxy, GalleryAdmin)
admin.site.register(PhotoSizeProxy, PhotoSizeAdmin)
admin.site.register(PhotoProxy, PhotoAdmin)
