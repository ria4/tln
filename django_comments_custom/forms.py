
"""
/!\ This may break when upgrading django! /!\

This whole mess of copy-paste cannot be avoided (?) because django wants to
load all apps at once, therefore preventing easy imports from one app
(contrib.contenttypes, django_comments) to another (django_comments_custom).

But I'd rather copy-paste code than modify django app registry mechanisms...
"""

from django import forms
from django.utils.translation import pgettext_lazy, ugettext_lazy as _
from ._forms import CommentForm, COMMENT_MAX_LENGTH

class CommentFormCustom(CommentForm):
    name = forms.CharField(label=pgettext_lazy("Person name", "Name"), max_length=50, widget=forms.TextInput(attrs={"placeholder": "~nom~"}))
    comment = forms.CharField(label=_('Comment'),
                              widget=forms.Textarea(attrs={"placeholder": "~commentaire~"}),
                              max_length=COMMENT_MAX_LENGTH)

    def get_comment_create_data(self, site_id=None):
        from django.contrib.contenttypes.models import ContentType
        return dict(
            content_type=ContentType.objects.get_for_model(self.target_object),
            object_pk=force_text(self.target_object._get_pk_val()),
            user_name=self.cleaned_data["name"],
            comment=self.cleaned_data["comment"],
            submit_date=timezone.now(),
            site_id=site_id or getattr(settings, "SITE_ID", None),
            is_public=True,
            is_removed=False,
        )

CommentFormCustom.base_fields.pop('url')
CommentFormCustom.base_fields.pop('email')
