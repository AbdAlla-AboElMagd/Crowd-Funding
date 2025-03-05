"""
URL configuration for project project.

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
from django.shortcuts import render
from django.urls import path
from django.contrib.auth import views as auth_views  
from crowdFunding.views import about, custom_login, custom_logout, home, signup ,activate
from django.conf.urls import handler404 
from crowdFunding.views import about, home, signup

def custom_page_not_found(request, exception):
    return render(request, 'crowdFunding/404.html', status=404)

handler404 = custom_page_not_found
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('about/', about, name='about'),
    path('signup/', signup, name='signup'),  
    # path('login/', auth_views.LoginView.as_view(template_name='crowdFunding/login.html'), name='login'),
     path('login/', custom_login, name='login'), 
    path('logout/', custom_logout, name='logout'),  
     path('activate/<uidb64>/<token>/', activate, name='activate'),
]
