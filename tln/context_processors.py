from django.contrib.auth.forms import AuthenticationForm

def login_form(req):
    f = AuthenticationForm()
    f.fields["username"].label = "Identifiant"
    mobile_attrs = { "autocomplete": "off",
                     "autocapitalize": "off",
                     "spellcheck": "false" }
    f.fields["username"].widget.attrs.update(mobile_attrs)
    return {"login_form": f}

def android(req):
    user_agent = req.META.get("HTTP_USER_AGENT")
    if user_agent:
        return {"android": "android" in user_agent.lower()}
    else:
        return {"android": False}
