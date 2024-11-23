from django.shortcuts import render, redirect
from .forms import AddMatchForm
from .choices import HOME_LOCATIONS, TEAMS, TEAMS_KEYS
from .models import Match
from odds.utils import OddsCalculator as OddsCalc

# Create your views here.

def AddMatch(request):

    if request.method == 'POST':
        form = AddMatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            # Get the odds
            oddsCalc = OddsCalc()
            odds = oddsCalc.predict_match_odds(TEAMS_KEYS[form.cleaned_data['home_team']], TEAMS_KEYS[form.cleaned_data['away_team']])
            # Set the odds
            match.home_odds = odds['home_odds']
            match.draw_odds = odds['draw_odds']
            match.away_odds = odds['away_odds']
            # Save the match
            match.save()
            return render(request, "matches/add_match.html", {'form': form, 'HOME_LOCATIONS': HOME_LOCATIONS, 'TEAMS': TEAMS, 'errors': form.errors})
        print("Form is not valid")
        print(match.errors)
        return render(request, "matches/add_match.html", {'form': form, 'HOME_LOCATIONS': HOME_LOCATIONS, 'TEAMS': TEAMS, 'errors': form.errors})
    else:


        form = AddMatchForm(initial={'home_score': 0, 'away_score': 0})
    return render(request, "matches/add_match.html", {'form': form, 'HOME_LOCATIONS': HOME_LOCATIONS, 'TEAMS': TEAMS, 'errors': form.errors})

def upcomingMatches(request):
    matches = Match.objects.all()
    update_match_odds(matches)
    matches = matches.order_by('match_date', 'match_time')
    team_colors = {}

    for match in matches:
        # Dynamically add color attributes
        match.home_team_color = TEAMS.get(match.home_team, {}).get("color", "#CCCCCC")
        match.away_team_color = TEAMS.get(match.away_team, {}).get("color", "#CCCCCC")
        # Rename teams to full names
        match.home_team_full = TEAMS.get(match.home_team, {}).get("name", match.home_team)
        match.away_team_full = TEAMS.get(match.away_team, {}).get("name", match.away_team)


    odds = OddsCalc()
    
    return render(request, "matches/upcoming_matches.html", {'matches': matches, 'TEAMS': TEAMS})

def update_match_odds(matches):
    oddsCalc = OddsCalc()
    for match in matches:
        odds = oddsCalc.predict_match_odds(TEAMS_KEYS[match.home_team], TEAMS_KEYS[match.away_team])
        match.home_odds = odds['home_odds']
        match.draw_odds = odds['draw_odds']
        match.away_odds = odds['away_odds']
        match.save()