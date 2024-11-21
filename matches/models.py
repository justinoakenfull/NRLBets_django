from django.db import models
from .choices import HOME_LOCATIONS, TEAMS

# Create your models here.
class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_date = models.DateTimeField()
    match_time = models.TimeField()
    match_location = models.CharField(max_length=100, choices=HOME_LOCATIONS)
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_score = models.IntegerField(max_length=100, choices=TEAMS)
    away_score = models.IntegerField(max_length=100, choices=TEAMS)
    home_odds = models.DecimalField(max_digits=4, decimal_places=2)
    draw_odds = models.DecimalField(max_digits=4, decimal_places=2)
    away_odds = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.match_date} - {self.match_time}"
    
    def set_home_score(self, score):
        if score >= 0:
            self.home_score = score
        self.save()

    def set_away_score(self, score):
        if score >= 0:
            self.away_score = score
        self.save()

    def get_winner(self):
        if self.home_score > self.away_score:
            return self.home_team
        elif self.away_score > self.home_score:
            return self.away_team
        else:
            return "Draw"
        
    def get_odds(self, team):
        if team == self.home_team:
            return self.home_odds
        elif team == self.away_team:
            return self.away_odds
        else:
            return self.draw_odds