from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login 
from django.contrib.auth.decorators import login_required

# Create your views here.
# Request Handler, not actually 'views' in the sense of 'views' in MVC

def home(request):
    return render(request, 'landing_page.html')

def register(request):
    if request.method == 'POST':
        # Register the user
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'user/register.html', {'form': form})


@login_required
def profile(request):
    current_user = request.user
    account = current_user.account
    print(f"Current User: {current_user}")
    print(f"Account: {account}")
    
    return render(request, 'user/profile.html', {'current_user': current_user, 'credits': current_user.account.get_credits()})
