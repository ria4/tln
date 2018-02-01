
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect


# Login

def login_view(req):
    username = req.POST['username']
    password = req.POST['password']
    user = authenticate(req, username=username, password=password)
    if user is not None:
        login(req, user)
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))

