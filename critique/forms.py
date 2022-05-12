"""
BooleanField must be required=False, because of some django nonsense.
Also, the validation data written here is mostly useless, thanks to client-side validation.
"""

from dal.autocomplete import ModelSelect2
from django import forms
from django.db.models import Q

from .models import Cinema, Oeuvre


OEUVRES_TYPES = [
    ('film', 'Film'),
    ('serie', 'Série'),
    ('album', 'Album'),
    ('jeu', 'Jeu'),
    ('livre', 'Livre'),
    ('bd', 'BD')
 ]


class DateInput(forms.DateInput):
    """
    Use this custom widget to make the default type for DateField 'date'
    instead of 'text'. Note that only recent browsers support this.
    """
    input_type = 'date'

class OeuvreForm(forms.Form):
    mtype = forms.ChoiceField(label="type", choices=OEUVRES_TYPES)
    title_vf = forms.CharField(label="titre vf", max_length=200)
    title_vo = forms.CharField(label="titre vo", max_length=200, required=False)
    title_alt = forms.CharField(label="titre alt", max_length=200, required=False)
    artists = forms.CharField(label="artistes", max_length=1000)
    year = forms.IntegerField(label="année", max_value=2100)
    imdb_id = forms.RegexField(label="imdb id", regex='^tt[0-9]{7,8}$', required=False)
    image_link = forms.URLField(label="url image", required=False)
    tags = forms.CharField(label="tags", required=False)
    envie = forms.BooleanField(label="envie", required=False)

class CommentaireForm(forms.Form):
    title = forms.CharField(label="titre", max_length=200, required=False)
    date = forms.DateField(label="date", widget=DateInput)
    no_month = forms.BooleanField(label="sans mois", required=False)
    no_day = forms.BooleanField(label="sans jour", required=False)
    content = forms.CharField(label="contenu", widget=forms.Textarea)

class CinemaForm(forms.Form):
    name = forms.CharField(label="nom", max_length=100)
    name_short = forms.CharField(label="nom court", max_length=100, required=False)
    name_long = forms.CharField(label="nom long", max_length=100)
    location = forms.CharField(label="lieu", max_length=100)
    comment = forms.CharField(label="contenu", widget=forms.Textarea(attrs={'rows': 2}), required=False)
    visited = forms.DateField(label="visité le", widget=DateInput)

class SeanceForm(forms.Form):
    cinema = forms.ModelChoiceField(
        label="cinéma",
        queryset=Cinema.objects.exclude(Q(name="UGC") | Q(name="MK2")),
        widget=ModelSelect2(
            url='autocomplete_cinema',
            attrs={'data-minimum-input-length': 2},
        )
    )
    date = forms.DateField(label="date", widget=DateInput)
    hour = forms.CharField(label="heure", max_length=5)
    #no_month = forms.BooleanField(label="sans mois", required=False)
    #no_day = forms.BooleanField(label="sans jour", required=False)
    film = forms.ModelChoiceField(
        label="film",
        required=False,
        queryset=Oeuvre.objects.filter(info__mtype='film'),
        widget=ModelSelect2(
            url='autocomplete_film',
            attrs={'data-minimum-input-length': 3},
        )
    )
    seance_title = forms.CharField(label="ou titre", max_length=200, required=False)
