from django.urls import path, re_path
from django.views.generic import TemplateView

import critique.views.artiste as views_artiste
import critique.views.chronologie as views_chronologie
import critique.views.cinema as views_cinema
import critique.views.collection as views_collection
import critique.views.commentaire as views_commentaire
import critique.views.oeuvre as views_oeuvre
import critique.views.oeuvrespan as views_oeuvrespan
import critique.views.seance as views_seance
import critique.views.top as views_top


urlpatterns = [
    # index
    path('', TemplateView.as_view(template_name='critique/index.html'), name='critique_index'),

    # artistes
    path('artiste/autocomplete', views_artiste.ArtisteAutocomplete.as_view(create_field='name', validate_create=True), name='autocomplete_artiste'),
    path('artiste/<slug:slug>', views_artiste.detail_artiste, name='detail_artiste'),

    # oeuvres
    path('oeuvre/add', views_oeuvre.add_oeuvre, name='add_oeuvre'),
    path('oeuvre/autocomplete', views_oeuvre.OeuvreAutocomplete.as_view(), name='autocomplete_oeuvre'),
    path('oeuvre/autocomplete-film', views_oeuvre.FilmAutocomplete.as_view(), name='autocomplete_film'),
    path('oeuvre/<slug:slug>', views_oeuvre.detail_oeuvre, name='detail_oeuvre'),
    path('oeuvre/<slug:slug>/delete', views_oeuvre.delete_oeuvre, name='delete_oeuvre'),
    path('oeuvre/<slug:slug>/update_latest_oeuvrespan', views_oeuvrespan.update_latest_oeuvrespan, name='update_latest_oeuvrespan'),
    path('oeuvre/<slug:slug>/delete_latest_oeuvrespan', views_oeuvrespan.delete_latest_oeuvrespan, name='delete_latest_oeuvrespan'),
    path('oeuvre/<slug:slug>/add_comment', views_commentaire.add_comment, name='add_comment'),
    path('oeuvre/<slug:slug>/update_latest_comment', views_commentaire.update_latest_comment, name='update_latest_comment'),
    path('oeuvre/<slug:slug>/delete_latest_comment', views_commentaire.delete_latest_comment, name='delete_latest_comment'),
    path('oeuvrespan/add', views_oeuvrespan.add_oeuvrespan, name='add_oeuvrespan'),
    path('search/', views_oeuvre.search_oeuvres, name='search_oeuvres'),
    path('search/<str:match>', views_oeuvre.search_oeuvres, name='search_oeuvres'),

    # commentaires
    path('textes/', views_top.TopTextesView.as_view(), name='top_textes'),
    path('thinky-games/', views_top.TgdbExcerptsView.as_view(), name='list_tgdb_excerpts'),
    path('notes/', views_commentaire.list_notes, name='list_notes'),
    path('notes/<int:page>', views_commentaire.list_notes, name='list_notes'),
    path('notes/<str:mtype>', views_commentaire.list_notes, name='list_notes'),
    path('notes/<str:mtype>/<int:page>', views_commentaire.list_notes, name='list_notes'),

    # collections
    path('rencontres/', views_collection.list_oeuvres, name='list_oeuvres'),
    path('rencontres/<str:mtype>', views_collection.list_oeuvres, name='list_oeuvres'),
    path('perspectives/', views_collection.list_envies, name='list_envies'),
    path('perspectives/<str:mtype>', views_collection.list_envies, name='list_envies'),
    path('perspectives/<str:mtype>/<int:page>', views_collection.list_envies, name='list_envies'),

    # tops
    path('top_films/', views_top.TopFilmsView.as_view(), name='top_films'),
    path('top_films/<int:year>', views_top.TopFilmsView.as_view(), name='top_films'),
    path('top_jeux/', views_top.TopJeuxView.as_view(), name='top_jeux'),

    # tags
    path('tags/', views_collection.list_tags, name='list_tags'),
    path('tags/autocomplete', views_oeuvre.OeuvreTagAutocomplete.as_view(create_field='name', validate_create=True), name='autocomplete_tag'),
    path('tags/<slug:slug>', views_collection.detail_tag, name='detail_tag'),
    path('tags/<slug:slug>/<int:page>', views_collection.detail_tag, name='detail_tag'),

    # cinemas
    re_path(r'^cinema/(?P<subpath>.*)$', views_cinema.CinemaRedirectView.as_view()),
    path('cinemas/add', views_cinema.add_cinema, name='add_cinema'),
    path('cinemas/autocomplete', views_cinema.CinemaAutocomplete.as_view(), name='autocomplete_cinema'),
    path('cinemas/<slug:slug>', views_cinema.detail_cinema, name='detail_cinema'),
    path('cinemas/<slug:slug>/delete', views_cinema.delete_cinema, name='delete_cinema'),
    path('cinemas/', views_cinema.list_cinemas, name='list_cinemas'),

    # seances
    path('seances/', views_seance.list_seances, name='list_seances'),
    path('seances/add', views_seance.add_seance, name='add_seance'),
    path('seances/<int:year>', views_seance.list_seances, name='list_seances'),

    # chronologie
    path('chronologie/', views_chronologie.get_chronologie, name='get_chronologie'),
]

