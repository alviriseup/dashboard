from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.template import Context


def index(request):
    return render(request, 'user/index.html', {'title':'index'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

            messages.success(request, f'Your account has been created ! You are now able to log in')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title':'register here'})


def Login(request):
    if request.method == 'POST':

        # AuthencationForm can also be used. See how to do it!

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f'Welcome {username} !')
            return redirect('index')
        else:
            messages.info(request, f'Account does not exist.')
    form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form, 'title':'log in'})
