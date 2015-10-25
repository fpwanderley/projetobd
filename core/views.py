from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import *


def home(request):

    c = RequestContext(request)
    print('ASD')
    return render_to_response('index.html', c)