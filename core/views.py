from django.shortcuts import render

# Create your views here.
# Request Handler, not actually 'views' in the sense of 'views' in MVC

def home(request):
    return render(request, 'landing_page.html')