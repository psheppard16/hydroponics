from django.conf.urls import include, url
from django.contrib import admin
import os
from massadmin import urls as massadmin_urls
from massadmin import mass_change_selected
from hydro.urls import status_api_patterns
from hydro.views import *

admin.site.add_action(mass_change_selected)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'hydro'),
)

handler403 = 'hydro.templates.permission_denied_view'

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include(massadmin_urls)),

    url(r'^status/', include(status_api_patterns)),
    url(r'^hydro/student', HydroStudentView, name="hydro_student"),
    url(r'^hydro/full_time', HydroFullTimeView, name="hydro_full_time"),
    url(r'^hydro/manager', HydroManagerView, name="hydro_manager"),
    url(r'^schedule/student', ScheduleStudentView, name="schedule_student"),
    url(r'^schedule/full_time', ScheduleFullTimeView, name="schedule_full_time"),
    url(r'^schedule/manager', ScheduleManagerView, name="schedule_manager"),
    url(r'^settings/full_time', SettingsFullTimeView, name="settings_full_time"),
    url(r'^settings/manager', SettingsManagerView, name="settings_manager"),
    url(r'^error', ErrorView, name="error"),
    url(r'^policies', PoliciesView, name="policies"),
]
