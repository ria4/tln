from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', TemplateView.as_view(template_name='critique/preambule.html'), name='preambule'),
    path('preambule/', TemplateView.as_view(template_name='critique/preambule.html'), name='preambule'),
    path('textes/', views.TopTextesView.as_view(), name='top_textes'),
    path('notes/', views.list_notes, name='list_notes'),
    path('notes/<int:page>', views.list_notes, name='list_notes'),
    path('notes/<str:mtype>', views.list_notes, name='list_notes'),
    path('notes/<str:mtype>/<int:page>', views.list_notes, name='list_notes'),
    path('oeuvre/add', views.add_oeuvre, name='add_oeuvre'),
    path('oeuvre/autocomplete-film', views.FilmAutocomplete.as_view(), name='autocomplete_film'),
    path('oeuvre/<slug:slug>', views.detail_oeuvre, name='detail_oeuvre'),
    path('oeuvre/<slug:slug>/delete', views.delete_oeuvre, name='delete_oeuvre'),
    path('oeuvre/<slug:slug>/add_comment', views.add_comment, name='add_comment'),
    path('oeuvre/<slug:slug>/update_latest_comment', views.update_latest_comment, name='update_latest_comment'),
    path('oeuvre/<slug:slug>/delete_latest_comment', views.delete_latest_comment, name='delete_latest_comment'),
    path('artiste/<slug:slug>', views.detail_artiste, name='detail_artiste'),
    path('perspectives/', views.list_envies, name='list_envies'),
    path('perspectives/<str:mtype>', views.list_envies, name='list_envies'),
    path('perspectives/<str:mtype>/<int:page>', views.list_envies, name='list_envies'),
    path('tags/', views.list_tags, name='list_tags'),
    path('tags/<slug:slug>', views.detail_tag, name='detail_tag'),
    path('tags/<slug:slug>/<int:page>', views.detail_tag, name='detail_tag'),
    path('top_films/', views.top_films, name='top_films'),
    path('top_films/<int:year>', views.top_films, name='top_films'),
    path('top_jeux/', views.top_jeux, name='top_jeux'),
    path('rencontres/', views.list_oeuvres, name='list_oeuvres'),
    path('rencontres/<str:mtype>', views.list_oeuvres, name='list_oeuvres'),
    path('cinema/add', views.add_cinema, name='add_cinema'),
    path('cinema/autocomplete', views.CinemaAutocomplete.as_view(), name='autocomplete_cinema'),
    path('cinema/<slug:slug>', views.detail_cinema, name='detail_cinema'),
    path('cinema/<slug:slug>/delete', views.delete_cinema, name='delete_cinema'),
    path('cinemas/', views.list_cinemas, name='list_cinemas'),
    path('seances/', views.list_seances, name='list_seances'),
    path('seances/add', views.add_seance, name='add_seance'),
    path('seances/<int:year>', views.list_seances, name='list_seances'),
    path('search/', views.search_oeuvres, name='search_oeuvres'),
    path('search/<str:match>', views.search_oeuvres, name='search_oeuvres'),
]

