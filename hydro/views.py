from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from hydro.forms import *
from hydro.serializers import *

import logging


###########################################################################
#                            HYDROPONICS VIEWS                            #
#                                                                         #
###########################################################################

def HomeView(request):
    context = {'title': "Home",
               'user': request.user,
               }
    return render(request, 'home/home.html', context)

def ErrorView(request):
    context = {'title': "Error",
               }
    return render(request, 'shared/error.html', context)