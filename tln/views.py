from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from tln.utils import remove_query_param


# Login

def login_view(req):
    redirect_url = remove_query_param(req.META.get('HTTP_REFERER'), "loginfail")
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(req, username=username, password=password)
    if user is not None:
        login(req, user)
    else:
        redirect_url += "?loginfail=1" + "#login"
    return HttpResponseRedirect(redirect_url)

def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
