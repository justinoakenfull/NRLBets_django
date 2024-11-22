# import csv
# from datetime import datetime

# START_DATE_2024 = datetime.strptime("03-Mar-24", "%d-%b-%y")
# START_DATE_2023 = datetime.strptime("02-Mar-23", "%d-%b-%y")
# START_DATE_2022 = datetime.strptime("10-Mar-22", "%d-%b-%y")
# START_DATE_2021 = datetime.strptime("11-Mar-21", "%d-%b-%y")
# START_DATE_2020 = datetime.strptime("12-Mar-20", "%d-%b-%y")
# END_DATE_2024 = datetime.strptime("06-Oct-24", "%d-%b-%y")
# END_DATE_2023 = datetime.strptime("01-Oct-23", "%d-%b-%y")
# END_DATE_2022 = datetime.strptime("02-Oct-22", "%d-%b-%y")
# END_DATE_2021 = datetime.strptime("03-Oct-21", "%d-%b-%y")
# END_DATE_2020 = datetime.strptime("25-Oct-20", "%d-%b-%y")

# def calculate_odds():
#     data = load_csv("odds/data/nrl_history.csv")
#     current_date = datetime.now()

#     team_stats = {}

#     for row in data:
#         home_team = row["Home Team"]
#         away_team = row['Away Team']
#         home_score = row['Home Score']
#         away_score = row['Away Score']
#         game_date = datetime.strptime(row["Date"], "%d-%b-%y")
#         game_weight = calculate_game_weight(game_date, current_date)

#         initialize_team_stats(team_stats, home_team)
#         initialize_team_stats(team_stats, away_team)    
        
#         team_stats[home_team]['home_games'] += game_weight
#         if home_score > away_score:
#             team_stats[home_team]['home_wins'] += game_weight
#         elif home_score < away_score:
#             team_stats[home_team]['home_losses'] += game_weight
#         else:
#             team_stats[home_team]['home_draws'] += game_weight
        
#         team_stats[away_team]['away_games'] += game_weight
#         if away_score > home_score:
#             team_stats[away_team]['away_wins'] += game_weight
#         elif away_score < home_score:
#             team_stats[away_team]['away_losses'] += game_weight
#         else:
#             team_stats[away_team]['away_draws'] += game_weight

#     for team, stats in team_stats.items():
#         stats['home_win_prob'] = stats['home_wins'] / stats['home_games'] if stats['home_games'] > 0 else 0
#         stats['away_win_prob'] = stats['away_wins'] / stats['away_games'] if stats['away_games'] > 0 else 0
#         stats['draw_prob'] = stats['home_draws'] / stats['home_games'] if stats['home_games'] > 0 else 0


#     odds = predict_match_odds("Melbourne Storm", "Penrith Panthers", team_stats)
#     print("Melbourne Storm: ", odds['home_odds'], "Penrith Panthers: ", odds['away_odds'], "Draw Odds: ", odds['draw_odds'])
#     odds = predict_match_odds("Penrith Panthers", "Cronulla-Sutherland Sharks", team_stats)
#     print("Penrith Panthers: ", odds['home_odds'], "Cronulla-Sutherland Sharks: ", odds['away_odds'], "Draw Odds: ", odds['draw_odds'])
#     odds = predict_match_odds("Canterbury Bulldogs", "Manly-Warringah Sea Eagles", team_stats)
#     print("Canterbury Bulldogs: ", odds['home_odds'], "Manly-Warringah Sea Eagles: ", odds['away_odds'], "Draw Odds: ", odds['draw_odds'])

#     print("Done")

# def load_csv(file_path):
    
#     with open(file_path, 'r') as file:
#         reader = csv.DictReader(file)
#         data = [row for row in reader]
#     return data

# def initialize_team_stats(team_stats, team):
#     if team not in team_stats:
#         team_stats[team] = {
#             'home_games': 0,
#             'home_wins': 0,
#             'home_losses': 0,
#             'home_draws': 0,
#             'away_games': 0,
#             'away_wins': 0,
#             'away_losses': 0,
#             'away_draws': 0,
#         }

# def predict_match_odds(home_team, away_team, team_stats, home_advantage_factor=0.1):
#     # Get baseline probabilities for both teams
#     home_stats = team_stats.get(home_team, {"home_win_prob": 0.5, "draw_prob": 0.1})
#     away_stats = team_stats.get(away_team, {"away_win_prob": 0.5, "draw_prob": 0.1})

