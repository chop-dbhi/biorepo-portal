from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import logout_then_login, LoginView
from django.contrib.auth import authenticate, login
from django.contrib.flatpages.models import FlatPage
from django.views.decorators.cache import never_cache
from django.core.cache import cache

from accounts.utils import throttle_login, clear_throttled_login
from redis.exceptions import ConnectionError

from .forms import BrpAuthenticationForm

import re

@never_cache
def throttled_login(request):
    "Displays the login form and handles the login action."
    is_IE = False
    user_agent = request.META['HTTP_USER_AGENT']

    # if the user is already logged-in, simply redirect them to the entry page
    if request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    if (re.findall(r'MSIE', user_agent) or re.findall(r'Trident', user_agent)):
        is_IE = True
    template_name = 'accounts/login.html'

    login_allowed = request.session.get('login_allowed', True)
    if request.method == 'POST':
        # if the session has already been flagged to not allow login attempts, then
        # simply redirect back to the login page
        if not login_allowed:
            return HttpResponseRedirect(settings.LOGIN_URL)
        # Check if cache is available
        try:
            cache.get('')
        except ConnectionError:
            form = {
                'non_field_errors': ['Redis not connected. Unable to create session.']
            }
            return render(request, template_name, {
                'form': form,
                'is_IE': is_IE,
            })
        except:
            raise

        login_allowed = throttle_login(request)

        if login_allowed:
            user = authenticate(request,
                                username=request.POST['email'],
                                password=request.POST['password'])
            if user is not None:
                request.META['action'] = 'Login successful.'
                # We know if the response is a redirect, the login
                # was successful, thus we can clear the throttled login counter
                clear_throttled_login(request)
                login(request, user)

                return redirect('#/')
            else:
                # TODO add an error message for user
                return redirect('login')

    return render(request, template_name, {
        'login_not_allowed': not login_allowed,
        'is_IE': is_IE,
    })


@never_cache
def eula(request, readonly=True, redirect_to=None):
    redirect_to = redirect_to or settings.LOGIN_REDIRECT_URL

    if request.method == 'POST':
        # only if these agree do we let them pass, otherwise they get logged out
        if request.POST.get('decision', '').lower() == 'i agree':
            request.user.profile.eula = True
            request.user.profile.save()
            return HttpResponseRedirect(redirect_to)
        return logout_then_login(request)

    flatpage = FlatPage.objects.get(url='/eula/')
    return render(request, 'accounts/eula.html', {
        'flatpage': flatpage,
        'readonly': readonly,
    })
