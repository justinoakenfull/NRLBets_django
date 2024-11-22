from django.shortcuts import render, redirect
from .forms import AddMatchForm
from .choices import HOME_LOCATIONS, TEAMS
from .models import Match
from odds.utils import OddsCalculator as OddsCalc

# Create your views here.

def AddMatch(request):

    if request.method == 'POST':
        form = AddMatchForm(request.POST)
        # Process the form
        print("Processing form")
        add_match = form
        print(add_match)
        print("Checking if form is valid")
        if add_match.is_valid():
            print("Form is valid")
            add_match.save()
            print("Match saved")
            return redirect('home')
        print("Form is not valid")
        print(add_match.errors)
        return render(request, "matches/add_match.html", {'form': form, 'HOME_LOCATIONS': HOME_LOCATIONS, 'TEAMS': TEAMS, 'errors': form.errors})
    else:
        form = AddMatchForm(initial={'home_score': 0, 'away_score': 0})
    return render(request, "matches/add_match.html", {'form': form, 'HOME_LOCATIONS': HOME_LOCATIONS, 'TEAMS': TEAMS, 'errors': form.errors})

def upcomingMatches(request):
    matches = Match.objects.all()
    matches = matches.order_by('match_date', 'match_time')

    odds = OddsCalc()
    
    for match in matches:
        match.home_team = TEAMS[match.home_team]['name']
        match.away_team = TEAMS[match.away_team]['name']
        match_odds = odds.predict_match_odds(match.home_team, match.away_team)
        match.home_odds = match_odds['home_odds']
        match.draw_odds = match_odds['draw_odds']
        match.away_odds = match_odds['away_odds']
    return render(request, "matches/upcoming_matches.html", {'matches': matches})