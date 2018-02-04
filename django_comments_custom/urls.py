
from django.conf.urls import url
from django_comments.urls import urlpatterns as _urlpatterns
from .views.comments import post_comment


urlpatterns = _urlpatterns[1:] + [url(r'^post/$', post_comment, name='comments-post-comment')]

