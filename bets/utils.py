from .models import UserBet


def payout_bets(match_id):
    #TODO: Complete the matchs bets and pay the winners
    pass

def get_all_user_bets(user):
    return UserBet.objects.filter(user=user)