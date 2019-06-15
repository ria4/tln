from django import template
import django_comments
from django_comments.templatetags.comments import RenderCommentFormNode

register = template.Library()


class RenderCommentFormNodeWithAuthInfo(RenderCommentFormNode):
    def get_form(self, context):
        obj = self.get_object(context)
        is_superuser = context['request'].user.is_superuser
        if obj:
            return django_comments.get_form()(obj, is_user_superuser=is_superuser)
        else:
            return None

@register.tag
def render_comment_form_with_auth_info(parser, token):
    return RenderCommentFormNodeWithAuthInfo.handle_token(parser, token)
