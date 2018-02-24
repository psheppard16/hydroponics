from django.conf.urls import include, url
from django.contrib import admin
import os
from hydro.urls import hydro_api_patterns
from hydro.views import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'hydro'),
)

handler403 = 'hydro.templates.permission_denied_view'

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/', include(hydro_api_patterns)),
    url(r'^home', HomeView, name="home"),
    url(r'^chemical', ChemicalSettingsView, name="chemical_settings"),
    url(r'^waste', WasteSettingsView, name="waste_settings"),
    url(r'^control', ControlEditView, name="control"),
    url(r'^error', ErrorView, name="error"),
]
