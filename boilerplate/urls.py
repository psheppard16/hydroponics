from django.conf.urls import include, url
from django.contrib import admin
import os
from hydro.urls import status_api_patterns
from hydro.views import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'hydro'),
)

handler403 = 'hydro.templates.permission_denied_view'

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^status/', include(status_api_patterns)),
    url(r'^hydro/home', HomeView, name="home"),
    url(r'^error', ErrorView, name="error"),
]
