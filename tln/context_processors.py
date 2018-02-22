from django.contrib.auth.forms import AuthenticationForm

def login_form(req):
    return {"login_form": AuthenticationForm()}
