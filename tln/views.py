from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils.http import is_safe_url

from tln.utils import remove_query_param, update_query_param


# Login

def login_view(req):
    redirect_url = remove_query_param(req.META.get('HTTP_REFERER'), "loginfail")
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(req, username=username, password=password)
    if user is not None:
        login(req, user)
        next_url = req.POST.get("next", None)
        if next_url:
            if not is_safe_url(next_url, req.get_host()):
                next_url = "/"
            return redirect(next_url)
    else:
        redirect_url = update_query_param(redirect_url, "loginfail", 1)
        redirect_url += "#login"
    return redirect(redirect_url)

def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
    return redirect(req.META.get('HTTP_REFERER'))
