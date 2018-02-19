from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('critique/', include('critique.urls')),
    path('blog/', include('blog.urls')),
    path('photos/', include('photos.urls')),
]

#TODO remove for production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#handler404 = 'tln.views.error_404'
#handler500 = 'mysite.views.my_custom_error_view'
#handler403 = 'mysite.views.my_custom_permission_denied_view'
#handler400 = 'mysite.views.my_custom_bad_request_view'
