"""
BooleanField must be required=False, because of some django nonsense.
Also, the validation data written here is mostly useless, thanks to client-side validation.
"""

from django import forms


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
    mtype = forms.ChoiceField(choices=OEUVRES_TYPES)
    title_vf = forms.CharField(max_length=200)
    title_vo = forms.CharField(max_length=200, required=False)
    title_alt = forms.CharField(max_length=200, required=False)
    artists = forms.CharField(max_length=1000)
    year = forms.IntegerField(max_value=2100)
    imdb_id = forms.RegexField(regex='^tt[0-9]{7,8}$', required=False)
    image_link = forms.URLField(required=False)
    tags = forms.CharField(required=False)
    envie = forms.BooleanField(required=False)

class CommentaireForm(forms.Form):
    title = forms.CharField(max_length=200, required=False)
    date = forms.DateField(widget=DateInput)
    no_month = forms.BooleanField(required=False)
    no_day = forms.BooleanField(required=False)
    content = forms.CharField(widget=forms.Textarea)

class CinemaForm(forms.Form):
    name = forms.CharField(max_length=100)
    name_short = forms.CharField(max_length=100, required=False)
    name_long = forms.CharField(max_length=100)
    location = forms.CharField(max_length=100)
    comment = forms.CharField(widget=forms.Textarea, required=False)
    visited = forms.DateField(widget=DateInput)

class SeanceForm(forms.Form):
    cinema = forms.CharField(max_length=100)
    date = forms.DateField(widget=DateInput)
    hour = forms.CharField(max_length=5)
    no_month = forms.BooleanField(required=False)
    film_slug = forms.CharField(max_length=200, required=False)
    seance_title = forms.CharField(max_length=200, required=False)
