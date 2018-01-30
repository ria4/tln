
#from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('zinnia.urls')),
    path('comments/', include('django_comments.urls')),
    #path('admin/', admin.site.urls),
]

