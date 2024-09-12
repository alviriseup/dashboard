from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', user_profile, name='user-profile'),
    path('profile/update_user_info', update_user_info, name='update-user-info'),
    path('profile/update_password', update_password, name='update-password'),
]
