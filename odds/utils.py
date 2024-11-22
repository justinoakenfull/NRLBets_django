import csv
import os
from datetime import datetime
from django.conf import settings

head_to_head_stats_multiplier = 1.5
home_advantage_default = 0.146



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
        self.head_to_head_stats = {}
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
            self.initialize_head_to_head_stats(home_team, away_team)

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

            # Update head-to-head stats with higher weight
            head_to_head_weight = game_weight * head_to_head_stats_multiplier

            # Home team stats in head-to-head
            self.head_to_head_stats[home_team][away_team]['home_games'] += head_to_head_weight
            if home_score > away_score:
                self.head_to_head_stats[home_team][away_team]['home_wins'] += head_to_head_weight
            elif home_score < away_score:
                self.head_to_head_stats[home_team][away_team]['home_losses'] += head_to_head_weight
            else:
                self.head_to_head_stats[home_team][away_team]['home_draws'] += head_to_head_weight

            # Away team stats in head-to-head
            self.head_to_head_stats[away_team][home_team]['away_games'] += head_to_head_weight
            if away_score > home_score:
                self.head_to_head_stats[away_team][home_team]['away_wins'] += head_to_head_weight
            elif away_score < home_score:
                self.head_to_head_stats[away_team][home_team]['away_losses'] += head_to_head_weight
            else:
                self.head_to_head_stats[away_team][home_team]['away_draws'] += head_to_head_weight

        # Calculate overall probabilities
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

        # Calculate head-to-head probabilities
        for team1, opponents in self.head_to_head_stats.items():
            for team2, stats in opponents.items():
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

    def initialize_head_to_head_stats(self, team1, team2):
        if team1 not in self.head_to_head_stats:
            self.head_to_head_stats[team1] = {}
        if team2 not in self.head_to_head_stats[team1]:
            self.head_to_head_stats[team1][team2] = {
                'home_games': 0,
                'home_wins': 0,
                'home_losses': 0,
                'home_draws': 0,
                'away_games': 0,
                'away_wins': 0,
                'away_losses': 0,
                'away_draws': 0,
            }
        if team2 not in self.head_to_head_stats:
            self.head_to_head_stats[team2] = {}
        if team1 not in self.head_to_head_stats[team2]:
            self.head_to_head_stats[team2][team1] = {
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
                max_weight=0.8,
                min_weight=0.6,
            )
        elif past_seasons == 2:
            return self.linear_decay(
                game_date,
                self.START_DATES[game_date.year],
                self.END_DATES[game_date.year],
                max_weight=0.6,
                min_weight=0.4,
            )
        elif past_seasons == 3:
            return self.linear_decay(
                game_date,
                self.START_DATES[game_date.year],
                self.END_DATES[game_date.year],
                max_weight=0.4,
                min_weight=0.2,
            )
        elif past_seasons == 4:
            return self.linear_decay(
                game_date,
                self.START_DATES[game_date.year],
                self.END_DATES[game_date.year],
                max_weight=0.2,
                min_weight=0.05,
            )
        else:
            return 0.05

    def linear_decay(self, game_date, season_first_date, season_last_date, max_weight, min_weight):
        total_days = (season_last_date - season_first_date).days
        game_position = (game_date - season_first_date).days
        weight = ((game_position / total_days) * (max_weight - min_weight)) + min_weight
        return weight

    def predict_match_odds(self, home_team, away_team, home_advantage_factor=home_advantage_default):
        # Get baseline probabilities
        home_stats = self.team_stats.get(home_team, {
            'home_win_prob': 0.5,
            'draw_prob': 0.1
        })
        away_stats = self.team_stats.get(away_team, {
            'away_win_prob': 0.5,
            'draw_prob': 0.1
        })

        # Get head-to-head stats
        head_to_head_home_stats = self.head_to_head_stats.get(home_team, {}).get(away_team, None)
        head_to_head_away_stats = self.head_to_head_stats.get(away_team, {}).get(home_team, None)

        # Calculate combined probabilities
        home_win_prob = home_stats['home_win_prob']
        away_win_prob = away_stats['away_win_prob']
        draw_prob = (home_stats['draw_prob'] + away_stats['draw_prob']) / 2

        if head_to_head_home_stats and head_to_head_away_stats:
            # Give higher weight to head-to-head stats
            h2h_home_win_prob = head_to_head_home_stats['home_win_prob']
            h2h_away_win_prob = head_to_head_away_stats['away_win_prob']
            h2h_draw_prob = (head_to_head_home_stats['draw_prob'] + head_to_head_away_stats['draw_prob']) / 2

            # Combine probabilities (you can adjust the weighting factors as needed)
            total_weight = 1.0 + head_to_head_stats_multiplier  # Base weight + head-to-head weight
            home_win_prob = (home_win_prob + head_to_head_stats_multiplier * h2h_home_win_prob) / total_weight
            away_win_prob = (away_win_prob + head_to_head_stats_multiplier * h2h_away_win_prob) / total_weight
            draw_prob = (draw_prob + head_to_head_stats_multiplier * h2h_draw_prob) / total_weight

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
        home_odds = 1 / adjusted_home_win_prob
        away_odds = 1 / adjusted_away_win_prob
        draw_odds = 1 / adjusted_draw_prob
        return {
            'home_odds': round(home_odds, 2),
            'away_odds': round(away_odds, 2),
            'draw_odds': abs(round(draw_odds, 2)),
        }
