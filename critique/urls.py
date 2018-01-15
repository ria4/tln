from django.urls import path
from . import views

urlpatterns = [
    path('', views.preambule, name='preambule'),
    path('oeuvre/<slug:slug>', views.detail_oeuvre_slug, name='detail_oeuvre_slug'),
    path('oeuvre/id/<str:id>', views.detail_oeuvre, name='detail_oeuvre'),
    path('artiste/<str:artist>', views.artiste, name='artiste'),
    path('envies/<str:mtype>', views.liste_envies, name='liste_envies'),
    path('envies/<str:mtype>/<int:page>', views.liste_envies, name='liste_envies'),
    path('collection/<str:mtype>', views.liste_oeuvres, name='liste_oeuvres'),
    path('collection/<str:mtype>/<int:page>', views.liste_oeuvres, name='liste_oeuvres'),
    path('notes/', views.liste_notes, name='liste_notes'),
    path('notes/<int:page>', views.liste_notes, name='liste_notes'),
    path('notes/<str:mtype>', views.liste_notes, name='liste_notes'),
    path('notes/<str:mtype>/<int:page>', views.liste_notes, name='liste_notes'),
    path('top_films/', views.top_films, name='top_films'),
    path('top_films/<int:year>', views.top_films, name='top_films'),
    path('textes/', views.top_textes, name='top_textes'),
    path('cinema/id/<str:id>', views.detail_cinema, name='detail_cinema'),
    path('cinemas/', views.liste_cinemas, name='liste_cinemas'),
    path('seances/', views.liste_seances, name='liste_seances'),
    path('seances/<int:year>', views.liste_seances, name='liste_seances'),
]

