from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from zinnia.admin.entry import EntryAdmin
from zinnia.models.entry import Entry
from .models import EntryLang


class EntryLangAdmin(EntryAdmin):
    fieldsets = (
        (_('Content'), {
            'fields': (('title', 'status'), 'lang', 'lead', 'content',)}),) + \
                    EntryAdmin.fieldsets[1:]

admin.site.register(Entry, EntryLangAdmin)
