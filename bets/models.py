from django.db import models
from .choices import TEAM_CHOICE, BET_STATUS

# A user's bet on an NRL match
class UserBet(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('core.Account', on_delete=models.CASCADE)
    match = models.ForeignKey('matches.Match', on_delete=models.CASCADE)
    home_score = models.IntegerField(null=True, blank=True)  # Nullable for scoreline bets
    away_score = models.IntegerField(null=True, blank=True)
    home_odds = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    draw_odds = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    away_odds = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    bet_amount = models.DecimalField(max_digits=10, decimal_places=2)
    team_choice = models.CharField(max_length=100, choices=TEAM_CHOICE, null=True, blank=True)
    payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=BET_STATUS, default='Pending')

    class Meta:
        db_table = 'user_bets'
        verbose_name = 'User Bet'
        verbose_name_plural = 'User Bets'

    def __str__(self):
        return f"{self.user.user.username} - {self.match.home_team} vs {self.match.away_team}"
    
    def get_bet_odds(self):
        if self.team_choice == 'home':
            return self.home_odds
        elif self.team_choice == 'away':
            return self.away_odds
        elif self.team_choice == 'draw':
            return self.draw_odds
        else:
            return None # Invalid team choice