#     # Extract probabilities
#     home_win_prob = home_stats["home_win_prob"]
#     away_win_prob = away_stats["away_win_prob"]
#     draw_prob = (home_stats["draw_prob"] + away_stats["draw_prob"]) / 2

#     # Adjust for home advantage
#     adjusted_home_win_prob = home_win_prob + home_advantage_factor
#     adjusted_away_win_prob = away_win_prob
#     adjusted_draw_prob = draw_prob - (home_advantage_factor / 2)

#     # Normalize probabilities to sum to 1
#     total_prob = adjusted_home_win_prob + adjusted_away_win_prob + adjusted_draw_prob
#     adjusted_home_win_prob /= total_prob
#     adjusted_away_win_prob /= total_prob
#     adjusted_draw_prob /= total_prob

#     # Convert probabilities to odds
#     home_odds = 1 / adjusted_home_win_prob
#     away_odds = 1 / adjusted_away_win_prob
#     draw_odds = 1 / adjusted_draw_prob

#     return {
#         "home_odds": round(home_odds, 2),
#         "away_odds": round(away_odds, 2),
#         "draw_odds": abs(round(draw_odds, 2))
#     }

# def calculate_game_weight(game_date, current_date):
#     past_seasons = (current_date.year - game_date.year)
#     if past_seasons == 0:
#         return linear_decay(game_date, START_DATE_2024, END_DATE_2024, 1.0, 0.8)
#     if past_seasons == 1:
#         return linear_decay(current_date, START_DATE_2023, END_DATE_2023, 0.79, 0.6)
#     if past_seasons == 2:
#         return linear_decay(current_date, START_DATE_2022, END_DATE_2022, 0.59, 0.4)
#     if past_seasons == 3:
#         return linear_decay(current_date, START_DATE_2021, END_DATE_2021, 0.39, 0.2)
#     if past_seasons == 4:
#         return linear_decay(current_date, START_DATE_2020, END_DATE_2020, .19, 0.05)
#     else:
#         return 0.05

# def linear_decay(game_date, season_first_date, season_last_date, max_weight, min_weight):
#     """
#     Apply linear decay within a season based on the earliest and latest game dates in the data.
#     :param game_date: Date of the game (datetime object).
#     :param season_first_date: First game date of the season (datetime object).
#     :param season_last_date: Last game date of the season (datetime object).
#     :param max_weight: Maximum weight (latest game in the season).
#     :param min_weight: Minimum weight (earliest game in the season).
#     :return: Weight (float)
#     """

#     # Total duration of the season
#     total_days = (season_last_date - season_first_date).days
#     game_position = (game_date - season_first_date).days

#     # Linear interpolation
#     weight = (game_position / total_days) * (max_weight - (max_weight - min_weight)) + (max_weight - min_weight)
#     return weight

# calculate_odds()

import csv
import os
from datetime import datetime
from django.conf import settings

