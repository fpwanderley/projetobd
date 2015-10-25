from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from .models import *

INACTIVE_USER = 'O usuário está inativo.'
WRONG_USERNAME_OR_PASSWORD = 'Usuário e senha não conferem.'

@login_required
def home(request):
    c = RequestContext(request)
    return render_to_response('index.html', c)

@login_required
def user_logout(request):
    logout(request)
    return redirect('core:login')

def user_login(request, next = None):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                if not next:
                    return redirect('core:home')
                else:
                    return redirect(next)

            else:
                error_message = INACTIVE_USER
        else:
            error_message = WRONG_USERNAME_OR_PASSWORD

        login_form = LoginForm()

        # Redireciona para a tela de login com mensagem de erro.
        context = RequestContext(request, {
            'error_message': error_message,
            'LoginForm':login_form,
        })
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context))

    else:
        next = ""
        if request.GET:
            next = request.GET['next']

        login_form = LoginForm()

        context = RequestContext(request, {
            'next': next,
            'LoginForm':login_form,
        })
        template = loader.get_template('login.html')
        return HttpResponse(template.render(context))

@login_required()
def user_checkin(request):

    user = request.user

    user.iniciar_turno()

