from odds.utils import OddsCalculator as OddsCalc
from .choices import TEAMS, TEAMS_KEYS, HOME_LOCATIONS
from .models import Match

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

def get_match_round(match_id):
    match = Match.objects.get(match_id=match_id)
    match_round = match.match_date.isocalendar()[1]-9

    if match_round == 0:
        return 1
    return match_round