from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .models import *

def prelogin(request):

    if request.user.is_authenticated():
        return redirect('home/')

    return login(request)

# @login_required
def home(request):

    c = RequestContext(request)
    return render_to_response('index.html', c)


def login(request):

    c = RequestContext(request)
    return render_to_response('login.html', c)