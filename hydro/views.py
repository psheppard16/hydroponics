from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from hydro.models import *
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
               'config': Configuration.models.get(),
               'pH_data': Data.objects.filter(type=Type(type="pH")),
               'EC_data': Data.objects.filter(type=Type(type="EC")),
               'ORP_data': Data.objects.filter(type=Type(type="ORP")),
               }
    return render(request, 'home/home.html', context)

def ErrorView(request):
    context = {'title': "Error",
               }
    return render(request, 'shared/error.html', context)