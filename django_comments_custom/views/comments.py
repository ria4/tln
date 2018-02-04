from django.http import HttpResponseRedirect, JsonResponse
from django_comments.views.comments import CommentPostBadRequest, post_comment as _post_comment


def post_comment(request, next=None, using=None):
    """
    With the current django_comments, _post_comment can only return
    a CommentPostBadRequest, an HttpResponse (for previews)
    or an HttpResponseRedirect (when comment has been saved).
    """
    res = {}
    res['post_comment_success'] = isinstance(_post_comment(request, next=next, using=using),
                                             HttpResponseRedirect)
    return JsonResponse(res)
