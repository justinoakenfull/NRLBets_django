from django.shortcuts import render, redirect
from django.db.models import Exists, OuterRef, Value, BooleanField
from .forms import AddMatchForm
from .choices import HOME_LOCATIONS, TEAMS, TEAMS_KEYS, MATCH_STATUS
from .models import Match

from odds.utils import OddsCalculator as OddsCalc
from bets.utils import payout_bets
from .utils import get_matches_by_round, get_team_attribute, get_location_full
from .utils import update_match_odds, get_match, get_match_round

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
            # Set the status
            match.status = MATCH_STATUS["Scheduled"]
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
    round = int(request.GET.get('round', 1))
    round = max(1, min(round, 27))  # Ensure round is between 1 and 27

    # Fetch matches for the specified round
    matches = get_matches_by_round(round, request.user)

    # Process annotations for team names and colors dynamically
    for match in matches:
        match.home_team_color = get_team_attribute(match.home_team, "color")
        match.away_team_color = get_team_attribute(match.away_team, "color")
        match.home_team_full = get_team_attribute(match.home_team, "name")
        match.away_team_full = get_team_attribute(match.away_team, "name")
        match.match_location_full = get_location_full(match.match_location)

    user_credits = request.user.account.credits if request.user.is_authenticated else 0

    return render(request, "matches/matches.html", {
        'matches': matches,
        'round': round,
        'next_round': round + 1,
        'previous_round': round - 1,
        'user_credits': user_credits,
    })


def completeMatch(request):
    match_id = request.GET.get('match_id')
    match = get_match(match_id)
    match_round = get_match_round(match.match_date)
    if request.method == 'POST':
        home_score = request.POST.get('home_score')
        away_score = request.POST.get('away_score')
        try:
            home_score = int(home_score)
            away_score = int(away_score)
        except:
            return render(request, "matches/complete_match.html", {'match': match, 'TEAMS': TEAMS, 'round': match_round, 'errors': {"Scores must be integers"}})
        match.set_home_score(home_score)
        match.set_away_score(away_score)
        match.status = MATCH_STATUS["Full Time"]
        match.save()
        # Call function to complete bets
        payout_bets(match_id)
        return redirect('upcoming_matches')
    
    return render(request, "matches/complete_match.html", {'match': match, 'TEAMS': TEAMS, 'round': match_round})

