from django.contrib.auth.forms import AuthenticationForm

def login_form(req):
    f = AuthenticationForm()
    f.fields["username"].label = "Identifiant"
    return {"login_form": f}

def android(req):
    return {"android": "android" in req.META["HTTP_USER_AGENT"].lower()}
