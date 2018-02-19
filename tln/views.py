from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
#from django.shortcuts import render


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

#def error_404(req):
#    return render(req, 'zinnia/error_404.html', {})
