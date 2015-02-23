# This Python file uses the following encoding: utf-8
import logging

from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse
from django.contrib.auth import (logout as auth_logout, login as auth_login, get_user_model, authenticate)
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, resolve_url

from sdauth.forms import AuthForm
from sdauth.models import User

logger = logging.getLogger('__name__')



def logout(request):
    auth_logout(request)
    return redirect(reverse('auth:login'))


def login(request):
    if request.user.is_authenticated():
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))

    auth_logout(request)
    context = {}
    if request.method == 'POST':
        form = AuthForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()

            auth_login(request, user)

            return redirect(request.GET.get('next') or settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthForm(request)

    context['login_form'] = form

    return render(request, 'auth/login.jinja', context)