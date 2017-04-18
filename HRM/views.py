__author__ = 'Tusfiqur'
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
def loginPage(request, message):

    render(request, 'start.html')

def login(request):
    context = {}
    try:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request,user)
            else:
                context['error'] = 'Non active user'
        else:
            context['error'] = 'Wrong username or password'
    except:
        context['error'] = ''

    populateContext(request,context)
    if context['authenticated']:
        return HttpResponseRedirect(reverse('home'))

    return render(request, 'start.html', context)

def logout(request):
    context = {}
    try:
        auth_logout(request)
    except:
        context['error'] = 'some error occured'

    populateContext(request,context)
    return render(request, 'start.html', context)


def populateContext(request, context):
    context['authenticated'] = request.user.is_authenticated()
    if context['authenticated'] == True:
        context['username'] = request.user.username


@login_required
def home(request):

    return render(request, 'home.html')

@login_required
def features(request):

    return render(request, 'new_features.html')