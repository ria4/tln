
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from .forms import OeuvreForm, OeuvreCommentForm

def oeuvre_form_dispenser(req):
    form = OeuvreForm(auto_id='id_empty_%s')
    return {"oeuvre_form_empty": form}

def comment_form_dispenser(req):
    date = datetime.now().strftime('%Y-%m-%d')
    form = OeuvreCommentForm({'date': date}, auto_id='id_empty_%s')
    return {"comment_form_empty": form}

def login_form_dispenser(req):
    return {"login_form": AuthenticationForm()}

