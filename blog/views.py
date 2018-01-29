
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render


def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
    return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
