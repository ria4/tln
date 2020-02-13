from django.contrib import admin
from django.contrib.auth.models import User
from django.forms.models import BaseInlineFormSet

from zinnia.admin.entry import EntryAdmin as EntryAdminDefault
from zinnia.models.entry import Entry

from .models import EntryCustom


class EntryCustomFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.forms[0].fields["allowed_users"].queryset = User.objects.filter(is_superuser=False)

class EntryCustomInline(admin.StackedInline):
    model = EntryCustom
    can_delete = False
    filter_horizontal = ("allowed_users",)
    formset = EntryCustomFormSet

class EntryAdmin(EntryAdminDefault):
    inlines = [EntryCustomInline, ]

admin.site.unregister(Entry)
admin.site.register(Entry, EntryAdmin)
