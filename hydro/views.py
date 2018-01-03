from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from hydro.forms import *
from hydro.serializers import *

import logging


###########################################################################
#                            HYDROPONICS VIEWS                            #
#                                                                         #
###########################################################################

def HomeView(request):
    context = {'title': "Home",
               }
    return render(request, 'home/home.html', context)

def ErrorView(request):
    context = {'title': "Error",
               }
    return render(request, 'shared/error.html', context)

def NavbarView(request):
    context = {'title': "Navbar"}
    return render(request, 'shared/navbar.html', context)

def SidebarView(request):
    context = {'title': "Sidebar",
               'user_role': "student",  # fill this in
    }
    return render(request, 'shared/sidebar.html', context)

def AnalyticsView(request):
    context = {'title': "Analytics",
               }
    return render(request, 'hydro/home_elements/analytics.html', context)

def StatusView(request):
    context = {'title': "Status",
               }
    return render(request, 'hydro/home_elements/status.html', context)

def WeatherView(request):
    context = {'title': "Weather",
               }
    return render(request, 'hydro/home_elements/weather.html', context)

def ReportView(request):
    context = {'title': "Reports",
               }
    return render(request, 'hydro/home_elements/report.html', context)

def ShiftsView(request):
    context = {'title': "Shifts",
               }
    return render(request, 'hydro/home_elements/shifts.html', context)

def DailyView(request):
    context = {'title': "Daily",
               }
    return render(request, 'hydro/student_elements/daily.html', context)