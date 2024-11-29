from django.shortcuts import render
from django.http import request, response
import json

# Create your views here.
def AddBet(request):

    if request.method == 'POST':
        json_data = json.loads(request.body)
        print(json_data)
        for bet in json_data:
            print(bet)
            return response.HttpResponse("Bet added")

    return render(request, "bets/add_match.html", {})