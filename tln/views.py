from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from tln.constants import LOGIN_FAILED_WRONG_CREDENTIALS
from tln.utils import qs_update_loginfail


# Login

@require_http_methods(["GET", "POST"])
def login_view(req):
    if req.method == "GET":
        url = reverse("home") + "?" + req.GET.urlencode(safe="/") + "#login"
        return redirect(url)

    username = req.POST.get('username')
    password = req.POST.get('password')
    user = authenticate(req, username=username, password=password)

    url = req.GET.get("next", "")
    if not url_has_allowed_host_and_scheme(
        url,
        allowed_hosts={req.get_host()},
        require_https=True,
    ):
        url = reverse("home")

    if user is not None:
        login(req, user)
    else:
        url = reverse("home")
        url += "?" + qs_update_loginfail(req, LOGIN_FAILED_WRONG_CREDENTIALS) + "#login"
    return redirect(url)

@require_http_methods(["GET", "POST"])
def logout_view(req):
    if req.user.is_authenticated:
        logout(req)
    return redirect(req.META.get("HTTP_REFERER", "home"))
