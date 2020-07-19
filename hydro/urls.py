import os
from django.conf.urls import include, url
from rest_framework import routers
from hydro.api import *
from hydro.views import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'hydro'),
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'data', DataViewSet)
router.register(r'data', DataTypeViewSet)

hydro_patterns = [
    url(r'^home', HomeView, name="home"),
    url(r'^chemical', ChemicalSettingsView.as_view(), name="chemical"),
    url(r'^waste', WasteSettingsView.as_view(), name="waste"),
    url(r'^control', ControlEditView, name="control"),
    url(r'^error', ErrorView, name="error"),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]