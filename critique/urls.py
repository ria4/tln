from django.urls import path
from django.views.generic import TemplateView

import critique.views.artiste as views_artiste
import critique.views.cinema as views_cinema
import critique.views.collection as views_collection
import critique.views.commentaire as views_commentaire
import critique.views.oeuvre as views_oeuvre
import critique.views.oeuvrespan as views_oeuvrespan
import critique.views.seance as views_seance
import critique.views.top as views_top


urlpatterns = [
    path('', TemplateView.as_view(template_name='critique/preambule.html')),
    path('preambule/', TemplateView.as_view(template_name='critique/preambule.html'), name='preambule'),
    path('textes/', views_top.TopTextesView.as_view(), name='top_textes'),
    path('notes/', views_commentaire.list_notes, name='list_notes'),
    path('notes/<int:page>', views_commentaire.list_notes, name='list_notes'),
    path('notes/<str:mtype>', views_commentaire.list_notes, name='list_notes'),
    path('notes/<str:mtype>/<int:page>', views_commentaire.list_notes, name='list_notes'),
    path('oeuvre/add', views_oeuvre.add_oeuvre, name='add_oeuvre'),
    path('oeuvre/autocomplete-oeuvre', views_oeuvre.OeuvreAutocomplete.as_view(), name='autocomplete_oeuvre'),
    path('oeuvre/autocomplete-film', views_oeuvre.FilmAutocomplete.as_view(), name='autocomplete_film'),
    path('oeuvre/<slug:slug>', views_oeuvre.detail_oeuvre, name='detail_oeuvre'),
    path('oeuvre/<slug:slug>/delete', views_oeuvre.delete_oeuvre, name='delete_oeuvre'),
    path('oeuvre/<slug:slug>/update_latest_oeuvrespan', views_oeuvrespan.update_latest_oeuvrespan, name='update_latest_oeuvrespan'),
    path('oeuvre/<slug:slug>/delete_latest_oeuvrespan', views_oeuvrespan.delete_latest_oeuvrespan, name='delete_latest_oeuvrespan'),
    path('oeuvre/<slug:slug>/add_comment', views_commentaire.add_comment, name='add_comment'),
    path('oeuvre/<slug:slug>/update_latest_comment', views_commentaire.update_latest_comment, name='update_latest_comment'),
    path('oeuvre/<slug:slug>/delete_latest_comment', views_commentaire.delete_latest_comment, name='delete_latest_comment'),
    path('oeuvrespan/add', views_oeuvrespan.add_oeuvrespan, name='add_oeuvrespan'),
    path('artiste/<slug:slug>', views_artiste.detail_artiste, name='detail_artiste'),
    path('perspectives/', views_collection.list_envies, name='list_envies'),
    path('perspectives/<str:mtype>', views_collection.list_envies, name='list_envies'),
    path('perspectives/<str:mtype>/<int:page>', views_collection.list_envies, name='list_envies'),
    path('tags/', views_collection.list_tags, name='list_tags'),
    path('tags/<slug:slug>', views_collection.detail_tag, name='detail_tag'),
    path('tags/<slug:slug>/<int:page>', views_collection.detail_tag, name='detail_tag'),
    path('top_films/', views_top.top_films, name='top_films'),
    path('top_films/<int:year>', views_top.top_films, name='top_films'),
    path('top_jeux/', views_top.top_jeux, name='top_jeux'),
    path('rencontres/', views_collection.list_oeuvres, name='list_oeuvres'),
    path('rencontres/<str:mtype>', views_collection.list_oeuvres, name='list_oeuvres'),
    path('cinema/add', views_cinema.add_cinema, name='add_cinema'),
    path('cinema/autocomplete', views_cinema.CinemaAutocomplete.as_view(), name='autocomplete_cinema'),
    path('cinema/<slug:slug>', views_cinema.detail_cinema, name='detail_cinema'),
    path('cinema/<slug:slug>/delete', views_cinema.delete_cinema, name='delete_cinema'),
    path('cinemas/', views_cinema.list_cinemas, name='list_cinemas'),
    path('seances/', views_seance.list_seances, name='list_seances'),
    path('seances/add', views_seance.add_seance, name='add_seance'),
    path('seances/<int:year>', views_seance.list_seances, name='list_seances'),
    path('search/', views_oeuvre.search_oeuvres, name='search_oeuvres'),
    path('search/<str:match>', views_oeuvre.search_oeuvres, name='search_oeuvres'),
]

