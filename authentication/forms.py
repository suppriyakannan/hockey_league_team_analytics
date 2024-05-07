from django import forms
from .models import PossessionData

class PossessionDataForm(forms.ModelForm):
    class Meta:
        model = PossessionData
        fields = ['match_number', 'team1_name', 'team2_name', 'team1_possession_percentage', 'team2_possession_percentage']
from django import forms
from .models import Injury

class InjuryForm(forms.ModelForm):
    class Meta:
        model = Injury
        fields = ['player', 'injury_type', 'injury_details', 'body_part', 'status', 'date_reported']
        widgets = {
            'date_reported': forms.DateInput(attrs={'type': 'date'})
        }