class OddsCalculator:
    START_DATES = {
        2024: datetime.strptime("03-Mar-24", "%d-%b-%y"),
        2023: datetime.strptime("02-Mar-23", "%d-%b-%y"),
        2022: datetime.strptime("10-Mar-22", "%d-%b-%y"),
        2021: datetime.strptime("11-Mar-21", "%d-%b-%y"),
        2020: datetime.strptime("12-Mar-20", "%d-%b-%y"),
    }
    END_DATES = {
        2024: datetime.strptime("06-Oct-24", "%d-%b-%y"),
        2023: datetime.strptime("01-Oct-23", "%d-%b-%y"),
        2022: datetime.strptime("02-Oct-22", "%d-%b-%y"),
        2021: datetime.strptime("03-Oct-21", "%d-%b-%y"),
        2020: datetime.strptime("25-Oct-20", "%d-%b-%y"),
    }

    def __init__(self):
        self.team_stats = {}
        self.current_date = datetime.now()
        self.data = self.load_csv()
        self.calculate_team_stats()

    def load_csv(self):
        file_path = os.path.join(settings.BASE_DIR, 'odds', 'data', 'nrl_history.csv')
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]

    def calculate_team_stats(self):
        for row in self.data:
            home_team = row["Home Team"]
            away_team = row["Away Team"]
            home_score = int(row["Home Score"])
            away_score = int(row["Away Score"])
            game_date = datetime.strptime(row["Date"], "%d-%b-%y")
            game_weight = self.calculate_game_weight(game_date)

            self.initialize_team_stats(home_team)
            self.initialize_team_stats(away_team)

            # Update home team stats
            self.team_stats[home_team]['home_games'] += game_weight
            if home_score > away_score:
                self.team_stats[home_team]['home_wins'] += game_weight
            elif home_score < away_score:
                self.team_stats[home_team]['home_losses'] += game_weight
            else:
                self.team_stats[home_team]['home_draws'] += game_weight

            # Update away team stats
            self.team_stats[away_team]['away_games'] += game_weight
            if away_score > home_score:
                self.team_stats[away_team]['away_wins'] += game_weight
            elif away_score < home_score:
                self.team_stats[away_team]['away_losses'] += game_weight
            else:
                self.team_stats[away_team]['away_draws'] += game_weight

        # Calculate probabilities
        for team, stats in self.team_stats.items():
            stats['home_win_prob'] = (
                stats['home_wins'] / stats['home_games'] if stats['home_games'] > 0 else 0
            )
            stats['away_win_prob'] = (
                stats['away_wins'] / stats['away_games'] if stats['away_games'] > 0 else 0
            )
            stats['draw_prob'] = (
                stats['home_draws'] / stats['home_games'] if stats['home_games'] > 0 else 0
            )

    def initialize_team_stats(self, team):
        if team not in self.team_stats:
            self.team_stats[team] = {
                'home_games': 0,
                'home_wins': 0,
                'home_losses': 0,
                'home_draws': 0,
                'away_games': 0,
                'away_wins': 0,
                'away_losses': 0,
                'away_draws': 0,
            }

    def calculate_game_weight(self, game_date):
        past_seasons = self.current_date.year - game_date.year
        if past_seasons == 0:
            return self.linear_decay(
                game_date,
                self.START_DATES[game_date.year],
                self.END_DATES[game_date.year],
                max_weight=1.0,
                min_weight=0.8,
            )
        elif past_seasons == 1:
            return self.linear_decay(
                game_date,
                self.START_DATES[game_date.year],
                self.END_DATES[game_date.year],
                max_weight=0.79,
                min_weight=0.6,
            )
        elif past_seasons == 2:
            return self.linear_decay(
                game_date,
                self.START_DATES[game_date.year],
                self.END_DATES[game_date.year],
                max_weight=0.59,
                min_weight=0.4,
            )
        elif past_seasons == 3:
            return self.linear_decay(
                game_date,
                self.START_DATES[game_date.year],
                self.END_DATES[game_date.year],
                max_weight=0.39,
                min_weight=0.2,
            )
        elif past_seasons == 4:
            return self.linear_decay(
                game_date,
                self.START_DATES[game_date.year],
                self.END_DATES[game_date.year],
                max_weight=0.19,
                min_weight=0.05,
            )
        else:
            return 0.05

    def linear_decay(self, game_date, season_first_date, season_last_date, max_weight, min_weight):
        total_days = (season_last_date - season_first_date).days
        game_position = (game_date - season_first_date).days
        weight = ((game_position / total_days) * (max_weight - min_weight)) + min_weight
        return weight

    def predict_match_odds(self, home_team, away_team, home_advantage_factor=0.1):
        # Get baseline probabilities
        home_stats = self.team_stats.get(home_team, {
            'home_win_prob': 0.5,
            'draw_prob': 0.1
        })
        away_stats = self.team_stats.get(away_team, {
            'away_win_prob': 0.5,
            'draw_prob': 0.1
        })

        # Extract probabilities
        home_win_prob = home_stats['home_win_prob']
        away_win_prob = away_stats['away_win_prob']
        draw_prob = (home_stats['draw_prob'] + away_stats['draw_prob']) / 2

        # Adjust for home advantage
        adjusted_home_win_prob = home_win_prob + home_advantage_factor
        adjusted_away_win_prob = away_win_prob
        adjusted_draw_prob = draw_prob - (home_advantage_factor / 2)

        # Normalize probabilities
        total_prob = adjusted_home_win_prob + adjusted_away_win_prob + adjusted_draw_prob
        adjusted_home_win_prob /= total_prob
        adjusted_away_win_prob /= total_prob
        adjusted_draw_prob /= total_prob

        # Convert probabilities to odds
        home_odds = 1 / adjusted_home_win_prob if adjusted_home_win_prob > 0 else float('inf')
        away_odds = 1 / adjusted_away_win_prob if adjusted_away_win_prob > 0 else float('inf')
        draw_odds = 1 / adjusted_draw_prob if adjusted_draw_prob > 0 else float('inf')

        return {
            'home_odds': round(home_odds, 2),
            'away_odds': round(away_odds, 2),
            'draw_odds': abs(round(draw_odds, 2)),
        }
