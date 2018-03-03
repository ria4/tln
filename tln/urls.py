from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', include('home.urls')),
    path('blog/', include('blog.urls')),
    path('photos/', include('photos.urls')),
    path('critique/', include('critique.urls')),

    path('admin/', admin.site.urls),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
]

#TODO remove for production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
