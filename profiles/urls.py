"""storefront URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views
from django import forms
from allauth.account.forms import SignupForm
from .forms import ProfileForm, UserForm


urlpatterns = [
    # url from the main sales page
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^profile/update$', views.update_profile, name='update_profile'),
    url(r'^post/$', views.ProfileFormPreview(ProfileForm)),  
    
    url(r'^register/$', views.Wizard.as_view([SignupForm, UserForm, ProfileForm]), name='register'), 
]
