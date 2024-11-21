from django.shortcuts import render
from .forms import AddMatchForm

# Create your views here.

def AddMatch(request):

    if request.method == 'POST':
        # Process the form
        pass
    else:
        form = AddMatchForm()
    return render(request, "matches/add_match.html", {'form': form})