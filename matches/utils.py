from django.db.models import F, Value, IntegerField, ExpressionWrapper, Func, Exists, OuterRef, Value, BooleanField
from django.db.models.functions import Coalesce
from odds.utils import OddsCalculator as OddsCalc
from .choices import TEAMS, TEAMS_KEYS, HOME_LOCATIONS
from .models import Match
from bets.models import UserBet

def update_match_odds(matches):
    oddsCalc = OddsCalc()
    for match in matches:
        odds = oddsCalc.predict_match_odds(TEAMS_KEYS[match.home_team], TEAMS_KEYS[match.away_team])
        match.home_odds = odds['home_odds']
        match.draw_odds = odds['draw_odds']
        match.away_odds = odds['away_odds']
        match.save()

def get_match(match_id):
    match = Match.objects.get(match_id=match_id)
    # Dynamically add color attributes
    match.home_team_color = TEAMS.get(match.home_team, {}).get("color", "#CCCCCC")
    match.away_team_color = TEAMS.get(match.away_team, {}).get("color", "#CCCCCC")
    # Rename teams to full names
    match.home_team_full = TEAMS.get(match.home_team, {}).get("name", match.home_team)
    match.away_team_full = TEAMS.get(match.away_team, {}).get("name", match.away_team)
    # Add full location name
    match.match_location_full = HOME_LOCATIONS.get(match.match_location, match.match_location)
    
    return match

# Utility function for team attributes
def get_team_attribute(team_key, attribute):
    return TEAMS.get(team_key, {}).get(attribute, f"Unknown {attribute}")

def get_location_full(location_key):
    return HOME_LOCATIONS.get(location_key, location_key)

# Query to fetch matches and annotate dynamic fields
def get_matches_by_round(round, user):
    assert 1 <= round <= 27, "Round must be between 1 and 27"

    matches = Match.objects.all().order_by('match_date', 'match_time')

    
    filtered_matches = []

    if user.is_authenticated:
        # Annotate user bets for authenticated users
        matches = matches.annotate(
            user_has_bet=Exists(
                UserBet.objects.filter(
                    user=user.account,
                    match=OuterRef('pk'),
                    status='Pending'
                )
            )
        )
    else:
        # Default annotation for unauthenticated users
        matches = Match.objects.filter(pk__in=[m.pk for m in matches]).annotate(
            user_has_bet=Value(False, output_field=BooleanField())
        )

    for match in matches:
        match.match_round = get_match_round(match.match_date)
        if round == match.match_round:
            filtered_matches.append(match)

    # Update odds for the filtered matches
    update_match_odds(filtered_matches)

    return filtered_matches


def get_match_round(match_date):
    match_round = match_date.isocalendar()[1] - 9

    return max(1, match_round)

def get_team_colour(team):
    return TEAMS.get(team, {}).get("color", "#CCCCCC")