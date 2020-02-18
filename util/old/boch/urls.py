from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_boch, name='get_boch'),
    path('<str:day>', views.get_boch, name='get_boch'),
]
