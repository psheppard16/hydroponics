from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from hydro.models import *
from hydro.forms import *
from hydro.serializers import *
from django.urls import reverse

import logging
log = logging.getLogger('hydro')

###########################################################################
#                            HYDROPONICS VIEWS                            #
#                                                                         #
###########################################################################

def HomeView(request):



    context = {'title': "Home",
               'user': request.user,
               'config': Configuration.objects.get(id=1),
               'pH_data': Data.objects.filter(type=Type(type="pH")),
               'EC_data': Data.objects.filter(type=Type(type="EC")),
               'ORP_data': Data.objects.filter(type=Type(type="ORP")),
               }
    return render(request, 'home/home.html', context)


def ErrorView(request):
    context = {'title': "Error",
               }
    return render(request, 'shared/error.html', context)


def ConfigurationEditView(request):
    """

        :param request:
        :return:
    """

    if request.POST:
        config = Configuration.objects.get(id=1)
        form = ConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            saved = form.save(commit=False)
            saved.save()
            form.save_m2m()
            response = redirect('home')
            response['Location'] += '?updated=success'
            return response
        else:
            log.error(form.errors)
            response = redirect('home')
            response['Location'] += '?updated=failed'
            return response

def ControlEditView(request):
    """

        :param request:
        :return:
    """
    if request.POST:
        config = Configuration.objects.get(id=1)
        form = ConfigurationForm(request.POST, instance=config)
        if form.is_valid():
            saved = form.save(commit=False)
            saved.save()
            form.save_m2m()
            response = redirect('home')
            response['Location'] += '?updated=success'
            return response
        else:
            log.error(form.errors)
            response = redirect('home')
            response['Location'] += '?updated=failed'
            return response