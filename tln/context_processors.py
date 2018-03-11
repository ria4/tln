from django.contrib.auth.forms import AuthenticationForm

def login_form(req):
    return {"login_form": AuthenticationForm()}

def android(req):
    return {"android": "android" in req.META["HTTP_USER_AGENT"].lower()}
