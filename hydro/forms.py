from django import forms
from hydro.models import *

class ChemicalSettingsForm(forms.ModelForm):
    """Form for editing chemical chemical_settings from POST requests

        """
    class Meta:
        model = ChemicalSettings
        exclude = ['last_pH_change', 'last_nutrient_change', 'last_ORP_change']

class WasteSettingsForm(forms.ModelForm):
    """Form for editing waste chemical_settings from POST requests

        """
    class Meta:
        model = WasteSettings
        exclude = ['last_water_change']

class RequestForm(forms.ModelForm):
    """Form for creating action requests from POST requests

        """
    class Meta:
        model = Request
        exclude = ['exec_time', 'request_time', 'status']