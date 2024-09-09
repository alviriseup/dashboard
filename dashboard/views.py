from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User


@login_required
def user_list(request):
    query = request.GET.get('search', '')
    # users = User.objects.all()
    users = User.objects.filter(username__icontains=query)

    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # return render(request, 'dashboard/user_list.html', {'users': users, 'query': query})
    return render(request, 'dashboard/user_list.html', {'page_obj': page_obj, 'query': query})

