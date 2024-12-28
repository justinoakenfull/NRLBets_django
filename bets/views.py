from django.shortcuts import render, get_object_or_404, redirect
from django.http import request, response, JsonResponse
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.timezone import now, make_aware
from .models import UserBet
from .choices import BET_STATUS
from matches.models import Match
from matches.utils import get_match_round, get_matches_by_round, get_team_attribute, get_location_full
from core.models import Account
from decimal import Decimal
from datetime import datetime
from .utils import get_all_user_bets
from itertools import groupby
import json


### Add Bet
@login_required
def add_Bet(request):
    if request.method != 'POST':
        messages.error(request, 'Invalid HTTP method. Use POST.')
        return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)
    
    try:
            
        data = json.loads(request.body)
        bets = data.get('bets', [])
        user_id = request.user.account.id
        current_user = User.objects.get(pk=user_id)

        created_bets = []
        credits_to_remove = 0

        if not bets:
            messages.error(request, 'No bets provided in the request.')
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
                    messages.error(request, 'Invalid team choice. Must be one of: home, draw, away.')
                    raise ValidationError('Invalid team choice. Must be one of: home, draw, away.')
                if bet_amount < 0:
                    messages.error(request, 'Bet amount must be a positive number.')
                    raise ValidationError('Bet amount must be a positive number.')
                if home_odds < 0 or draw_odds < 0 or away_odds < 0:
                    messages.error(request, 'Odds must be positive numbers.')
                    raise ValidationError('Odds must be positive numbers.')
                if not match:
                    messages.error(request, f'Match with the id: {match_id} does not exist.')
                    raise ValidationError(f'Match with the id: {match_id} does not exist.')
                match_start = make_aware(datetime.combine(match.match_date, match.match_time))
                if match_start < now():
                    messages.error(request, 'Match has already started. Bets cannot be placed on past matches.')
                    raise ValidationError('Match has already started. Bets cannot be placed on past matches.')
                if (bet_amount+credits_to_remove) > user.get_credits():
                    messages.error(request, 'Insufficient balance to place bet.')
                    raise ValidationError('Insufficient balance to place bet.')
                existing_bet = UserBet.objects.filter(user=user, match=match_id, status='Pending').first()
                if existing_bet:
                    messages.error(request, 'Bet already exists for this match. Multiple bets are not allowed.')
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
        messages.success(request, 'Bets created successfully.')
        return JsonResponse({'message': 'Bets created successfully.', 'created_bets': created_bets}, status=201)
    except ValidationError as e:
        messages.error(request, str(e))
        return JsonResponse({'error': str(e)}, status=400)
    except json.JSONDecodeError:
        messages.error(request, 'Invalid JSON payload.')
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return JsonResponse({'error': f"An unexpected error occurred: {str(e)}"}, status=500)

### Get Bet
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
        bet.team_choice_colour = get_team_attribute(bet.match.home_team if bet.team_choice == 'home' else bet.match.away_team, "color")
    
    settled_bets = [bet for bet in bets if bet.status != 'Pending' and bet.status != 'Cancelled']
    cancelled_bets = [bet for bet in bets if bet.status == 'Cancelled']
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

    cancelled_bets_with_rounds = [
        {
            'bet': bet,
            'round_number': get_match_round(bet.match.match_date)
        }
        for bet in cancelled_bets
    ]

    grouped_bets = {}
    for round_number, bets_in_round in groupby(pending_bets_with_rounds, key=lambda x: x['round_number']):
        grouped_bets[round_number] = [bet['bet'] for bet in bets_in_round]

    grouped_settled_bets = {}
    for round_number, bets_in_round in groupby(settled_bets_with_rounds, key=lambda x: x['round_number']):
        grouped_settled_bets[round_number] = [bet['bet'] for bet in bets_in_round]
    
    grouped_cancelled_bets = {}
    for round_number, bets_in_round in groupby(cancelled_bets_with_rounds, key=lambda x: x['round_number']):
        grouped_cancelled_bets[round_number] = [bet['bet'] for bet in bets_in_round]

    active_bets_count = len(pending_bets)
    print(len(settled_bets))
    return render(request, "bets.html", {'grouped_bets': grouped_bets, 'grouped_settled_bets': grouped_settled_bets, 'grouped_cancelled_bets': grouped_cancelled_bets, 'cancelled_bets_count': len(cancelled_bets), 'active_bets_count': len(pending_bets), 'settled_bets_count': len(settled_bets)})

### Cancel Bet
@login_required
def cancel_bet(request, bet_id):
    if request.method != 'POST':
        messages.error(request, 'Invalid HTTP method. Use DELETE.')
        return redirect('all_user_bets')
    
    user = request.user.account
    bet = get_object_or_404(UserBet, pk=bet_id)

    if bet.status != 'Pending':
        messages.error(request, f'Bet cannot be cancelled. Current status: {bet.status}. It must be "Pending" to cancel.')
        return redirect('all_user_bets')
    if bet.user != user:
        messages.error(request, 'You are not authorized to cancel this bet.')
        return redirect('all_user_bets')
    bet.status = BET_STATUS.get('Cancelled', 'Cancelled')
    bet.save()

    user.add_credits(bet.bet_amount)

    messages.success(request, 'Bet cancelled successfully.')
    return redirect('all_user_bets')