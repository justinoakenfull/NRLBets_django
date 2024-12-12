from django.shortcuts import render
from django.http import request, response, JsonResponse
from django.core.exceptions import ValidationError
from django.db import transaction
import json
from django.contrib.auth.decorators import login_required
from .models import UserBet
from matches.models import Match
from matches.utils import get_match_round, get_matches_by_round, get_team_attribute, get_location_full
from django.contrib.auth.models import User
from core.models import Account
from decimal import Decimal
from django.utils.timezone import now, make_aware
from datetime import datetime
from .utils import get_all_user_bets
from itertools import groupby

# # Create your views here.
# def AddBet(request):

#     if request.method == 'POST':
#         json_data = json.loads(request.body)
#         print(json_data)
#         for bet in json_data:
#             print(bet)
#             return response.HttpResponse("Bet added")

#     return render(request, "bets/add_match.html", {})

@login_required
def add_Bet(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)
    
    try:
            
        data = json.loads(request.body)
        bets = data.get('bets', [])
        user_id = request.user.account.id
        current_user = User.objects.get(pk=user_id)

        created_bets = []
        credits_to_remove = 0

        if not bets:
            raise ValidationError('No bets provided in the request.')

        with transaction.atomic():
            for bet in bets:
                user = Account.objects.get(user=current_user)
                match_id = bet.get('match_id')
                home_odds = Decimal(bet.get('bet_home_odds').strip().replace('$', ''))
                draw_odds = Decimal(bet.get('bet_draw_odds').strip().replace('$', ''))
                away_odds = Decimal(bet.get('bet_away_odds').strip().replace('$', ''))
                bet_amount = Decimal(bet.get('bet_amount'))
                team_choice = bet.get('team_choice')
                payout = Decimal(bet.get('payout')) # Potential payout
                created_at = now()
                updated_at = now()
                match = Match.objects.filter(match_id=match_id).first()

                if team_choice not in ['home', 'draw', 'away']:
                    raise ValidationError('Invalid team choice. Must be one of: home, draw, away.')
                if bet_amount < 0:
                    raise ValidationError('Bet amount must be a positive number.')
                if home_odds < 0 or draw_odds < 0 or away_odds < 0:
                    raise ValidationError('Odds must be positive numbers.')
                if not match:
                    raise ValidationError(f'Match with the id: {match_id} does not exist.')
                match_start = make_aware(datetime.combine(match.match_date, match.match_time))
                if match_start < now():
                    raise ValidationError('Match has already started. Bets cannot be placed on past matches.')
                if (bet_amount+credits_to_remove) > user.get_credits():
                    raise ValidationError('Insufficient balance to place bet.')
                existing_bet = UserBet.objects.filter(user=user, match=match_id)
                if existing_bet:
                    raise ValidationError('Bet already exists for this match. Multiple bets are not allowed.')
                new_bet = UserBet.objects.create(
                    user=user,
                    match=match,
                    home_odds=home_odds,
                    draw_odds=draw_odds,
                    away_odds=away_odds,
                    bet_amount=bet_amount,
                    team_choice=team_choice,
                    payout=payout,
                    created_at=created_at,
                    updated_at=updated_at
                )
                credits_to_remove += bet_amount
                created_bets.append(bet)
            user.remove_credits(credits_to_remove)

        return JsonResponse({'message': 'Bets created successfully.', 'created_bets': created_bets}, status=201)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)
    
@login_required
def get_current_bets(request):
    user_id = request.user.account.id

    bets = get_all_user_bets(user_id)
    for bet in bets:
        bet.match.home_team_color = get_team_attribute(bet.match.home_team, "color")
        bet.match.away_team_color = get_team_attribute(bet.match.away_team, "color")
        bet.match.home_team_full = get_team_attribute(bet.match.home_team, "name")
        bet.match.away_team_full = get_team_attribute(bet.match.away_team, "name")
        bet.match.match_location_full = get_location_full(bet.match.match_location)
    
    settled_bets = [bet for bet in bets if bet.status != 'Pending']
    pending_bets = [bet for bet in bets if bet.status == 'Pending']

    pending_bets_with_rounds = [
        {
            'bet': bet,
            'round_number': get_match_round(bet.match.match_date)
        }
        for bet in pending_bets
    ]

    settled_bets_with_rounds = [
        {
            'bet': bet,
            'round_number': get_match_round(bet.match.match_date)
        }
        for bet in settled_bets
    ]

    grouped_bets = {}
    for round_number, bets_in_round in groupby(pending_bets_with_rounds, key=lambda x: x['round_number']):
        grouped_bets[round_number] = [bet['bet'] for bet in bets_in_round]

    grouped_settled_bets = {}
    for round_number, bets_in_round in groupby(settled_bets_with_rounds, key=lambda x: x['round_number']):
        grouped_settled_bets[round_number] = [bet['bet'] for bet in bets_in_round]

    active_bets_count = len(pending_bets)
    print(len(settled_bets))
    return render(request, "bets.html", {'grouped_bets': grouped_bets, 'grouped_settled_bets': grouped_settled_bets, 'active_bets_count': len(pending_bets), 'settled_bets_count': len(settled_bets)})