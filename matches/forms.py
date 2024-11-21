from django import forms
from .models import Match
from .choices import HOME_LOCATIONS, TEAMS

class AddMatchForm(forms.Form):
    match_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Select match date and time'
        })
    )
    match_time = forms.TimeField(
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
            'placeholder': 'Select match time'
        })
    )
    home_team = forms.ChoiceField(
        choices=[(key, value) for key, value in TEAMS.items()],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    away_team = forms.ChoiceField(
        choices=[(key, value) for key, value in TEAMS.items()],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    magic_round = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input',
                                          'id': 'magic_round'})
    )
    match_location = forms.ChoiceField(
        choices=[(key, value) for key, value in HOME_LOCATIONS.items()],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    home_score = forms.IntegerField(
        min_value=0,
        max_value=150,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter home team score',
            'step': 1
        })
    )
    away_score = forms.IntegerField(
        min_value=0,
        max_value=150,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter away team score',
            'step': 1
        })
    )
    home_odds = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter home odds',
            'step': '0.01'
        })
    )
    draw_odds = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter draw odds',
            'step': '0.01'
        })
    )
    away_odds = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter away odds',
            'step': '0.01'
        })
    )
