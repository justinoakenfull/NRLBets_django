from django.shortcuts import render, redirect
from .forms import AddMatchForm
from .choices import HOME_LOCATIONS, TEAMS

# Create your views here.

def AddMatch(request):

    if request.method == 'POST':
        form = AddMatchForm(request.POST)
        # Process the form
        print("Processing form")
        add_match = form
        print(add_match)
        print("Checking if form is valid")
        if add_match.is_valid():
            print("Form is valid")
            add_match.save()
            print("Match saved")
            return redirect('home')
        print("Form is not valid")
        print(add_match.errors)
        return render(request, "matches/add_match.html", {'form': form, 'HOME_LOCATIONS': HOME_LOCATIONS, 'TEAMS': TEAMS, 'errors': form.errors})
    else:
        form = AddMatchForm(initial={'home_score': 0, 'away_score': 0})
    return render(request, "matches/add_match.html", {'form': form, 'HOME_LOCATIONS': HOME_LOCATIONS, 'TEAMS': TEAMS, 'errors': form.errors})