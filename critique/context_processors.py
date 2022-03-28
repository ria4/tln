from datetime import datetime
from .forms import CinemaForm, CommentaireForm, OeuvreForm, SeanceForm


def oeuvre_form(req):
    form = OeuvreForm(auto_id='id_empty_%s')
    form.fields["title_vf"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"oeuvre_form_empty": form}

def comment_form(req):
    date = datetime.now().strftime('%Y-%m-%d')
    form = CommentaireForm({'date': date}, auto_id='id_empty_%s')
    form.fields["content"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"comment_form_empty": form}

def cinema_form(req):
    visited = datetime.fromtimestamp(0).strftime('%Y-%m-%d')
    form = CinemaForm({'visited': visited}, auto_id='id_empty_cinema_%s')
    form.fields["name"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"cinema_form_empty": form}

def seance_form(req):
    date = datetime.now().strftime('%Y-%m-%d')
    form = SeanceForm({'date': date}, auto_id='id_empty_seance_%s')
    form.fields["cinema"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"seance_form_empty": form}
