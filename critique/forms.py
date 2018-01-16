
from django import forms
# BooleanField must be required=False, because of some django nonsense.

OEUVRES_TYPES = [('film', 'Film'),
                 ('serie', 'Série'),
                 ('album', 'Album'),
                 ('jeu', 'Jeu'),
                 ('livre', 'Livre'),
                 ('bd', 'BD')]


class OeuvreForm(forms.Form):
    type = forms.ChoiceField(choices=OEUVRES_TYPES)
    title_vf = forms.CharField(max_length=1000)
    title_vo = forms.CharField(max_length=1000, required=False)
    title_alt = forms.CharField(max_length=1000, required=False)
    artists = forms.CharField(max_length=1000)
    year = forms.IntegerField(max_value=2100)
    imdb_id = forms.RegexField(regex='^tt[0_9]{7}$', required=False)
    image_link = forms.URLField(required=False)
    tags = forms.CharField(required=False)
    envie = forms.BooleanField(required=False)

class OeuvreCommentForm(forms.Form):
    title = forms.CharField(max_length=500, required=False)
    date = forms.DateField()
    date_month_unknown = forms.BooleanField(required=False)
    date_day_unknown = forms.BooleanField(required=False)
    content = forms.CharField()

class CinemaForm(forms.Form):
    name = forms.CharField(max_length=100)
    comment = forms.CharField(widget=forms.Textarea)
    visited = forms.DateField()

