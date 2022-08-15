from django.contrib.auth.forms import AuthenticationForm

from tln.constants import LOGIN_FORM_ERROR_CODES_MAP


def login_form(req):
    f = AuthenticationForm()
    f.fields["username"].label = "Identifiant"
    additional_attrs = { "class": "focus-on-reveal" }
    mobile_attrs = { "autocomplete": "off",
                     "autocapitalize": "off",
                     "spellcheck": "false" }
    f.fields["username"].widget.attrs.update({**additional_attrs, **mobile_attrs})
    return {"login_form": f, "login_error_codes": LOGIN_FORM_ERROR_CODES_MAP}

def android(req):
    user_agent = req.META.get("HTTP_USER_AGENT")
    if user_agent:
        return {"android": "android" in user_agent.lower()}
    else:
        return {"android": False}

def webkit(req):
    user_agent = req.META.get("HTTP_USER_AGENT")
    if user_agent:
        return {"webkit": "webkit" in user_agent.lower()}
    else:
        return {"webkit": False}
