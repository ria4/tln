from django_comments.urls import urlpatterns as _urlpatterns
from django.urls import path
from .views.comments import post_comment


urlpatterns = _urlpatterns[1:] + [
    path('post/', post_comment, name='comments-post-comment')
]
