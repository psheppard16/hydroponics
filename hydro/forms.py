from django import forms
from hydro.models import *

class ConfigurationForm(forms.ModelForm):
    """Form for creating configurations from POST requests

        """
    class Meta:
        model = Configuration
        exclude = ['last_pH_change', 'last_nutrient_change', 'last_water_change']

class RequestForm(forms.ModelForm):
    """Form for creating configurations from POST requests

        """
    class Meta:
        model = Request
        exclude = ['exec_time', 'request_time', 'status']