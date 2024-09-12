from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

from .forms import UpdateUserForm, UpdatePasswordForm


@login_required
def user_profile(request):
    user = request.user
    context = {
        'full_name': f'{user.first_name} {user.last_name}',
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }
    return render(request, 'account/user_profile.html', context)



# Update user first name and last name
@login_required
def update_user_info(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            # return redirect('user-profile')
            return HttpResponseRedirect(reverse('user-profile') + '?tab=settings')
        else:
            messages.error(request, 'Error updating profile info.')

    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'account/user_profile.html', {'user_form': user_form})



# Update user password
@login_required
def update_password(request):
    if request.method == 'POST':
        password_form = UpdatePasswordForm(user=request.user, data=request.POST)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)     # Keeps user logged in after password change
            messages.success(request, 'Your password has been updated successfully!')
            # return redirect('user-profile')
            return HttpResponseRedirect(reverse('user-profile') + '?tab=password')
        else:
            messages.error(request, 'Error updating password.')

    else:
        password_form = UpdatePasswordForm(user=request.user)

    return render(request, 'account/user_profile.html', {'password_form': password_form})
