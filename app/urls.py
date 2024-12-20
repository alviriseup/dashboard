"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user import views as user_view
from blog import views as blog_view
from django.contrib.auth import views as auth
from .router import router
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),

    # path('', include('user.urls')),
    path('', blog_view.blog_home, name='home'),
    path('account/', include('account.urls')),
    path('blog/', include('blog.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('login/', user_view.Login, name='login'),
    path('logout/', auth.LogoutView.as_view(template_name='user/index.html'), name='logout'),
    path('register/', user_view.register, name='register'),
    path('portal', include('user.urls')),
]
