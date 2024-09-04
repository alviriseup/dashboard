from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User


@login_required
def user_list(request):
    query = request.GET.get('search', '')
    # users = User.objects.all()
    users = User.objects.filter(username__icontains=query)

    return render(request, 'dashboard/user_list.html', {'users': users, 'query': query})

