from django.conf.urls import include, url
from django.contrib import admin
import os
from hydro.urls import hydro_patterns
from hydro.views import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'hydro'),
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hydro/', include(hydro_patterns)),
]
