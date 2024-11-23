from django import forms
from .models import Match
from .choices import HOME_LOCATIONS, TEAMS
from odds.utils import OddsCalculator as OddsCalc

class AddMatchForm(forms.ModelForm):

    home_score = forms.IntegerField(
        min_value=0,
        max_value=150,
        initial=0,
        widget=forms.HiddenInput()
    )

    # Define 'away_score' field
    away_score = forms.IntegerField(
        min_value=0,
        max_value=150,
        initial=0,
        widget=forms.HiddenInput()
    )

    home_odds = forms.DecimalField(
        min_value=0,
        max_value=150,
        decimal_places=4,
        initial=0,
        required=False,
        widget=forms.HiddenInput()
    )
    draw_odds = forms.DecimalField(
        min_value=0,
        max_value=150,
        decimal_places=4,
        initial=0,
        required=False,
        widget=forms.HiddenInput()
    )
    away_odds = forms.DecimalField(
        min_value=0,
        max_value=150,
        decimal_places=4,
        initial=0,
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Match
        fields = [
            'match_date', 'match_time', 'home_team', 'away_team', 'match_location', 'home_score', 'away_score', 
            'home_odds', 'draw_odds', 'away_odds'
        ]
        widgets = {
            'match_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'Select match date'
            }),
            'match_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'placeholder': 'Select match time'
            }),
            'home_team': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'away_team': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'match_location': forms.Select(attrs={'class': 'form-control'}),
            'home_score': forms.HiddenInput(),
            'away_score': forms.HiddenInput(),
            'home_odds': forms.HiddenInput(),
            'draw_odds': forms.HiddenInput(),
            'away_odds': forms.HiddenInput()

        }