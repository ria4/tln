
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', include('zinnia.urls')),
    path('comments/', include('django_comments.urls')),
    path('logout', views.logout_view, name='logout'),
]

