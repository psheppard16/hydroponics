from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from hydro.forms import *
from hydro.serializers import *

import logging


###########################################################################
#                             TIMECLOCK VIEWS                             #
#                                                                         #
###########################################################################

def HydroStudentView(request):
    context = {'title': "Hydro Student",
               'user_net_id': "",  # fill this in
               'user_role': "",  # fill this in
               'currently_working': [],  # fill this in

               }
    return render(request, 'hydro/student.html', context)

def StatusView(request):
    context = {'title': "Sidebar",
               }
    return render(request, 'hydro/student_elements/status.html', context)

def WeatherView(request):
    context = {'title': "Sidebar",
               }
    return render(request, 'hydro/student_elements/weather.html', context)

def ReportView(request):
    context = {'title': "Sidebar",
               }
    return render(request, 'hydro/student_elements/report.html', context)

def ShiftsView(request):
    context = {'title': "Sidebar",
               }
    return render(request, 'hydro/student_elements/shifts.html', context)

def StudentAnalyticsView(request):
    context = {'title': "Analytics",
               }
    return render(request, 'hydro/student_elements/analytics.html', context)

def DailyView(request):
    context = {'title': "Daily",
               }
    return render(request, 'hydro/student_elements/daily.html', context)




def HydroFullTimeView(request):
    context = {'title': "Hydro Full Time"}
    return render(request, 'hydro/full_time.html', context)

def FullTimeClockEventsView(request):
    context = {'title': "Clock Events",
               }
    return render(request, 'hydro/full_time_elements/clock_events.html', context)

def FullTimeEditUserView(request):
    context = {'title': "Edit User",
               }
    return render(request, 'hydro/full_time_elements/edit_user.html', context)

def FullTimeReportsPanelOneView(request):
    context = {'title': "Reports Panel One",
               }
    return render(request, 'hydro/full_time_elements/full_time_reports_panel_one.html', context)

def FullTimeReportsPanelTwoView(request):
    context = {'title': "Reports Panel Two",
               }
    return render(request, 'hydro/full_time_elements/full_time_reports_panel_two.html', context)



def HydroManagerView(request):
    context = {'title': "Hydro Manager"}
    return render(request, 'hydro/manager.html', context)

def ManagerAnalyticsView(request):
    class Center:   #temporary testing class, should be removed once models are set up
        def __init__(self, name, currently_working):
            self.name = name
            self.currently_working = currently_working

    context = {'title': "Analytics",
               'max_list': list(reversed([x for x in range(5  + 1)])),
               'row_size': 100 / (5 + 1),
               'centers': [Center("CC", ["student1", "fts2"]), Center("HC", ["student4"]), Center("HC", ["student7", "fts3"]), Center("HC", [])],
               }
    return render(request, 'hydro/manager_elements/analytics.html', context)

def ManagerClockEventsView(request):
    class ClockEvent:   #temporary testing class, should be removed once models are set up
        def __init__(self, type, name, time, date, notes):
            self.type = type
            self.name = name
            self.time = time
            self.date = date
            self.notes = notes
    context = {'title': "Clock Events",
               'date_start': "12/2/2017",
               'date_stop': "12/3/2017",
               'clock_events': [ClockEvent("in", "Preston Sheppard", "10:15AM", "12/13/2017", "test event"),
                                ClockEvent("out", "Preston Sheppard", "12:15PM", "12/13/2017", "test event")]
               }
    return render(request, 'hydro/manager_elements/clock_events.html', context)

def ManagePanelOneView(request):
    context = {'title': "Manage Panel One",
               }
    return render(request, 'hydro/manager_elements/manage_panel_one.html', context)

def ManagePanelTwoView(request):
    context = {'title': "Manage Panel Two",
               }
    return render(request, 'hydro/manager_elements/manage_panel_two.html', context)

def ManagePanelThreeView(request):
    context = {'title': "Manage Panel Three",
               }
    return render(request, 'hydro/manager_elements/manage_panel_three.html', context)

def ManagerReportsPanelOneView(request):
    context = {'title': "Reports Panel One",
               }
    return render(request, 'hydro/manager_elements/manager_reports_panel_one.html', context)

