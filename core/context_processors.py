from django.contrib.auth.decorators import login_required

def user_credits(request):
    if request.user.is_authenticated:
        # Replace `credits` with the actual attribute or related field that stores user credits

        credits = request.user.account.credits
    else:
        credits = None
    return {'user_credits': credits}
