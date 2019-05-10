
from django import forms
from django.utils.encoding import force_text
from django.utils.translation import pgettext_lazy, ugettext_lazy as _
from django.utils import timezone

# django wants to load all apps at once, therefore preventing easy imports from
# one app (contrib.contenttypes, django_comments) to another (the present one).
from django.apps import apps
if apps.apps_ready:
    from django_comments.forms import CommentForm
else:
    apps.apps_ready = True
    from django_comments.forms import CommentForm
    apps.apps_ready = False

COMMENT_MAX_LENGTH = 6000


class CommentFormCustom(CommentForm):
    name = forms.CharField(label=pgettext_lazy("Person name", "Name"), max_length=50,
                           widget=forms.TextInput(attrs={"placeholder": "~nom~"}))
    email = forms.EmailField(label=_("Email address"), required=False,
                             widget=forms.EmailInput(attrs={"placeholder": "~email~ (si vous souhaitez être prévenu·e de futures réponses)"}))
    comment = forms.CharField(label=_('Comment'), max_length=COMMENT_MAX_LENGTH,
                              widget=forms.Textarea(attrs={"placeholder": "~commentaire~"}))

    def __init__(self, target_object, data=None, initial=None, is_user_authenticated=False, **kwargs):
        super().__init__(target_object, data=data, initial=initial, **kwargs)
        if is_user_authenticated:
            self.fields['name'].initial = 'ria'

    def get_comment_create_data(self, site_id=None):
        from django.contrib.contenttypes.models import ContentType
        return dict(
            content_type=ContentType.objects.get_for_model(self.target_object),
            object_pk=force_text(self.target_object._get_pk_val()),
            user_name=self.cleaned_data["name"],
            user_email=self.cleaned_data["email"],
            comment=self.cleaned_data["comment"],
            submit_date=timezone.now(),
            site_id=site_id or getattr(settings, "SITE_ID", None),
            is_public=True,
            is_removed=False,
        )

CommentFormCustom.base_fields.pop('url')
