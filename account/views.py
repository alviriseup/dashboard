from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def user_profile(request):
    user = request.user
    context = {
        'full name': f'{user.first_name} {user.last_name}',
        'username': user.username,
        'email': user.email,
    }
    return render(request, 'account/user_profile.html', context)