def ManagerReportsPanelTwoView(request):
    context = {'title': "Reports Panel Two",
               }
    return render(request, 'hydro/manager_elements/manager_reports_panel_two.html', context)

def ManagerReportsPanelThreeView(request):
    context = {'title': "Reports Panel Three",
               }
    return render(request, 'hydro/manager_elements/manager_reports_panel_three.html', context)

def ManagerReportsPanelFourView(request):
    context = {'title': "Reports Panel Four",
               }
    return render(request, 'hydro/manager_elements/manager_reports_panel_four.html', context)



###########################################################################
#                              SCHEDULE VIEWS                             #
#                                                                         #
###########################################################################

def ScheduleStudentView(request):
    context = {'title': "Schedule Student"}
    return render(request, 'schedule/student.html', context)

def StudentScheduleView(request):
    context = {'title': "Student Schedule"}
    return render(request, 'schedule/student_elements/schedule.html', context)

def StudentPostedShiftsView(request):
    context = {'title': "Student Posted Shifts"}
    return render(request, 'schedule/student_elements/posted_shifts.html', context)


def StudentAvailabilityView(request):
    class requestM:   #temporary testing class, should be removed once models are set up
        def __init__(self, id, day):
            self.id = id
            self.day = day

    class conflictM:
        def __init__(self, id, day):
            self.id = id
            self.day = day

    requests = [requestM(0, "Monday")]
    conflicts = [conflictM(0, "Monday"), conflictM(1, "Monday")]
    days = ["Sunday", "Monday", "Tuesday", "Thursday", "Friday", "Saturday"]
    context = {'title': "Student Availability",
               'days': days,
               'requests': requests,
               'conflicts': conflicts
               }
    return render(request, 'schedule/student_elements/availability.html', context)



def ScheduleFullTimeView(request):
    context = {'title': "Schedule Full Time"}
    return render(request, 'schedule/full_time.html', context)

def FullTimeScheduleManagementView(request):
    context = {'title': "Full Time Schedule Management"}
    return render(request, 'schedule/full_time_elements/schedule_management.html', context)

def FullTimeSchedulerView(request):
    context = {'title': "Full Time Scheduler"}
    return render(request, 'schedule/full_time_elements/scheduler.html', context)

def FullTimePostedShiftsView(request):
    context = {'title': "Full Time Posted Shifts"}
    return render(request, 'schedule/full_time_elements/posted_shifts.html', context)



def ScheduleManagerView(request):
    context = {'title': "Schedule Manager"}
    return render(request, 'schedule/manager.html', context)

def ManagerScheduleManagementView(request):
    context = {'title': "Manager Schedule Management"}
    return render(request, 'schedule/manager_elements/schedule_management.html', context)

def ManagerSchedulerView(request):
    context = {'title': "Manager Scheduler"}
    return render(request, 'schedule/manager_elements/scheduler.html', context)

def ManagerPostedShiftsView(request):
    context = {'title': "Manager Posted Shifts"}
    return render(request, 'schedule/manager_elements/posted_shifts.html', context)

def ManagerAvailabilityView(request):
    context = {'title': "Manager availability"}
    return render(request, 'schedule/manager_elements/availability.html', context)


###########################################################################
#                              SETTINGS VIEWS                             #
#                                                                         #
###########################################################################

def SettingsManagerView(request):
    context = {'title': "Settings Manager"}
    return render(request, 'settings/manager.html', context)

def SettingsFullTimeView(request):
    context = {'title': "Settings Full Time"}
    return render(request, 'settings/full_time.html', context)


###########################################################################
#                              POLICIES VIEWS                             #
#                                                                         #
###########################################################################

def PoliciesView(request):  # fix
    context = {'title': "Policies"}
    return render(request, 'policies/student.html', context)


###########################################################################
#                               SHARED VIEWS                              #
#                                                                         #
###########################################################################

def ErrorView(request):
    context = {'title': "Error",
               'name': "",  # fill this in
               'error': "",  # fill this in
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
