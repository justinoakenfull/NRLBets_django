from django import forms
from .models import Match
from .choices import HOME_LOCATIONS, TEAMS

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
            'home_odds': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter home odds',
                'step': '0.01'
            }),
            'draw_odds': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter draw odds',
                'step': '0.01'
            }),
            'away_odds': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter away odds',
                'step': '0.01'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate team choices dynamically
        # team_choices = [(key, value['name']) for key, value in TEAMS.items()]
        # self.fields['home_team'].choices = team_choices
        # self.fields['away_team'].choices = team_choices

        # Populate location choices dynamically
        location_choices = [(key, value) for key, value in HOME_LOCATIONS.items()]
        self.fields['match_location'].choices = location_choices

        print(self.fields['home_team'].choices)
        print(self.fields['away_team'].choices)