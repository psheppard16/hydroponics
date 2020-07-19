from django.shortcuts import render, redirect
from hydro.forms import *
from hydro.serializers import *
from django.views.generic.edit import FormView
from django.forms.models import model_to_dict
import datetime

import logging

log = logging.getLogger('hydro')


###########################################################################
#                            HYDROPONICS VIEWS                            #
#                                                                         #
###########################################################################

def HomeView(request):
    context = {'title': "Home",
               'user': request.user,
               'chemical_setings': ChemicalSettings.objects.get(id=1),
               'waste_setings': WasteSettings.objects.get(id=1)
               }
    return render(request, 'home/home.html', context)


def ErrorView(request):
    context = {'title': "Error",
               }
    return render(request, 'shared/error.html', context)


class ChemicalSettingsView(FormView):
    template_name = 'chemical/chemical.html'
    form_class = ChemicalSettingsForm
    success_url = '/?updated=success'

    def get_initial(self):
        initial = super(ChemicalSettingsView, self).get_initial()
        initial.update(model_to_dict(ChemicalSettings.objects.get(id=1)))
        return initial

    def get_form(self):
        return ChemicalSettingsForm(instance=ChemicalSettings.objects.get(id=1), **self.get_form_kwargs())

    def form_valid(self, form):
        saved = form.save(commit=False)
        ChemicalSettings.objects.filter(pk=1).update(**model_to_dict(saved))
        response = redirect('chemical')
        return response


class WasteSettingsView(FormView):
    template_name = 'waste/waste.html'
    form_class = ChemicalSettingsForm
    success_url = '/?updated=success'

    def get_initial(self):
        initial = super(WasteSettingsView, self).get_initial()
        initial.update(model_to_dict(WasteSettings.objects.get(id=1)))
        return initial

    def get_form(self):
        return WasteSettingsForm(instance=WasteSettings.objects.get(id=1), **self.get_form_kwargs())

    def form_valid(self, form):
        saved = form.save(commit=False)
        WasteSettings.objects.filter(pk=1).update(**model_to_dict(saved))
        response = redirect('waste')
        return response


def ControlEditView(request):
    """

        :param request:
        :return:
    """
    if request.POST:
        form = RequestForm(request.POST)
        if form.is_valid():
            saved = form.save(commit=False)
            saved.save()
            form.save_m2m()
            response = redirect('home')
            response['Location'] += '?requested=success'
            return response
        else:
            log.error(form.errors)
            response = redirect('home')
            response['Location'] += '?requested=failed'
            return response
