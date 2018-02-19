from datetime import datetime
from .forms import OeuvreForm, OeuvreCommentForm, SeanceForm

def oeuvre_form(req):
    form = OeuvreForm(auto_id='id_empty_%s')
    return {"oeuvre_form_empty": form}

def comment_form(req):
    date = datetime.now().strftime('%Y-%m-%d')
    form = OeuvreCommentForm({'date': date}, auto_id='id_empty_%s')
    return {"comment_form_empty": form}

def seance_form(req):
    date = datetime.now().strftime('%Y-%m-%d')
    form = SeanceForm({'date': date}, auto_id='id_empty_seance_%s')
    return {"seance_form_empty": form}
