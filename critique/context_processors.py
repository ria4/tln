from datetime import datetime

from critique.forms import (
    CinemaForm,
    CommentaireForm,
    OeuvreForm,
    OeuvreSpanForm,
    SeanceForm,
    TierListForm,
)


def oeuvre_form(req):
    year = datetime.now().strftime('%Y')
    form = OeuvreForm({'year': year}, auto_id='id_empty_%s')
    form.fields["mtype"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"oeuvre_form_empty": form}

def oeuvrespan_form(req):
    date_start = datetime.now().strftime('%Y-%m-%d')
    date_end = datetime.now().strftime('%Y-%m-%d')
    form = OeuvreSpanForm(
        {'date_start': date_start, 'date_end': date_end},
        auto_id='id_empty_oeuvrespan_%s',
    )
    form.fields["ongoing"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"oeuvrespan_form_empty": form}

def comment_form(req):
    date = datetime.now().strftime('%Y-%m-%d')
    form = CommentaireForm({'date': date}, auto_id='id_empty_%s')
    form.fields["content"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"comment_form_empty": form}

def cinema_form(req):
    visited = datetime.now().strftime('%Y-%m-%d')
    form = CinemaForm({'visited': visited}, auto_id='id_empty_cinema_%s')
    form.fields["name"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"cinema_form_empty": form}

def seance_form(req):
    date = datetime.now().strftime('%Y-%m-%d')
    form = SeanceForm({'date': date}, auto_id='id_empty_seance_%s')
    form.fields["cinema"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"seance_form_empty": form}

def tierlist_form(req):
    form = TierListForm(auto_id='id_empty_tierlist_%s')
    form.fields["name"].widget.attrs.update({"class": "focus-on-reveal"})
    return {"tierlist_form_empty": form}
