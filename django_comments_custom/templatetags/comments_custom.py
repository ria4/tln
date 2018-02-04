from django import template
import django_comments
from django_comments.templatetags.comments import RenderCommentFormNode

register = template.Library()


class RenderCommentFormNodeWithAuthInfo(RenderCommentFormNode):
    def get_form(self, context):
        obj = self.get_object(context)
        is_authenticated = context['request'].user.is_authenticated
        if obj:
            return django_comments.get_form()(obj, is_user_authenticated=is_authenticated)
        else:
            return None

@register.tag
def render_comment_form_with_auth_info(parser, token):
    return RenderCommentFormNodeWithAuthInfo.handle_token(parser, token)
